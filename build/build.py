# -*- coding: utf-8 -*-
"""VitaCalc static site generator.

Writes plain .html files (no runtime dependency on this script). Run with:

    python build/build.py

Change BASE_URL below to your real domain before going live: it is used for
canonical URLs, Open Graph tags, JSON-LD and sitemap.xml.
"""

import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from content import CALCULATORS, CALC_BY_SLUG, DIRECTORY_ORDER, TAG_LABELS

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# --------------------------------------------------------------------------
# Site configuration
# --------------------------------------------------------------------------
BASE_URL = 'https://www.vitacalc.in'          # <- change to your domain
BRAND = 'VitaCalc'
TAGLINE = 'Health calculators that respect your privacy'
ORG = 'VitaCalc'          # legal/publisher name used in JSON-LD and the legal pages
EMAIL = 'hello@vitacalc.in'
LOCALE = 'en_IN'
BUILD_DATE = '2026-09-16'

# --------------------------------------------------------------------------
# Icon set (inline SVG, currentColor)
# --------------------------------------------------------------------------
def _svg(body, stroke=True):
    attrs = ('fill="none" stroke="currentColor" stroke-width="1.9" '
             'stroke-linecap="round" stroke-linejoin="round"') if stroke else 'fill="currentColor"'
    return '<svg viewBox="0 0 24 24" %s aria-hidden="true" focusable="false">%s</svg>' % (attrs, body)


ICONS = {
    'scale': _svg('<path d="M12 3v18"/><path d="M6 7h12"/><path d="M6 7 3 14h6L6 7Z"/>'
                  '<path d="M18 7l-3 7h6l-3-7Z"/><path d="M8 21h8"/>'),
    'flame': _svg('<path d="M12 2c1.5 3.5-1 5-1 7a3 3 0 0 0 6 0c0-1-.4-2-1-3 2.5 1.7 4 4.3 4 7a8 8 0 1 1-16 0c0-4.5 3-7 5-9 1.4-1.4 2.5-2 3-2Z"/>'),
    'target': _svg('<circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="5"/><circle cx="12" cy="12" r="1.4"/>'),
    'body': _svg('<circle cx="12" cy="4.5" r="2.2"/><path d="M12 7v7"/><path d="M7 9.5h10"/>'
                 '<path d="M9.5 21 12 14l2.5 7"/>'),
    'bolt': _svg('<path d="M13 2 4.5 13H11l-1 9 8.5-11H12l1-9Z"/>'),
    'run': _svg('<circle cx="15" cy="4.5" r="2"/><path d="M11.5 21 13 15l-3-2.5 1-5.5 3.5 3 3 .8"/>'
                '<path d="m10 12.5-3.5 2L5 19"/><path d="M14 15.5 17 18l.8 3"/>'),
    'calendar': _svg('<rect x="3" y="5" width="18" height="16" rx="2.5"/><path d="M3 10h18"/>'
                     '<path d="M8 3v4M16 3v4"/><circle cx="12" cy="15" r="1.4"/>'),
    'heart': _svg('<path d="M12 20.5s-7.5-4.7-7.5-10a4.3 4.3 0 0 1 7.5-2.8A4.3 4.3 0 0 1 19.5 10.5c0 5.3-7.5 10-7.5 10Z"/>'),
    'ruler': _svg('<rect x="2" y="8" width="20" height="8" rx="2"/><path d="M6.5 8v3M10 8v4M13.5 8v3M17 8v4"/>'),
    'arrow': _svg('<path d="M5 12h13"/><path d="m12.5 6 6 6-6 6"/>'),
    'check': _svg('<circle cx="12" cy="12" r="9"/><path d="m8.5 12.2 2.4 2.4 4.6-5"/>'),
    'search': _svg('<circle cx="11" cy="11" r="7"/><path d="m20 20-3.6-3.6"/>'),
    'menu': _svg('<path d="M4 7h16M4 12h16M4 17h16"/>'),
    'close': _svg('<path d="M6 6l12 12M18 6 6 18"/>'),
    'shield': _svg('<path d="M12 3 5 6v6c0 4.5 3 7.7 7 9 4-1.3 7-4.5 7-9V6l-7-3Z"/><path d="m9 12 2 2 4-4"/>'),
    'zap': _svg('<path d="M4 14h6l-1 7 11-11h-6l1-7-11 11Z"/>'),
    'phone': _svg('<rect x="6" y="2.5" width="12" height="19" rx="2.5"/><path d="M10.5 18.5h3"/>'),
    'lock': _svg('<rect x="4.5" y="10" width="15" height="10.5" rx="2.5"/>'
                 '<path d="M8 10V7a4 4 0 0 1 8 0v3"/>'),
    'leaf': _svg('<path d="M20 4c0 9-5.5 13-11 13a5 5 0 0 1-5-5C4 6.5 11 4 20 4Z"/><path d="M9 15c2-4 5-6 8-7"/>'),
    'mail': _svg('<rect x="3" y="5" width="18" height="14" rx="2.5"/><path d="m3.5 7 8.5 6 8.5-6"/>'),
    'moon': _svg('<path d="M20 14.5A8.2 8.2 0 0 1 9.5 4 8.3 8.3 0 1 0 20 14.5Z"/>'),
    'sun': _svg('<circle cx="12" cy="12" r="4.2"/><path d="M12 2.6v2M12 19.4v2M2.6 12h2M19.4 12h2'
                'M5.4 5.4l1.4 1.4M17.2 17.2l1.4 1.4M18.6 5.4l-1.4 1.4M6.8 17.2l-1.4 1.4"/>'),
}

# Runs before first paint so a returning dark-mode visitor never sees a white
# flash. Light is the default; the OS preference is deliberately not consulted.
THEME_BOOT = (
    '<script>(function(){try{var t=localStorage.getItem("vitacalc.theme");'
    'if(t!=="dark")t="light";document.documentElement.setAttribute("data-theme",t);'
    'if(t==="dark"){var m=document.getElementById("theme-color");if(m)m.content="#16100D";}'
    '}catch(e){}})();</script>\n'
)

BRAND_MARK = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.3" '
              'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
              '<path d="M3 12.5h3.2l1.8-5 2.8 10.5L14 8l1.6 4.5H21"/></svg>')


# --------------------------------------------------------------------------
# Page shell
# --------------------------------------------------------------------------
def rel(depth, path=''):
    """Relative prefix from a page at `depth` folders deep back to site root."""
    return ('../' * depth) + path


def nav_html(depth, current):
    def link(href, label, key):
        aria = ' aria-current="page"' if current == key else ''
        return '<li><a class="nav__link" href="%s"%s>%s</a></li>' % (rel(depth, href), aria, label)

    return (
        '<nav class="nav" id="site-nav" aria-label="Main">'
        '<ul class="nav__list">'
        + link('index.html', 'Home', 'home')
        + link('calculators/index.html', 'Calculators', 'calculators')
        + link('about/index.html', 'About', 'about')
        + '<li><a class="nav__cta" href="%s">Start calculating %s</a></li>' % (
            rel(depth, 'calculators/index.html'), ICONS['arrow'])
        + '</ul></nav>'
    )


def header_html(depth, current):
    return (
        '<a class="skip-link" href="#main">Skip to main content</a>'
        '<header class="site-header">'
        '<div class="wrap site-header__inner">'
        '<a class="brand" href="%s">'
        '<span class="brand__mark">%s</span><span>Vita<em>Calc</em></span></a>'
        '%s'
        '<button class="theme-toggle" type="button" id="theme-toggle" '
        'aria-label="Switch to dark theme">'
        '<span class="icon-moon">%s</span><span class="icon-sun">%s</span>'
        '</button>'
        '<button class="nav-toggle" type="button" aria-expanded="false" aria-controls="site-nav" '
        'aria-label="Open menu">'
        '<span class="icon-open">%s</span><span class="icon-close">%s</span>'
        '</button>'
        '</div></header>'
    ) % (rel(depth, 'index.html'), BRAND_MARK, nav_html(depth, current),
         ICONS['moon'], ICONS['sun'], ICONS['menu'], ICONS['close'])


def footer_html(depth):
    def calc_links(slugs):
        return ''.join(
            '<li><a href="%s">%s</a></li>' % (
                rel(depth, 'calculators/%s/index.html' % s), CALC_BY_SLUG[s]['h1'])
            for s in slugs)

    return (
        '<footer class="site-footer">'
        '<div class="wrap">'
        '<div class="footer-grid">'

        '<div class="footer-brand">'
        '<a class="brand" href="%(home)s"><span class="brand__mark">%(mark)s</span>'
        '<span>Vita<em>Calc</em></span></a>'
        '<p class="mt-1">Nine health and fitness calculators that run entirely in your browser. '
        'Nothing you type is sent to a server, stored or shared.</p>'
        '<p><a href="mailto:%(email)s">%(email)s</a></p>'
        '</div>'

        '<div><h3>Popular calculators</h3><ul>%(pop)s</ul></div>'
        '<div><h3>More calculators</h3><ul>%(more)s</ul></div>'
        '<div><h3>About</h3><ul>'
        '<li><a href="%(about)s">About VitaCalc</a></li>'
        '<li><a href="%(disc)s">Health disclaimer</a></li>'
        '<li><a href="%(priv)s">Privacy policy</a></li>'
        '<li><a href="%(terms)s">Terms of use</a></li>'
        '</ul></div>'

        '</div>'
        '<div class="footer-bottom">'
        '<p class="mb-0">&copy; <span data-year>2026</span> %(brand)s. All calculations run locally in your browser.</p>'
        '<p class="mb-0">Estimates only &mdash; not medical advice.</p>'
        '</div>'
        '</div></footer>'
    ) % {
        'home': rel(depth, 'index.html'),
        'mark': BRAND_MARK,
        'email': EMAIL,
        'pop': calc_links(['bmi', 'bmr', 'calories-burned', 'body-fat', 'pace']),
        'more': calc_links(['ideal-weight', 'period', 'pregnancy', 'bra-size']),
        'about': rel(depth, 'about/index.html'),
        'disc': rel(depth, 'disclaimer/index.html'),
        'priv': rel(depth, 'privacy/index.html'),
        'terms': rel(depth, 'terms/index.html'),
        'brand': BRAND,
    }


def page(path, depth, title, description, body, current='', canonical='',
         jsonld=None, og_image='assets/img/og-default.png', noindex=False):
    """Writes one HTML file and returns its canonical URL."""
    canonical_url = BASE_URL + '/' + canonical
    ld = ''
    if jsonld:
        for block in jsonld:
            ld += '<script type="application/ld+json">%s</script>' % json.dumps(
                block, ensure_ascii=False, separators=(',', ':'))

    html = (
        '<!DOCTYPE html>\n'
        '<html lang="en" data-theme="light">\n<head>\n'
        '<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width, initial-scale=1">\n'
        '<title>%(title)s</title>\n'
        '<meta name="description" content="%(desc)s">\n'
        '<link rel="canonical" href="%(canon)s">\n'
        '<meta name="robots" content="%(robots)s">\n'
        '<meta name="theme-color" content="#FFF8F2" id="theme-color">\n'
        + THEME_BOOT +
        '<meta name="author" content="%(brand)s">\n'
        '<meta property="og:type" content="website">\n'
        '<meta property="og:site_name" content="%(brand)s">\n'
        '<meta property="og:locale" content="%(locale)s">\n'
        '<meta property="og:title" content="%(title)s">\n'
        '<meta property="og:description" content="%(desc)s">\n'
        '<meta property="og:url" content="%(canon)s">\n'
        '<meta property="og:image" content="%(base)s/%(ogimg)s">\n'
        '<meta property="og:image:width" content="1200">\n'
        '<meta property="og:image:height" content="630">\n'
        '<meta name="twitter:card" content="summary_large_image">\n'
        '<meta name="twitter:title" content="%(title)s">\n'
        '<meta name="twitter:description" content="%(desc)s">\n'
        '<meta name="twitter:image" content="%(base)s/%(ogimg)s">\n'
        '<link rel="icon" href="%(root)sassets/img/favicon.svg" type="image/svg+xml">\n'
        '<link rel="apple-touch-icon" href="%(root)sassets/img/apple-touch-icon.png">\n'
        '<link rel="manifest" href="%(root)ssite.webmanifest">\n'
        '<link rel="preconnect" href="https://fonts.googleapis.com">\n'
        '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
        '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;700;800&display=swap" media="print" onload="this.media=\'all\'">\n'
        '<noscript><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;700;800&display=swap"></noscript>\n'
        '<link rel="stylesheet" href="%(root)sassets/css/main.css">\n'
        '%(ld)s\n'
        '</head>\n'
        '<body>\n'
        '%(header)s\n'
        '<main id="main">\n%(body)s\n</main>\n'
        '%(footer)s\n'
        '<script src="%(root)sassets/js/engine.js"></script>\n'
        '<script src="%(root)sassets/js/data.js"></script>\n'
        '<script src="%(root)sassets/js/app.js"></script>\n'
        '</body>\n</html>\n'
    ) % {
        'title': title,
        'desc': description,
        'canon': canonical_url,
        'robots': 'noindex, follow' if noindex else 'index, follow, max-image-preview:large, max-snippet:-1',
        'brand': BRAND,
        'locale': LOCALE,
        'base': BASE_URL,
        'ogimg': og_image,
        'root': rel(depth),
        'ld': ld,
        'header': header_html(depth, current),
        'body': body,
        'footer': footer_html(depth),
    }

    full = os.path.join(ROOT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, 'w', encoding='utf-8') as fh:
        fh.write(html)
    return canonical_url


# --------------------------------------------------------------------------
# Shared fragments
# --------------------------------------------------------------------------
def breadcrumb(depth, trail):
    """trail: list of (label, href_or_None)."""
    items = []
    for label, href in trail:
        if href:
            items.append('<li><a href="%s">%s</a></li>' % (rel(depth, href), label))
        else:
            items.append('<li><span aria-current="page">%s</span></li>' % label)
    return ('<nav class="breadcrumb" aria-label="Breadcrumb"><div class="wrap"><ol>%s</ol></div></nav>'
            % ''.join(items))


def calc_card(slug, depth):
    c = CALC_BY_SLUG[slug]
    return (
        '<a class="calc-card" href="%(href)s" data-keywords="%(kw)s" data-tags="%(tags)s">'
        '<span class="calc-card__icon">%(icon)s</span>'
        '<h3>%(title)s</h3><p>%(blurb)s</p>'
        '<span class="calc-card__go">Open calculator %(arrow)s</span>'
        '</a>'
    ) % {
        'href': rel(depth, 'calculators/%s/index.html' % slug),
        'kw': '%s %s %s' % (c['h1'], c['keywords'], c['blurb']),
        'tags': ' '.join(c['tags']),
        'icon': ICONS[c['icon']],
        'title': c['h1'],
        'blurb': c['blurb'],
        'arrow': ICONS['arrow'],
    }


def faq_html(faqs):
    return '<div class="faq">' + ''.join(
        '<details class="faq-item"><summary>%s</summary>'
        '<div class="faq-body"><p>%s</p></div></details>' % (q, a)
        for q, a in faqs) + '</div>'


def faq_jsonld(faqs):
    return {
        '@context': 'https://schema.org',
        '@type': 'FAQPage',
        'mainEntity': [{
            '@type': 'Question',
            'name': strip_entities(q),
            'acceptedAnswer': {'@type': 'Answer', 'text': strip_entities(a)},
        } for q, a in faqs],
    }


def strip_entities(text):
    repl = {
        '&mdash;': '\u2014', '&ndash;': '\u2013', '&amp;': '&', '&nbsp;': ' ',
        '&rsquo;': '\u2019', '&lsquo;': '\u2018', '&ldquo;': '\u201c', '&rdquo;': '\u201d',
        '&minus;': '\u2212', '&times;': '\u00d7', '&hellip;': '\u2026', '&sup2;': '\u00b2',
        '&deg;': '\u00b0', '&plusmn;': '\u00b1',
    }
    for k, v in repl.items():
        text = text.replace(k, v)
    while '<' in text and '>' in text:
        start = text.index('<')
        end = text.index('>', start)
        text = text[:start] + text[end + 1:]
    return text


def breadcrumb_jsonld(trail):
    """trail: list of (name, absolute_path_or_None)."""
    return {
        '@context': 'https://schema.org',
        '@type': 'BreadcrumbList',
        'itemListElement': [{
            '@type': 'ListItem',
            'position': i + 1,
            'name': strip_entities(name),
            'item': BASE_URL + '/' + path if path else None,
        } for i, (name, path) in enumerate(trail)],
    }


# --------------------------------------------------------------------------
# Pages
# --------------------------------------------------------------------------
def build_home():
    depth = 0
    cards = ''.join(calc_card(s, depth) for s in DIRECTORY_ORDER)

    features = [
        ('lock', 'Nothing leaves your browser',
         'Every formula runs locally in JavaScript. No account, no upload, no tracking of what you enter.'),
        ('zap', 'Answers without a page reload',
         'Results appear instantly under the form, with the working shown so you can check it.'),
        ('phone', 'Built mobile-first',
         'Large tap targets, numeric keypads on number fields and layouts that reflow to one column.'),
        ('shield', 'Formulas cited, not hidden',
         'Each page names the equation it uses, the population it came from and where it breaks down.'),
    ]
    feature_html = ''.join(
        '<div class="feature"><div class="feature__icon">%s</div><h3>%s</h3><p>%s</p></div>'
        % (ICONS[i], t, d) for i, t, d in features)

    body = (
        '<section class="hero"><div class="wrap"><div class="hero__grid">'
        '<div>'
        '<p class="eyebrow"><b>9 tools</b> Fitness &amp; health calculators</p>'
        '<h1>Know your numbers,<br>without handing over your data</h1>'
        '<p class="hero__lede">BMI, BMR, body fat, calories burned, pace, cycle and pregnancy dates '
        '&mdash; nine calculators that work in metric and imperial, explain their own formulas, '
        'and never send a single measurement to a server.</p>'
        '<div class="hero__actions">'
        '<a class="btn btn--primary btn--lg" href="calculators/index.html">Browse all calculators %s</a>'
        '<a class="btn btn--ghost btn--lg" href="calculators/bmi/index.html">Try the BMI calculator</a>'
        '</div>'
        '<ul class="hero__points">'
        '<li>%s<span>Metric and imperial throughout, with your preference remembered</span></li>'
        '<li>%s<span>Every formula named, sourced and explained on the page</span></li>'
        '<li>%s<span>Free, no sign-up, and no health data ever transmitted</span></li>'
        '</ul>'
        '</div>'
        '<div class="hero__card">'
        '<h2>Start with the essentials</h2>'
        '<p class="small">The three people reach for most.</p>'
        '<div class="card-grid" style="grid-template-columns:1fr">%s%s%s</div>'
        '</div>'
        '</div></div></section>'

        '<section class="section"><div class="wrap">'
        '<div class="section__head"><h2>All nine calculators</h2>'
        '<p>Pick a tool, enter a few values and get a clear result with the reasoning behind it.</p></div>'
        '<div class="card-grid">%s</div>'
        '</div></section>'

        '<section class="section section--alt"><div class="wrap">'
        '<div class="section__head"><h2>Why VitaCalc works differently</h2>'
        '<p>Most health calculators exist to collect an email address. These exist to answer a question '
        'and get out of your way.</p></div>'
        '<div class="feature-grid">%s</div>'
        '</div></section>'

        '<section class="section"><div class="wrap">'
        '<div class="cta-band">'
        '<h2>Estimates, honestly labelled</h2>'
        '<p>Every result here is a population-level estimate, not a diagnosis. We show you the formula, '
        'the assumptions behind it and the situations where it stops being reliable &mdash; so you know '
        'exactly how much weight to give the number.</p>'
        '<a class="btn btn--lg" href="disclaimer/index.html">Read our health disclaimer</a>'
        '</div>'
        '</div></section>'
    ) % (ICONS['arrow'], ICONS['check'], ICONS['check'], ICONS['check'],
         calc_card('bmi', depth), calc_card('bmr', depth), calc_card('calories-burned', depth),
         cards, feature_html)

    website = {
        '@context': 'https://schema.org',
        '@type': 'WebSite',
        'name': BRAND,
        'url': BASE_URL + '/',
        'description': strip_entities(
            'Nine free health and fitness calculators &mdash; BMI, BMR, body fat, ideal weight, '
            'calories burned, pace, period, pregnancy and bra size &mdash; that run entirely in your browser.'),
        'publisher': {'@type': 'Organization', 'name': ORG, 'url': BASE_URL + '/'},
        'inLanguage': 'en',
    }
    itemlist = {
        '@context': 'https://schema.org',
        '@type': 'ItemList',
        'name': 'Health and fitness calculators',
        'itemListElement': [{
            '@type': 'ListItem',
            'position': i + 1,
            'name': strip_entities(CALC_BY_SLUG[s]['h1']),
            'url': '%s/calculators/%s/' % (BASE_URL, s),
        } for i, s in enumerate(DIRECTORY_ORDER)],
    }

    page('index.html', depth,
         title='%s &mdash; Free Health &amp; Fitness Calculators' % BRAND,
         description='Nine free health calculators: BMI, BMR, body fat, ideal weight, calories '
                     'burned, pace, period and pregnancy. Metric and imperial, no sign-up, run '
                     'privately in your browser.',
         body=body, current='home', canonical='', jsonld=[website, itemlist])


def build_directory():
    depth = 1
    chips = ''.join(
        '<button class="chip" type="button" data-tag="%s" aria-pressed="%s">%s</button>'
        % (tag, 'true' if tag == 'all' else 'false', label)
        for tag, label in TAG_LABELS)

    body = (
        breadcrumb(depth, [('Home', 'index.html'), ('Calculators', None)])
        + '<section class="section" style="padding-top:26px"><div class="wrap">'
        '<div class="section__head">'
        '<h1>Health &amp; fitness calculators</h1>'
        '<p>All nine tools in one place. Search by name or filter by category &mdash; every one works '
        'in metric and imperial and runs entirely in your browser.</p>'
        '</div>'
        '<div class="search-bar">%s'
        '<label class="visually-hidden" for="calc-search">Search calculators</label>'
        '<input class="input" type="search" id="calc-search" placeholder="Search calculators, e.g. body fat" '
        'autocomplete="off">'
        '</div>'
        '<div class="filter-chips" role="group" aria-label="Filter by category">%s</div>'
        '<div class="card-grid mt-3" id="calc-grid">%s</div>'
        '<p class="empty-state" id="calc-empty">No calculator matches that search. Try a different term.</p>'
        '</div></section>'

        '<section class="section section--alt"><div class="wrap">'
        '<div class="section__head"><h2>Which one should I use?</h2>'
        '<p>A short guide to picking the right tool.</p></div>'
        '<div class="feature-grid">'
        '<div class="feature"><div class="feature__icon">%s</div><h3>Checking your weight</h3>'
        '<p>Start with <a href="bmi/index.html">BMI</a> for a quick screen, then '
        '<a href="body-fat/index.html">body fat</a> for what that weight is actually made of. '
        '<a href="ideal-weight/index.html">Ideal weight</a> adds clinical reference figures.</p></div>'
        '<div class="feature"><div class="feature__icon">%s</div><h3>Managing calories</h3>'
        '<p><a href="bmr/index.html">BMR</a> gives your resting burn and daily maintenance calories. '
        '<a href="calories-burned/index.html">Calories burned</a> covers what a specific session adds.</p></div>'
        '<div class="feature"><div class="feature__icon">%s</div><h3>Training for a race</h3>'
        '<p><a href="pace/index.html">Pace</a> solves for pace, finish time or distance and prints '
        'split times for every standard race distance.</p></div>'
        '<div class="feature"><div class="feature__icon">%s</div><h3>Cycle and pregnancy</h3>'
        '<p><a href="period/index.html">Period</a> projects six cycles ahead. '
        '<a href="pregnancy/index.html">Pregnancy</a> dates a due date and gestational age. '
        '<a href="bra-size/index.html">Bra size</a> converts across four sizing systems.</p></div>'
        '</div></div></section>'
    ) % (ICONS['search'], chips,
         ''.join(calc_card(s, depth) for s in DIRECTORY_ORDER),
         ICONS['scale'], ICONS['flame'], ICONS['run'], ICONS['heart'])

    itemlist = {
        '@context': 'https://schema.org',
        '@type': 'ItemList',
        'name': 'All VitaCalc health calculators',
        'numberOfItems': len(DIRECTORY_ORDER),
        'itemListElement': [{
            '@type': 'ListItem',
            'position': i + 1,
            'name': strip_entities(CALC_BY_SLUG[s]['h1']),
            'description': strip_entities(CALC_BY_SLUG[s]['blurb']),
            'url': '%s/calculators/%s/' % (BASE_URL, s),
        } for i, s in enumerate(DIRECTORY_ORDER)],
    }
    crumbs = breadcrumb_jsonld([('Home', ''), ('Calculators', 'calculators/')])

    page('calculators/index.html', depth,
         title='All Health Calculators | %s' % BRAND,
         description='Browse all nine VitaCalc health and fitness calculators: BMI, BMR, ideal weight, '
                     'body fat, calories burned, running pace, period, pregnancy and bra size.',
         body=body, current='calculators', canonical='calculators/',
         jsonld=[itemlist, crumbs])


def build_calculator(c):
    depth = 2
    slug = c['slug']
    others = [s for s in DIRECTORY_ORDER if s != slug][:5]

    side = (
        '<aside class="calc-layout__side">'
        '<div class="side-card">'
        '<h2>Your result</h2>'
        '<div id="result" class="result" role="region" aria-live="polite" aria-label="Calculation result"></div>'
        '<p class="panel__note" id="result-placeholder">Fill in the form and select '
        '<strong>%(cta)s</strong> &mdash; your result appears here without the page reloading.</p>'
        '</div>'
        '<div class="side-card">'
        '<h2>Other calculators</h2>'
        '<ul class="link-list">%(links)s</ul>'
        '</div>'
        '</aside>'
    ) % {
        'cta': 'Calculate',
        'links': ''.join(
            '<li><a href="%s">%s%s</a></li>' % (
                rel(depth, 'calculators/%s/index.html' % s),
                ICONS[CALC_BY_SLUG[s]['icon']], CALC_BY_SLUG[s]['h1'])
            for s in others) +
        '<li><a href="%s">%sAll nine calculators</a></li>' % (
            rel(depth, 'calculators/index.html'), ICONS['arrow']),
    }

    body = (
        breadcrumb(depth, [('Home', 'index.html'), ('Calculators', 'calculators/index.html'), (c['nav'], None)])
        + '<div class="wrap">'
        '<div class="calc-head"><h1>%(h1)s</h1><p>%(intro)s</p></div>'
        '<div class="calc-layout">'
        '<form class="panel calc-layout__form" id="calc-form" novalidate>'
        '<h2>%(form_title)s</h2>'
        '%(form)s'
        '</form>'

        '%(side)s'

        '<div class="calc-layout__content">'
        '<article class="panel prose">'
        '<h2>%(method_title)s</h2>'
        '%(method)s'
        '</article>'

        '<section class="panel">'
        '<h2>Frequently asked questions</h2>'
        '%(faq)s'
        '</section>'

        '<section class="panel">'
        '<h2>Related calculators</h2>'
        '<div class="card-grid" style="grid-template-columns:repeat(auto-fill,minmax(230px,1fr))">%(related)s</div>'
        '</section>'
        '</div>'
        '</div></div>'
    ) % {
        'h1': c['h1'],
        'intro': c['intro'],
        'form_title': c['form_title'],
        'form': c['form'],
        'method_title': c['method_title'],
        'method': c['method'],
        'faq': faq_html(c['faqs']),
        'related': ''.join(calc_card(s, depth) for s in others[:3]),
        'side': side,
    }

    app = {
        '@context': 'https://schema.org',
        '@type': 'WebApplication',
        'name': strip_entities(c['h1']),
        'url': '%s/calculators/%s/' % (BASE_URL, slug),
        'description': strip_entities(c['meta_desc']),
        'applicationCategory': 'HealthApplication',
        'operatingSystem': 'Any (web browser)',
        'browserRequirements': 'Requires JavaScript',
        'isAccessibleForFree': True,
        'offers': {'@type': 'Offer', 'price': '0', 'priceCurrency': 'INR'},
        'publisher': {'@type': 'Organization', 'name': ORG, 'url': BASE_URL + '/'},
    }
    crumbs = breadcrumb_jsonld([
        ('Home', ''), ('Calculators', 'calculators/'),
        (strip_entities(c['h1']), 'calculators/%s/' % slug)])

    path = 'calculators/%s/index.html' % slug
    page(path, depth,
         title='%s | %s' % (c['meta_title'], BRAND),
         description=c['meta_desc'],
         body=body, current='calculators', canonical='calculators/%s/' % slug,
         jsonld=[app, faq_jsonld(c['faqs']), crumbs],
         og_image='assets/img/og-%s.png' % slug)

    # data-calc drives which engine module app.js runs
    full = os.path.join(ROOT, path)
    with open(full, 'r', encoding='utf-8') as fh:
        text = fh.read()
    text = text.replace('<body>', '<body data-calc="%s">' % slug, 1)
    with open(full, 'w', encoding='utf-8') as fh:
        fh.write(text)


# --------------------------------------------------------------------------
# Static content pages
# --------------------------------------------------------------------------
def simple_page(path, slug, title, meta_title, meta_desc, prose, nav_current=''):
    depth = 1
    body = (
        breadcrumb(depth, [('Home', 'index.html'), (title, None)])
        + '<section class="section" style="padding-top:26px"><div class="wrap">'
        '<article class="panel prose prose--page">'
        '<h1>%s</h1>%s'
        '<p class="disclaimer-note">Last updated: %s</p>'
        '</article></div></section>'
    ) % (title, prose, BUILD_DATE)
    page(path, depth, title='%s | %s' % (meta_title, BRAND), description=meta_desc,
         body=body, current=nav_current, canonical=slug + '/')


def build_static_pages():
    simple_page(
        'about/index.html', 'about', 'About VitaCalc',
        'About VitaCalc &mdash; Who Builds These Calculators',
        'VitaCalc is a set of nine free health and fitness calculators. Learn how the '
        'calculations work, where the formulas come from and how your data is handled.',
        '''
<p>VitaCalc is a small, deliberately unambitious website: nine health and fitness calculators, each on its own page, each doing one thing properly.</p>

<h2>Why we built it</h2>
<p>Health calculators on the open web tend to share three problems. They hide the formula, so you cannot tell whether the number means anything. They present estimates as facts, with no indication of the error bars. And an increasing number exist mainly to capture an email address or feed an advertising profile with data about your body.</p>
<p>We wanted the opposite of that. Every calculator here names the equation it uses, tells you what population it was derived from, and is explicit about where it stops being reliable. Nothing you type is transmitted anywhere.</p>

<h2>How the calculations work</h2>
<p>All nine calculators run as JavaScript in your browser. The formulas live in a single calculation module, kept deliberately separate from the interface code, so that each one is a pure function that can be tested against published reference values. Unit conversion happens before calculation &mdash; every formula receives canonical metric values regardless of which unit system you chose &mdash; and results are converted back for display.</p>
<p>Rounding is applied once, at the display step. Intermediate values keep full precision, so you will not see drift from rounding partway through.</p>

<h2>Where the formulas come from</h2>
<ul>
  <li><strong>BMI</strong> &mdash; World Health Organization adult classification</li>
  <li><strong>BMR</strong> &mdash; Mifflin-St Jeor (1990), revised Harris-Benedict (Roza &amp; Shizgal, 1984), Katch-McArdle</li>
  <li><strong>Ideal weight</strong> &mdash; Devine (1974), Robinson (1983), Miller (1983), Hamwi (1964)</li>
  <li><strong>Body fat</strong> &mdash; US Navy circumference method; Deurenberg BMI equation as cross-check</li>
  <li><strong>Calories burned</strong> &mdash; Compendium of Physical Activities (Ainsworth et al., 2011)</li>
  <li><strong>Pregnancy</strong> &mdash; Naegele&rsquo;s rule with cycle-length adjustment</li>
  <li><strong>Period</strong> &mdash; last menstrual period with a 14-day luteal phase assumption</li>
  <li><strong>Bra size</strong> &mdash; region-specific band and cup conventions held in a data table</li>
</ul>

<h2>What this site is not</h2>
<p>It is not a medical service, and nothing on it is a diagnosis or personalised advice. Every formula here is a population-level estimate. Estimates are useful &mdash; they give you a reference point and let you track change over time &mdash; but they describe averages, and you are not an average. Please read the <a href="../disclaimer/index.html">health disclaimer</a>, and take anything that concerns you to a qualified clinician.</p>

<h2>Corrections</h2>
<p>If you find a formula implemented incorrectly, a threshold that is out of date, or a result that disagrees with an authoritative source, we would genuinely like to know. Write to <a href="mailto:%(email)s">%(email)s</a> with the inputs you used and what you expected.</p>
''' % {'email': EMAIL},
        nav_current='about')

    simple_page(
        'disclaimer/index.html', 'disclaimer', 'Health disclaimer',
        'Health Disclaimer &mdash; Estimates, Not Medical Advice',
        'VitaCalc calculators provide general estimates for information only. They are not a diagnosis, '
        'not a treatment plan and not a substitute for professional medical advice.',
        '''
<p><strong>The calculators on this site provide general estimates for informational purposes only. They are not medical advice, not a diagnosis, and not a substitute for consultation with a qualified healthcare professional.</strong></p>

<h2>What an estimate means here</h2>
<p>Every formula on this site was derived from measurements of a group of people and fitted to describe that group on average. Applied to one individual, it carries error &mdash; often more than people expect:</p>
<ul>
  <li>BMR prediction equations are typically within about 10%% of lab-measured resting metabolism, meaning a 1,600 kcal estimate could plausibly be 1,440 or 1,760.</li>
  <li>Circumference-based body fat estimates carry a standard error of roughly 3 to 4 percentage points against DEXA.</li>
  <li>MET-based calorie estimates commonly differ from measured expenditure by 15 to 25%% for an individual.</li>
  <li>Around 4%% of babies are born on their calculated due date; about 80%% arrive within two weeks either side.</li>
  <li>Ovulation timing varies between cycles even for people with regular periods, so predicted fertile windows are probabilities, not certainties.</li>
</ul>

<h2>Do not use these tools to</h2>
<ul>
  <li>Diagnose, treat, cure or prevent any disease or condition.</li>
  <li>Prevent pregnancy. Calendar-based cycle prediction is not a contraceptive method.</li>
  <li>Make clinical decisions, including medication dosing, even though some formulas here originated in clinical dosing contexts.</li>
  <li>Replace ultrasound dating or any assessment your clinician has made. Their date takes precedence over ours.</li>
  <li>Justify extreme dieting, extreme training or any rapid change in body weight.</li>
</ul>

<h2>Please seek professional advice if</h2>
<ul>
  <li>You are pregnant, trying to conceive, or breastfeeding.</li>
  <li>You have diabetes, thyroid disease, heart or kidney disease, PCOS, an eating disorder, or any chronic condition.</li>
  <li>You take medication that affects weight, appetite, fluid balance or metabolism.</li>
  <li>You are planning a significant change to diet or exercise.</li>
  <li>A result concerns you, or a symptom is troubling you &mdash; regardless of what any calculator says.</li>
  <li>You are calculating on behalf of a child or teenager. Adult thresholds do not apply under 20.</li>
</ul>

<h2>Accuracy and liability</h2>
<p>We implement published formulas carefully and verify them against reference values, but we make no warranty that results are accurate, complete or fit for any particular purpose. To the maximum extent permitted by law, %(org)s accepts no liability for any loss or harm arising from use of, or reliance on, this website. Use it at your own discretion.</p>

<h2>In an emergency</h2>
<p>Do not use this website. Contact your local emergency number or go to the nearest emergency department immediately.</p>
''' % {'org': ORG},
        nav_current='')

    simple_page(
        'privacy/index.html', 'privacy', 'Privacy policy',
        'Privacy Policy &mdash; Health Data Stays Local',
        'VitaCalc privacy policy. All calculations run client-side in your browser. We do not collect, '
        'transmit or store the health measurements you enter.',
        '''
<p>The short version: <strong>everything you type into a calculator on this site stays in your browser.</strong> It is not sent to a server, not stored in an account, and not shared with anyone.</p>

<h2>What we do not collect</h2>
<p>We do not collect your height, weight, age, sex, body measurements, activity, menstrual cycle dates, pregnancy dates or any other value you enter into a calculator. This is not a policy promise we ask you to take on faith &mdash; it is a consequence of how the site is built. Each calculator is JavaScript running on your own device. There is no form submission, no API call and no analytics event carrying your inputs. You can verify this yourself: open your browser&rsquo;s developer tools, switch to the Network tab, and run any calculation. No request is made.</p>

<h2>What is stored on your device</h2>
<p>One item, and only if you change it: your preferred unit system (metric or imperial) is saved in your browser&rsquo;s <code>localStorage</code> under the key <code>vitacalc.units</code>, so you do not have to reselect it on every page. It contains the single word <code>metric</code> or <code>imperial</code>, never a measurement. It never leaves your device, and clearing your browser data removes it.</p>
<p>We set no cookies.</p>

<h2>Third-party requests</h2>
<p>The site loads its typeface from Google Fonts. That request tells Google your IP address and browser, as any request for a web resource does. It carries nothing about what you calculated. If you prefer to avoid it entirely, the site remains fully functional with a system font when that request is blocked.</p>
<p>Your web host may keep standard server access logs &mdash; IP address, timestamp, page requested, user agent. These are generated by the act of requesting a page and contain no calculator inputs.</p>

<h2>What we do not do</h2>
<ul>
  <li>No accounts, no sign-up, no email collection.</li>
  <li>No advertising networks and no advertising or tracking pixels.</li>
  <li>No selling, renting or sharing of data, because there is none to share.</li>
  <li>No behavioural profiling or cross-site tracking.</li>
</ul>

<h2>Children</h2>
<p>This site is not directed at children under 13 and we knowingly collect no personal information from anyone. Adult calculator thresholds should not be applied to children in any case &mdash; see the <a href="../disclaimer/index.html">health disclaimer</a>.</p>

<h2>Your rights</h2>
<p>Data protection law gives you rights of access, correction and erasure over personal data a service holds about you. Since we hold none, there is nothing to request &mdash; but if you believe otherwise, write to <a href="mailto:%(email)s">%(email)s</a> and we will respond.</p>

<h2>Changes to this policy</h2>
<p>If this site ever adds a feature that requires transmitting data &mdash; saved history, for example &mdash; it will be opt-in, clearly marked at the point of use, and this policy will be updated before the feature ships.</p>
''' % {'email': EMAIL},
        nav_current='')

    simple_page(
        'terms/index.html', 'terms', 'Terms of use',
        'Terms of Use',
        'Terms of use for VitaCalc, a free set of health and fitness calculators provided for '
        'informational purposes only.',
        '''
<p>By using this website you agree to these terms. If you do not agree with them, please do not use the site.</p>

<h2>1. What this service is</h2>
<p>%(brand)s provides free health and fitness calculators for general informational and educational use. It is not a medical device, not a medical service, and not a provider of healthcare. Nothing on this site creates a doctor&ndash;patient relationship.</p>

<h2>2. Informational use only</h2>
<p>All results are estimates produced by published formulas applied to the values you enter. They are not diagnoses, prescriptions, treatment plans or individualised advice. Please read the <a href="../disclaimer/index.html">health disclaimer</a> in full &mdash; it forms part of these terms.</p>

<h2>3. Your responsibilities</h2>
<ul>
  <li>Enter accurate values. Results are only as good as the inputs and the measurement technique behind them.</li>
  <li>Use results as one input among many, alongside professional advice.</li>
  <li>Do not rely on cycle or pregnancy calculators for contraception or for clinical decisions.</li>
  <li>Do not use this site in a medical emergency.</li>
</ul>

<h2>4. No warranty</h2>
<p>The site is provided &ldquo;as is&rdquo; and &ldquo;as available&rdquo;, without warranties of any kind, express or implied, including fitness for a particular purpose, accuracy or uninterrupted availability. We may change, suspend or withdraw any part of the site at any time without notice.</p>

<h2>5. Limitation of liability</h2>
<p>To the maximum extent permitted by law, %(org)s and its contributors are not liable for any direct, indirect, incidental, consequential or special loss arising from your use of, or inability to use, this website or any result it produces.</p>

<h2>6. Intellectual property</h2>
<p>The design, code, written explanations and branding of this site are the property of %(org)s. The underlying formulas are published scientific work in the public domain and are attributed on the relevant pages. You may use results for your own personal purposes. Republishing substantial portions of the site&rsquo;s content or code without permission is not permitted.</p>

<h2>7. External links</h2>
<p>Where we link to external resources, we do not control them and are not responsible for their content, accuracy or privacy practices.</p>

<h2>8. Governing law</h2>
<p>These terms are governed by the laws of India, and the courts of India have exclusive jurisdiction over any dispute arising from them.</p>

<h2>9. Contact</h2>
<p>Questions about these terms: <a href="mailto:%(email)s">%(email)s</a>.</p>
''' % {'brand': BRAND, 'org': ORG, 'email': EMAIL},
        nav_current='')

    # 404
    depth = 0
    body = (
        '<section class="section"><div class="wrap" style="text-align:center;max-width:620px">'
        '<p class="eyebrow"><b>404</b> Page not found</p>'
        '<h1>That page has moved on</h1>'
        '<p class="hero__lede" style="margin-inline:auto">The address you followed does not exist here. '
        'All nine calculators are one click away.</p>'
        '<div class="hero__actions" style="justify-content:center">'
        '<a class="btn btn--primary btn--lg" href="/calculators/">Browse all calculators</a>'
        '<a class="btn btn--ghost btn--lg" href="/">Back to home</a>'
        '</div></div></section>'
    )
    page('404.html', depth, title='Page not found | %s' % BRAND,
         description='That page does not exist on VitaCalc. Browse all nine health and fitness '
                     'calculators, or head back to the home page.',
         body=body, canonical='404.html', noindex=True)


# --------------------------------------------------------------------------
# Assets: favicon, OG images, manifest, sitemap, robots
# --------------------------------------------------------------------------
def build_favicon():
    svg = (
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64">'
        '<defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1">'
        '<stop offset="0" stop-color="#F2683C"/><stop offset="1" stop-color="#FF9A6B"/>'
        '</linearGradient></defs>'
        '<rect width="64" height="64" rx="16" fill="url(#g)"/>'
        '<path d="M8 34h8.5l4.8-13 7.5 28L37 21l4.3 13H56" fill="none" stroke="#fff" '
        'stroke-width="5.5" stroke-linecap="round" stroke-linejoin="round"/>'
        '</svg>'
    )
    path = os.path.join(ROOT, 'assets', 'img', 'favicon.svg')
    with open(path, 'w', encoding='utf-8') as fh:
        fh.write(svg)


def _font(size, bold=True):
    from PIL import ImageFont
    candidates = [
        r'C:\Windows\Fonts\seguibl.ttf' if bold else r'C:\Windows\Fonts\segoeui.ttf',
        r'C:\Windows\Fonts\segoeuib.ttf' if bold else r'C:\Windows\Fonts\segoeui.ttf',
        r'C:\Windows\Fonts\arialbd.ttf' if bold else r'C:\Windows\Fonts\arial.ttf',
    ]
    for c in candidates:
        if os.path.exists(c):
            try:
                return ImageFont.truetype(c, size)
            except Exception:
                continue
    return ImageFont.load_default()


def _wrap(draw, text, font, max_width):
    words = text.split()
    lines, line = [], ''
    for w in words:
        trial = (line + ' ' + w).strip()
        if draw.textlength(trial, font=font) <= max_width:
            line = trial
        else:
            if line:
                lines.append(line)
            line = w
    if line:
        lines.append(line)
    return lines


def _og_image(out_path, headline, subline):
    from PIL import Image, ImageDraw
    W, H = 1200, 630
    img = Image.new('RGB', (W, H), '#FFF8F2')
    d = ImageDraw.Draw(img)

    # Warm corner wash
    for i in range(320):
        t = i / 320.0
        r = int(255 - 8 * t)
        g = int(210 + 30 * t)
        b = int(180 + 50 * t)
        d.ellipse([W - 520 + i * 0.6, -300 + i * 0.5, W + 200 - i * 0.4, 340 - i * 0.55],
                  fill=(r, g, b))

    # Brand mark
    d.rounded_rectangle([80, 70, 152, 142], radius=20, fill='#F2683C')
    d.line([(96, 108), (110, 108), (117, 88), (128, 128), (135, 100), (140, 108)],
           fill='#FFFFFF', width=6, joint='curve')
    d.text((170, 84), 'VitaCalc', font=_font(42), fill='#2B1B12')

    headline_font = _font(70)
    lines = _wrap(d, headline, headline_font, W - 160)
    y = 250 - (len(lines) - 1) * 40
    for ln in lines:
        d.text((80, y), ln, font=headline_font, fill='#2B1B12')
        y += 86

    sub_font = _font(34, bold=False)
    for ln in _wrap(d, subline, sub_font, W - 200)[:2]:
        d.text((80, y + 14), ln, font=sub_font, fill='#7A6558')
        y += 46

    badge_font = _font(26)
    badge_text = 'Free  \u00b7  No sign-up  \u00b7  Private'
    badge_w = d.textlength(badge_text, font=badge_font)
    d.rounded_rectangle([80, H - 112, 80 + badge_w + 64, H - 44], radius=34, fill='#F2683C')
    d.text((112, H - 92), badge_text, font=badge_font, fill='#FFFFFF', anchor='lm')

    img.save(out_path, 'PNG', optimize=True)


def build_images():
    img_dir = os.path.join(ROOT, 'assets', 'img')
    os.makedirs(img_dir, exist_ok=True)
    try:
        _og_image(os.path.join(img_dir, 'og-default.png'),
                  'Health calculators that respect your privacy',
                  'BMI, BMR, body fat, calories burned, pace, period and pregnancy '
                  '\u2014 all calculated in your browser.')
        for c in CALCULATORS:
            _og_image(os.path.join(img_dir, 'og-%s.png' % c['slug']),
                      strip_entities(c['h1']),
                      strip_entities(c['blurb']))

        # Apple touch icon
        from PIL import Image, ImageDraw
        icon = Image.new('RGB', (180, 180), '#F2683C')
        di = ImageDraw.Draw(icon)
        di.line([(24, 96), (52, 96), (70, 52), (98, 140), (118, 68), (132, 96), (156, 96)],
                fill='#FFFFFF', width=13, joint='curve')
        icon.save(os.path.join(img_dir, 'apple-touch-icon.png'), 'PNG', optimize=True)
        return True
    except Exception as exc:  # Pillow missing or font unavailable
        print('  ! image generation skipped: %s' % exc)
        return False


def build_manifest():
    manifest = {
        'name': '%s \u2014 Health Calculators' % BRAND,
        'short_name': BRAND,
        'description': strip_entities(TAGLINE),
        'start_url': '/',
        'display': 'standalone',
        'background_color': '#FFF8F2',
        'theme_color': '#F2683C',
        'icons': [
            {'src': '/assets/img/favicon.svg', 'sizes': 'any', 'type': 'image/svg+xml'},
            {'src': '/assets/img/apple-touch-icon.png', 'sizes': '180x180', 'type': 'image/png'},
        ],
    }
    with open(os.path.join(ROOT, 'site.webmanifest'), 'w', encoding='utf-8') as fh:
        json.dump(manifest, fh, ensure_ascii=False, indent=2)


def build_sitemap():
    urls = [('', '1.0', 'monthly'), ('calculators/', '0.9', 'monthly')]
    urls += [('calculators/%s/' % s, '0.8', 'monthly') for s in DIRECTORY_ORDER]
    urls += [('about/', '0.4', 'yearly'), ('disclaimer/', '0.4', 'yearly'),
             ('privacy/', '0.3', 'yearly'), ('terms/', '0.3', 'yearly')]

    xml = ['<?xml version="1.0" encoding="UTF-8"?>',
           '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for path, priority, freq in urls:
        xml.append('  <url>')
        xml.append('    <loc>%s/%s</loc>' % (BASE_URL, path))
        xml.append('    <lastmod>%s</lastmod>' % BUILD_DATE)
        xml.append('    <changefreq>%s</changefreq>' % freq)
        xml.append('    <priority>%s</priority>' % priority)
        xml.append('  </url>')
    xml.append('</urlset>')
    with open(os.path.join(ROOT, 'sitemap.xml'), 'w', encoding='utf-8') as fh:
        fh.write('\n'.join(xml) + '\n')

    robots = (
        'User-agent: *\n'
        'Allow: /\n'
        '\n'
        '# No crawlable parameters or private areas exist on this site.\n'
        'Sitemap: %s/sitemap.xml\n'
    ) % BASE_URL
    with open(os.path.join(ROOT, 'robots.txt'), 'w', encoding='utf-8') as fh:
        fh.write(robots)


# --------------------------------------------------------------------------
def main():
    print('Building %s -> %s' % (BRAND, ROOT))
    build_home()
    print('  index.html')
    build_directory()
    print('  calculators/index.html')
    for c in CALCULATORS:
        build_calculator(c)
        print('  calculators/%s/index.html' % c['slug'])
    build_static_pages()
    print('  about/, disclaimer/, privacy/, terms/, 404.html')
    build_favicon()
    build_images()
    build_manifest()
    build_sitemap()
    print('  assets/img/*, site.webmanifest, sitemap.xml, robots.txt')
    print('Done. %d pages.' % (len(CALCULATORS) + 7))


if __name__ == '__main__':
    main()
