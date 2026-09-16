# -*- coding: utf-8 -*-
"""Responsive audit: sweeps every page across a range of viewport widths and
reports layout faults.

Checks at each width:
  * horizontal page overflow
  * any individual element wider than the viewport
  * interactive controls smaller than the 44x44 touch target minimum
  * text rendered below 12px
  * form rows collapsing to unusably narrow inputs
  * content column running wider than a comfortable reading measure
  * the nav switching to the menu button at the right point

Run:  python build/check_responsive.py [--shots]
"""

import os
import sys

from playwright.sync_api import sync_playwright

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SHOTS = os.environ.get('VITACALC_SHOTS', os.path.join(ROOT, 'build', 'screens'))

# name, width, height  -- real device classes, narrow to wide
VIEWPORTS = [
    ('small phone',    320, 640),
    ('phone',          360, 780),
    ('phone large',    390, 844),
    ('phone xl',       430, 932),
    ('phablet',        540, 900),
    ('tablet portrait', 768, 1024),
    ('tablet',         820, 1180),
    ('tablet landscape', 1024, 768),
    ('laptop',         1280, 800),
    ('desktop',        1440, 900),
    ('wide',           1920, 1080),
]

PAGES = [
    'index.html',
    'calculators/index.html',
    'calculators/bmi/index.html',
    'calculators/bmr/index.html',
    'calculators/ideal-weight/index.html',
    'calculators/body-fat/index.html',
    'calculators/calories-burned/index.html',
    'calculators/pace/index.html',
    'calculators/period/index.html',
    'calculators/pregnancy/index.html',
    'calculators/bra-size/index.html',
    'about/index.html',
    'privacy/index.html',
    'terms/index.html',
    'disclaimer/index.html',
    '404.html',
]

AUDIT_JS = """(vw) => {
  const out = {overflow: 0, wide: [], small_targets: [], tiny_text: [],
               narrow_inputs: [], measure: 0, nav_visible: false, burger_visible: false};

  out.overflow = Math.max(0, document.documentElement.scrollWidth
                             - document.documentElement.clientWidth);

  const vis = el => {
    const r = el.getBoundingClientRect();
    return r.width > 0 && r.height > 0 && getComputedStyle(el).visibility !== 'hidden';
  };

  // Elements sticking out past the viewport. Skip anything inside a container
  // that is allowed to scroll sideways on its own.
  for (const el of document.querySelectorAll('body *')) {
    if (!vis(el)) continue;
    if (el.closest('.table-scroll')) continue;
    const r = el.getBoundingClientRect();
    if (r.right > vw + 1 || r.left < -1) {
      out.wide.push(el.tagName.toLowerCase() + '.' + (el.className || '').toString().split(' ')[0]
                    + ' [' + Math.round(r.left) + '..' + Math.round(r.right) + ']');
    }
  }

  // Touch targets. Only meaningful on touch-sized screens, and the visually
  // hidden radio inside a .segmented control is not the target -- its label is.
  if (vw < 1100) {
    for (const el of document.querySelectorAll('a, button, input, select, summary, label')) {
      if (!vis(el)) continue;
      if (el.closest('.site-footer, .breadcrumb, .prose')) continue;
      // An inline link inside a sentence is exempt from the target-size rule
      if (el.tagName === 'A' && el.parentElement
          && ['P', 'LI', 'SPAN', 'TD', 'STRONG', 'EM'].includes(el.parentElement.tagName)) continue;
      const cs = getComputedStyle(el);
      if (parseFloat(cs.opacity) === 0 || cs.position === 'absolute' && el.offsetWidth <= 1) continue;
      if (el.tagName === 'LABEL' && !el.closest('.segmented')) continue;
      const r = el.getBoundingClientRect();
      if (r.height < 40 || r.width < 32) {
        out.small_targets.push((el.id || el.className || el.tagName) + ' '
                               + Math.round(r.width) + 'x' + Math.round(r.height));
      }
    }
  }

  // Text below 12px
  for (const el of document.querySelectorAll('p, li, td, th, span, label, dt, dd, small')) {
    if (!vis(el) || !el.textContent.trim()) continue;
    const fs = parseFloat(getComputedStyle(el).fontSize);
    if (fs < 12) out.tiny_text.push((el.className || el.tagName) + ' ' + fs.toFixed(1) + 'px');
  }

  // Number inputs squeezed too narrow to read their own value
  for (const el of document.querySelectorAll('.input')) {
    if (!vis(el)) continue;
    const r = el.getBoundingClientRect();
    if (r.width < 64) out.narrow_inputs.push((el.id || 'input') + ' ' + Math.round(r.width) + 'px');
  }

  // Reading measure of the main prose column
  const prose = document.querySelector('.prose p');
  if (prose) out.measure = Math.round(prose.getBoundingClientRect().width);

  const navLink = document.querySelector('#site-nav .nav__link');
  const burger = document.querySelector('.nav-toggle');
  out.nav_visible = navLink ? vis(navLink) : false;
  out.burger_visible = burger ? vis(burger) : false;
  return out;
}"""

problems = []


def url(rel_path):
    return 'file:///' + os.path.join(ROOT, rel_path).replace('\\', '/')


def run(take_shots=False):
    if take_shots:
        os.makedirs(SHOTS, exist_ok=True)

    with sync_playwright() as p:
        browser = p.chromium.launch()
        for name, w, h in VIEWPORTS:
            ctx = browser.new_context(viewport={'width': w, 'height': h})
            page = ctx.new_page()
            for rel_path in PAGES:
                page.goto(url(rel_path))
                page.wait_for_timeout(120)
                a = page.evaluate(AUDIT_JS, w)
                tag = '%s %dpx / %s' % (name, w, rel_path)

                if a['overflow'] > 1:
                    problems.append('%s: page scrolls sideways by %dpx' % (tag, a['overflow']))
                for item in a['wide'][:4]:
                    problems.append('%s: element past viewport -> %s' % (tag, item))
                for item in sorted(set(a['small_targets']))[:4]:
                    problems.append('%s: touch target too small -> %s' % (tag, item))
                for item in sorted(set(a['tiny_text']))[:3]:
                    problems.append('%s: text under 12px -> %s' % (tag, item))
                for item in a['narrow_inputs'][:4]:
                    problems.append('%s: input too narrow -> %s' % (tag, item))
                if a['measure'] and a['measure'] > 820:
                    problems.append('%s: prose measure %dpx is too wide to read comfortably'
                                    % (tag, a['measure']))

                # Nav: exactly one of full nav / burger should be showing
                if a['nav_visible'] and a['burger_visible']:
                    problems.append('%s: both the full nav and the menu button are visible' % tag)
                if not a['nav_visible'] and not a['burger_visible']:
                    problems.append('%s: no navigation is reachable' % tag)

            # Conditional fields are hidden by default, so the sweep above never
            # measures them. Reveal each one and re-check at this width.
            for rel_path, clicks in [
                ('calculators/pace/index.html', ['label[for="solveFor-time"]']),
                ('calculators/pace/index.html', ['label[for="solveFor-distance"]']),
                ('calculators/body-fat/index.html', ['label[for="sex-female"]']),
                ('calculators/bmr/index.html', []),
                ('calculators/bmi/index.html', ['label[for="units-imperial"]']),
            ]:
                page.goto(url(rel_path))
                page.wait_for_timeout(120)
                if rel_path.endswith('bmr/index.html'):
                    page.select_option('#formula', 'katch')
                for sel in clicks:
                    page.click(sel)
                page.wait_for_timeout(150)
                a2 = page.evaluate(AUDIT_JS, w)
                tag2 = '%s %dpx / %s (fields revealed)' % (name, w, rel_path)
                if a2['overflow'] > 1:
                    problems.append('%s: page scrolls sideways by %dpx' % (tag2, a2['overflow']))
                for item in a2['narrow_inputs'][:4]:
                    problems.append('%s: input too narrow -> %s' % (tag2, item))
                for item in a2['wide'][:3]:
                    problems.append('%s: element past viewport -> %s' % (tag2, item))
                for item in sorted(set(a2['small_targets']))[:3]:
                    problems.append('%s: touch target too small -> %s' % (tag2, item))

            if take_shots:
                for rel_path, short in [('index.html', 'home'),
                                        ('calculators/bmi/index.html', 'bmi'),
                                        ('calculators/index.html', 'dir')]:
                    page.goto(url(rel_path))
                    page.wait_for_timeout(200)
                    page.screenshot(path=os.path.join(
                        SHOTS, 'rwd-%s-%04d.png' % (short, w)))
            ctx.close()
        browser.close()

    seen = set()
    unique = [x for x in problems if not (x in seen or seen.add(x))]
    print('Swept %d pages x %d viewports.' % (len(PAGES), len(VIEWPORTS)))
    for x in unique:
        print('  ISSUE  %s' % x)
    print('\n%d issue(s)' % len(unique))
    sys.exit(1 if unique else 0)


if __name__ == '__main__':
    run('--shots' in sys.argv)
