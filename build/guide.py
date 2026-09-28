# -*- coding: utf-8 -*-
"""Long-form educational articles that sit *below* the calculator on each page.

Nothing in here touches the calculator markup, the form helpers or the
engine. build.py renders three extra blocks per calculator page:

    1. <article class="panel prose"> .. the guide: intro, table of contents
       and a stack of calculator-specific <h2> sections
    2. the existing FAQ accordion, extended with the `faqs` listed here
    3. <section class="panel prose"> .. limitations, when to get professional
       input, and a disclaimer written for that specific subject

Copy lives in the three guide_* modules so each stays readable:

    guide_body.py    bmi, ideal-weight, body-fat
    guide_energy.py  bmr, calories-burned, pace
    guide_womens.py  period, pregnancy, bra-size
"""

INFO_SVG = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" '
            'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false">'
            '<circle cx="12" cy="12" r="9"/><path d="M12 11v5"/><path d="M12 8h.01"/></svg>')

WARN_SVG = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" '
            'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false">'
            '<path d="M10.3 3.9 2.6 17.4A2 2 0 0 0 4.3 20.4h15.4a2 2 0 0 0 1.7-3L13.7 3.9a2 2 0 0 0-3.4 0Z"/>'
            '<path d="M12 9v4"/><path d="M12 17h.01"/></svg>')


def callout(html, warn=False):
    """An aside in the site's existing callout styling."""
    return '<div class="callout%s">%s<div>%s</div></div>' % (
        ' callout--warn' if warn else '', WARN_SVG if warn else INFO_SVG, html)


def fold(sid, heading, body, open_=False):
    """One collapsible section.

    The heading stays a real <h2> inside the <summary>, so the document
    outline and the crawlable content are unchanged -- only the default
    visibility differs. <details> content is in the DOM either way.
    """
    return (
        '<details class="guide-section"%s>'
        '<summary><h2 id="%s">%s</h2></summary>'
        '<div class="guide-section__body">%s</div>'
        '</details>'
    ) % (' open' if open_ else '', sid, heading, body)


def guide(intro, sections, limits, seek_title, seek, disclaimer, faqs=()):
    """Assemble one calculator's educational content.

    intro      HTML paragraphs opening the article
    sections   list of (anchor id, heading text, HTML body)
    limits     HTML for the "Important limitations" section
    seek_title heading for the "when to ask a professional" section
    seek       HTML for that section, or None to leave it out
    disclaimer HTML for the closing callout
    faqs       extra (question, answer) pairs appended to the page FAQ

    Every section renders as a closed <details> block, so the page opens as a
    short list of headings and the visitor expands only what they want. The
    text stays in the DOM either way, so nothing is hidden from a crawler, and
    the collapsed headings double as the contents list.
    """
    folds = ''.join(fold(sid, head, body) for sid, head, body in sections)
    article = intro + folds

    closing = fold('limitations', 'Important limitations', limits)
    if seek:
        closing += fold('professional-input', seek_title, seek)

    # The disclaimer is rendered by build.py in the sidebar, beside the
    # calculator rather than at the foot of the article. On health content it
    # should not be something a visitor has to scroll to the bottom to find.
    disclaimer_card = (
        '<div class="side-card side-card--warn">'
        '<h2 id="disclaimer">%s Disclaimer</h2>%s'
        '</div>'
    ) % (WARN_SVG, disclaimer)

    # `intro` and `folds` are exposed separately so build.py can slot the
    # calculator's own methodology fold between them, keeping every fold on
    # the page inside a single card instead of nesting one card in another.
    return {'article': article, 'intro': intro, 'folds': folds,
            'closing': closing, 'disclaimer': disclaimer_card,
            'faqs': list(faqs)}


from guide_body import GUIDES_BODY        # noqa: E402
from guide_energy import GUIDES_ENERGY    # noqa: E402
from guide_womens import GUIDES_WOMENS    # noqa: E402

GUIDES = {}
GUIDES.update(GUIDES_BODY)
GUIDES.update(GUIDES_ENERGY)
GUIDES.update(GUIDES_WOMENS)
