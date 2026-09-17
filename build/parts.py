# -*- coding: utf-8 -*-
"""Reusable form-markup helpers for the VitaCalc page generator.

Conventions used by assets/js/app.js:
  * [data-unit="metric"|"imperial"] blocks are shown/hidden by the unit toggle
  * [data-show-when="name:value"] blocks appear only for those control values
  * every input has a sibling <p class="error-msg" id="<inputId>-error">
  * no native `required` attribute (hidden fields would block submission);
    validation is done in JS so messages stay inline and accessible
"""

import re


def err(field_id):
    return '<p class="error-msg" id="%s-error" role="alert"></p>' % field_id


def number(field_id, label, unit=None, placeholder="", minimum=None, maximum=None,
           step="any", hint=None, required=True, inputmode="decimal"):
    star = ' <span class="req" aria-hidden="true">*</span>' if required else \
           ' <span class="text-muted" style="font-weight:400">(optional)</span>'
    attrs = [
        'class="input"', 'id="%s"' % field_id, 'name="%s"' % field_id,
        'type="number"', 'inputmode="%s"' % inputmode, 'step="%s"' % step,
        'autocomplete="off"',
    ]
    if placeholder:
        attrs.append('placeholder="%s"' % placeholder)
    if minimum is not None:
        attrs.append('data-min="%s"' % minimum)
    if maximum is not None:
        attrs.append('data-max="%s"' % maximum)
    if required:
        attrs.append('aria-required="true"')
    if hint:
        attrs.append('aria-describedby="%s-hint %s-error"' % (field_id, field_id))
    else:
        attrs.append('aria-describedby="%s-error"' % field_id)

    control = '<input %s>' % ' '.join(attrs)
    if unit:
        control = '<div class="input-group">%s<span class="unit">%s</span></div>' % (control, unit)

    return (
        '<div class="field">'
        '<label for="{id}">{label}{star}</label>'
        '{hint}{control}{err}'
        '</div>'
    ).format(
        id=field_id, label=label, star=star, control=control, err=err(field_id),
        hint=('<span class="field__hint" id="%s-hint">%s</span>' % (field_id, hint)) if hint else '',
    )


def units_toggle(note="Switch anytime &mdash; your choice is remembered on this device."):
    return (
        '<div class="unit-switch">'
        '<div><p>Unit system</p><span class="field__hint">%s</span></div>'
        '<fieldset class="segmented">'
        '<legend class="visually-hidden">Unit system</legend>'
        '<input type="radio" name="units" id="units-metric" value="metric" checked>'
        '<label for="units-metric">Metric</label>'
        '<input type="radio" name="units" id="units-imperial" value="imperial">'
        '<label for="units-imperial">Imperial</label>'
        '</fieldset>'
        '</div>' % note
    )


def height_field():
    metric = (
        '<div data-unit="metric">'
        + number('heightCm', 'Height', unit='cm', placeholder='170',
                 minimum=60, maximum=260, step='0.1')
        + '</div>'
    )
    imperial = (
        '<div data-unit="imperial" hidden>'
        '<div class="field">'
        '<span class="field__legend" id="height-imp-label">Height <span class="req" aria-hidden="true">*</span></span>'
        '<div class="input-row" role="group" aria-labelledby="height-imp-label">'
        '<div><div class="input-group">'
        '<input class="input" id="heightFt" name="heightFt" type="number" inputmode="numeric" step="1" '
        'data-min="2" data-max="8" placeholder="5" aria-label="Height, feet" aria-describedby="heightFt-error">'
        '<span class="unit">ft</span></div></div>'
        '<div><div class="input-group">'
        '<input class="input" id="heightIn" name="heightIn" type="number" inputmode="decimal" step="0.5" '
        'data-min="0" data-max="11.9" placeholder="7" aria-label="Height, inches" aria-describedby="heightIn-error">'
        '<span class="unit">in</span></div></div>'
        '</div>'
        + err('heightFt') + err('heightIn') +
        '</div></div>'
    )
    return metric + imperial


def weight_field(required=True, label='Weight', hint=None):
    metric = (
        '<div data-unit="metric">'
        + number('weightKg', label, unit='kg', placeholder='68', minimum=2,
                 maximum=500, step='0.1', required=required, hint=hint)
        + '</div>'
    )
    imperial = (
        '<div data-unit="imperial" hidden>'
        + number('weightLb', label, unit='lb', placeholder='150', minimum=4,
                 maximum=1100, step='0.1', required=required, hint=hint)
        + '</div>'
    )
    return metric + imperial


def length_field(base_id, label, hint=None, metric_ph='', imperial_ph='',
                 metric_min=10, metric_max=250, imperial_min=4, imperial_max=99):
    """A body measurement that exists in both cm and inch variants."""
    metric = (
        '<div data-unit="metric">'
        + number(base_id + 'Cm', label, unit='cm', placeholder=metric_ph,
                 minimum=metric_min, maximum=metric_max, step='0.1', hint=hint)
        + '</div>'
    )
    imperial = (
        '<div data-unit="imperial" hidden>'
        + number(base_id + 'In', label, unit='in', placeholder=imperial_ph,
                 minimum=imperial_min, maximum=imperial_max, step='0.1', hint=hint)
        + '</div>'
    )
    return metric + imperial


def sex_field(legend='Sex at birth',
              hint='Formulas on this page were derived separately for male and female bodies.'):
    return (
        '<fieldset class="field">'
        '<legend class="field__legend">%s <span class="req" aria-hidden="true">*</span></legend>'
        '<span class="field__hint" style="margin:-4px 0 8px">%s</span>'
        '<div class="segmented segmented--block">'
        '<input type="radio" name="sex" id="sex-male" value="male" checked>'
        '<label for="sex-male">Male</label>'
        '<input type="radio" name="sex" id="sex-female" value="female">'
        '<label for="sex-female">Female</label>'
        '</div>'
        '</fieldset>' % (legend, hint)
    )


def select(field_id, label, options, hint=None, extra_attr=''):
    """`options` is a list of (value, text, selected) tuples."""
    opts = ''.join(
        '<option value="%s"%s>%s</option>' % (v, ' selected' if sel else '', t)
        for v, t, sel in options
    )
    return (
        '<div class="field">'
        '<label for="{id}">{label}</label>'
        '{hint}'
        '<select id="{id}" name="{id}" aria-describedby="{id}-error" {extra}>{opts}</select>'
        '{err}'
        '</div>'
    ).format(id=field_id, label=label, opts=opts, extra=extra_attr, err=err(field_id),
             hint=('<span class="field__hint" id="%s-hint">%s</span>' % (field_id, hint)) if hint else '')


def date_field(field_id, label, hint=None, max_today=True):
    return (
        '<div class="field">'
        '<label for="{id}">{label} <span class="req" aria-hidden="true">*</span></label>'
        '{hint}'
        '<input class="input" type="date" id="{id}" name="{id}" '
        'aria-required="true" aria-describedby="{id}-error"{maxattr}>'
        '{err}'
        '</div>'
    ).format(id=field_id, label=label, err=err(field_id),
             maxattr=' data-max-today' if max_today else '',
             hint=('<span class="field__hint" id="%s-hint">%s</span>' % (field_id, hint)) if hint else '')


def segmented(name, legend, options, block=True, hint=None):
    """`options` is a list of (value, text, checked) tuples."""
    items = ''.join(
        '<input type="radio" name="{n}" id="{n}-{v}" value="{v}"{c}><label for="{n}-{v}">{t}</label>'.format(
            n=name, v=v, t=t, c=' checked' if c else '')
        for v, t, c in options
    )
    return (
        '<fieldset class="field">'
        '<legend class="field__legend">%s</legend>'
        '%s'
        '<div class="segmented%s">%s</div>'
        '</fieldset>'
    ) % (legend,
         ('<span class="field__hint" style="margin:-4px 0 8px">%s</span>' % hint) if hint else '',
         ' segmented--block' if block else '', items)


def actions(primary='Calculate'):
    return (
        '<p class="visually-hidden" data-error-summary role="status" aria-live="polite"></p>'
        '<div class="form-actions">'
        '<button type="submit" class="btn btn--primary btn--lg">'
        '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" '
        'stroke-linejoin="round" aria-hidden="true"><rect x="4" y="2" width="16" height="20" rx="2"/>'
        '<line x1="8" y1="6" x2="16" y2="6"/><line x1="8" y1="11" x2="8" y2="11"/><line x1="12" y1="11" x2="12" y2="11"/>'
        '<line x1="16" y1="11" x2="16" y2="11"/><line x1="8" y1="15" x2="8" y2="15"/><line x1="12" y1="15" x2="12" y2="15"/>'
        '<line x1="16" y1="15" x2="16" y2="19"/><line x1="8" y1="19" x2="12" y2="19"/></svg>'
        '%s</button>'
        '<button type="reset" class="btn btn--ghost">Reset</button>'
        '</div>' % primary
    )


# ---------------------------------------------------------------------------
# Method display: equations and procedures, set in the body typeface.
# These replace the old monospace <pre> blocks, which read like developer
# output rather than something a visitor to a health site wants to read.
# ---------------------------------------------------------------------------

def var(text):
    """Highlight a quantity the reader actually enters into the form."""
    return '<span class="eq__var">%s</span>' % text


def op(symbol):
    """An operator, de-emphasised so the quantities stand out."""
    return '<span class="eq__op">%s</span>' % symbol


TIMES = op('&times;')
PLUS = op('+')
MINUS = op('&minus;')
DIV = op('&divide;')


def equation(rows, tag=None, caption=None):
    """`rows` is a list of (left side, right side) HTML pairs.

    A row may also be a 3-tuple whose third item is a small note printed
    under that row.
    """
    out = []
    for row in rows:
        note = ''
        if len(row) == 3:
            lhs, rhs, note_text = row
            note = '<span class="eq__note">%s</span>' % note_text
        else:
            lhs, rhs = row
        out.append(
            '<div class="eq__row"><span class="eq__lhs">%s</span>'
            '<span class="eq__eq">=</span>'
            '<span class="eq__rhs">%s%s</span></div>' % (lhs, rhs, note)
        )
    return '<div class="eq">%s%s%s</div>' % (
        ('<span class="eq__tag">%s</span>' % tag) if tag else '',
        ''.join(out),
        ('<p class="eq__caption">%s</p>' % caption) if caption else '',
    )


def procedure(items):
    """A numbered procedure. Each item is (label, maths, example or None)."""
    out = []
    for i, item in enumerate(items, 1):
        label, maths = item[0], item[1]
        example = item[2] if len(item) > 2 else None
        out.append(
            '<li><span class="steps__num" aria-hidden="true">%d</span>'
            '<div class="steps__body">'
            '<p class="steps__label">%s</p>'
            '<p class="steps__math">%s</p>'
            '%s'
            '</div></li>' % (
                i, label, maths,
                ('<p class="steps__eg">%s</p>' % example) if example else '')
        )
    return '<ol class="steps">%s</ol>' % ''.join(out)


def worked(text, tag='Example'):
    """A worked example in the visitor's own terms."""
    return ('<div class="worked"><span class="worked__tag">%s</span>'
            '<p>%s</p></div>' % (tag, text))


def strip_tags(text):
    """Plain text for an attribute value: no markup, no double quotes."""
    return re.sub(r'<[^>]+>', '', text).replace('"', '&quot;')


def ref_table(caption, head, rows):
    """A small reference table for values that are data, not a formula.

    The scroll container is a labelled, focusable region: on a narrow screen
    these tables scroll sideways, and WCAG 2.1 requires that a scrollable
    area be reachable and operable from the keyboard, not only by touch.
    """
    return (
        '<div class="table-scroll" role="region" tabindex="0" aria-label="%s">'
        '<table class="data">'
        '<caption>%s</caption><thead><tr>%s</tr></thead><tbody>%s</tbody>'
        '</table></div>'
    ) % (
        strip_tags(caption),
        caption,
        ''.join('<th scope="col"%s>%s</th>' % (' class="num"' if n else '', h)
                for h, n in head),
        ''.join('<tr>%s</tr>' % ''.join(
            '<td%s>%s</td>' % (' class="num"' if head[i][1] else '', c)
            for i, c in enumerate(r)) for r in rows),
    )
