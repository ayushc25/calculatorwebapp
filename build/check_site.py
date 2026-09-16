# -*- coding: utf-8 -*-
"""Structural checks over the generated HTML.

Validates: tag balance, internal link targets, duplicate ids, label/for wiring,
error-box presence for every input, and that each calculator page exposes the
field ids its JavaScript module reads.

Run:  python build/check_site.py
"""

import os
import re
import sys
from html.parser import HTMLParser

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VOID = {'area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input', 'link',
        'meta', 'param', 'source', 'track', 'wbr', 'path', 'circle', 'rect',
        'line', 'polyline', 'polygon', 'ellipse', 'stop', 'use'}

errors = []
warnings = []


class Checker(HTMLParser):
    def __init__(self, path):
        super().__init__(convert_charrefs=True)
        self.path = path
        self.stack = []
        self.ids = []
        self.labels = []          # (for_value)
        self.inputs = []          # (tag, id, attrs)
        self.links = []
        self.in_svg = 0

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == 'svg':
            self.in_svg += 1
        if not self.in_svg and tag not in VOID:
            self.stack.append(tag)
        if 'id' in a:
            self.ids.append(a['id'])
        if tag == 'label' and 'for' in a:
            self.labels.append(a['for'])
        if tag in ('input', 'select', 'textarea'):
            self.inputs.append((tag, a.get('id'), a))
        if tag == 'a' and 'href' in a:
            self.links.append(a['href'])

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        if tag == 'svg':
            self.in_svg -= 1

    def handle_endtag(self, tag):
        if tag == 'svg':
            self.in_svg = max(0, self.in_svg - 1)
            return
        if self.in_svg or tag in VOID:
            return
        if not self.stack:
            errors.append('%s: stray closing </%s>' % (self.path, tag))
            return
        if self.stack[-1] != tag:
            errors.append('%s: closing </%s> but innermost open tag is <%s>'
                          % (self.path, tag, self.stack[-1]))
            # resync if the tag is open further up
            if tag in self.stack:
                while self.stack and self.stack.pop() != tag:
                    pass
            return
        self.stack.pop()


def all_pages():
    out = []
    for dirpath, dirnames, filenames in os.walk(ROOT):
        if 'build' in dirpath or '.git' in dirpath:
            continue
        for f in filenames:
            if f.endswith('.html'):
                out.append(os.path.join(dirpath, f))
    return sorted(out)


# field ids each calculator's JS module reads (or reads conditionally)
REQUIRED_FIELDS = {
    'bmi': ['heightCm', 'heightFt', 'heightIn', 'weightKg', 'weightLb', 'age'],
    'bmr': ['heightCm', 'weightKg', 'age', 'formula', 'activity', 'bodyFat'],
    'ideal-weight': ['heightCm', 'formula', 'weightKg'],
    'body-fat': ['heightCm', 'neckCm', 'neckIn', 'waistCm', 'waistIn', 'hipCm',
                 'hipIn', 'weightKg', 'age'],
    'calories-burned': ['weightKg', 'activity', 'durationHours', 'durationMinutes'],
    'pace': ['distance', 'timeH', 'timeM', 'timeS', 'paceM', 'paceS'],
    'period': ['lmp', 'cycleLength', 'periodLength'],
    'pregnancy': ['refDate', 'cycleLength'],
    'bra-size': ['underbust', 'bust', 'region'],
}
REQUIRED_RADIOS = {
    'bmi': ['units'], 'bmr': ['units', 'sex'], 'ideal-weight': ['units', 'sex'],
    'body-fat': ['units', 'sex'], 'calories-burned': ['units'],
    'pace': ['solveFor', 'distUnit', 'paceUnit'],
    'period': [], 'pregnancy': ['method'], 'bra-size': ['measureUnit'],
}


def check(path):
    rel_path = os.path.relpath(path, ROOT).replace('\\', '/')
    with open(path, encoding='utf-8') as fh:
        raw = fh.read()

    c = Checker(rel_path)
    c.feed(raw)
    if c.stack:
        errors.append('%s: unclosed tags at end of document: %s' % (rel_path, c.stack))

    # duplicate ids
    seen, dupes = set(), set()
    for i in c.ids:
        if i in seen:
            dupes.add(i)
        seen.add(i)
    if dupes:
        errors.append('%s: duplicate id(s): %s' % (rel_path, sorted(dupes)))

    # every label[for] points at a real id
    for f in c.labels:
        if f not in seen:
            errors.append('%s: <label for="%s"> has no matching element' % (rel_path, f))

    # aria-describedby targets exist
    for m in re.finditer(r'aria-describedby="([^"]+)"', raw):
        for target in m.group(1).split():
            if target not in seen:
                errors.append('%s: aria-describedby="%s" has no matching id' % (rel_path, target))

    # aria-controls targets exist
    for m in re.finditer(r'aria-controls="([^"]+)"', raw):
        if m.group(1) not in seen:
            errors.append('%s: aria-controls="%s" has no matching id' % (rel_path, m.group(1)))

    # every form control has an accessible name
    for tag, fid, a in c.inputs:
        if a.get('type') in ('hidden', 'submit', 'reset'):
            continue
        named = ('aria-label' in a) or (fid and fid in c.labels) or ('aria-labelledby' in a)
        if not named:
            errors.append('%s: <%s id=%s> has no label, aria-label or aria-labelledby'
                          % (rel_path, tag, fid))
        # number inputs that JS validates must have an error box
        if fid and a.get('type') == 'number' and ('%s-error' % fid) not in seen:
            errors.append('%s: input #%s has no #%s-error message container'
                          % (rel_path, fid, fid))

    # internal links resolve
    base_dir = os.path.dirname(path)
    for href in c.links:
        if href.startswith(('http://', 'https://', 'mailto:', 'tel:', '#')):
            continue
        target = href.split('#')[0].split('?')[0]
        if not target:
            continue
        if target.startswith('/'):
            resolved = os.path.join(ROOT, target.lstrip('/'))
        else:
            resolved = os.path.join(base_dir, target)
        if os.path.isdir(resolved):
            resolved = os.path.join(resolved, 'index.html')
        if not os.path.exists(resolved):
            errors.append('%s: broken link -> %s' % (rel_path, href))

    # referenced assets exist
    for m in re.finditer(r'(?:src|href)="((?:\.\./)*assets/[^"]+)"', raw):
        if not os.path.exists(os.path.join(base_dir, m.group(1))):
            errors.append('%s: missing asset -> %s' % (rel_path, m.group(1)))

    # SEO essentials
    for pattern, label in [
        (r'<title>.{10,70}</title>', 'title 10-70 chars'),
        (r'<meta name="description" content="[^"]{70,180}"', 'meta description 70-180 chars'),
        (r'<link rel="canonical"', 'canonical link'),
        (r'<meta property="og:image"', 'og:image'),
        (r'<h1[ >]', 'exactly one h1'),
    ]:
        if not re.search(pattern, raw, re.S):
            warnings.append('%s: %s not found/out of range' % (rel_path, label))
    if raw.count('<h1') != 1:
        errors.append('%s: found %d <h1> elements, expected 1' % (rel_path, raw.count('<h1')))

    # calculator-specific wiring
    m = re.search(r'<body data-calc="([^"]+)"', raw)
    if m:
        slug = m.group(1)
        for fid in REQUIRED_FIELDS.get(slug, []):
            if fid not in seen:
                errors.append('%s: calculator "%s" is missing field #%s' % (rel_path, slug, fid))
        for name in REQUIRED_RADIOS.get(slug, []):
            if ('name="%s"' % name) not in raw:
                errors.append('%s: calculator "%s" is missing radio group "%s"'
                              % (rel_path, slug, name))
        for required_id in ('calc-form', 'result', 'result-placeholder'):
            if required_id not in seen:
                errors.append('%s: missing #%s' % (rel_path, required_id))
        if 'data-show-when' in raw:
            for mm in re.finditer(r'data-show-when="([^:]+):', raw):
                name = mm.group(1)
                if ('name="%s"' % name) not in raw and ('id="%s"' % name) not in raw:
                    errors.append('%s: data-show-when references unknown control "%s"'
                                  % (rel_path, name))


def main():
    pages = all_pages()
    for p in pages:
        check(p)

    print('Checked %d pages.' % len(pages))
    for w in warnings:
        print('  WARN   %s' % w)
    for e in errors:
        print('  ERROR  %s' % e)
    print('\n%d error(s), %d warning(s)' % (len(errors), len(warnings)))
    sys.exit(1 if errors else 0)


if __name__ == '__main__':
    main()
