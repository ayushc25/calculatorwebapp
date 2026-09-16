# -*- coding: utf-8 -*-
"""End-to-end browser checks: fills each calculator, submits, asserts a result
appears, and captures screenshots for visual review.

Run:  python build/check_browser.py
"""

import os
import sys

from playwright.sync_api import sync_playwright

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SHOTS = os.path.join(os.environ.get('VITACALC_SHOTS', os.path.join(ROOT, 'build', 'screens')))

# slug -> (fill actions, expected substring in the result panel)
CASES = {
    'bmi': ([('fill', '#heightCm', '175'), ('fill', '#weightKg', '70')], 'Healthy weight'),
    'bmr': ([('fill', '#age', '30'), ('fill', '#heightCm', '180'), ('fill', '#weightKg', '80')], '1,780'),
    'ideal-weight': ([('fill', '#heightCm', '178')], 'Reference weight'),
    'body-fat': ([('fill', '#heightCm', '180'), ('fill', '#neckCm', '38'),
                  ('fill', '#waistCm', '85'), ('fill', '#weightKg', '80')], 'Estimated body fat'),
    'calories-burned': ([('fill', '#weightKg', '70'), ('select', '#activity', '8'),
                         ('fill', '#durationMinutes', '30')], 'Calories burned'),
    'pace': ([('fill', '#distance', '10'), ('fill', '#timeM', '50')], '5:00'),
    'period': ([('fill', '#lmp', '2026-09-01'), ('fill', '#cycleLength', '28')], 'Next period'),
    'pregnancy': ([('fill', '#refDate', '2026-05-01')], 'Estimated due date'),
    'bra-size': ([('fill', '#underbust', '78'), ('fill', '#bust', '92')], 'estimated size'),
}

failures = []


def url(rel_path):
    return 'file:///' + os.path.join(ROOT, rel_path).replace('\\', '/')


def run():
    os.makedirs(SHOTS, exist_ok=True)
    with sync_playwright() as p:
        browser = p.chromium.launch()

        for label, viewport in [('desktop', {'width': 1360, 'height': 900}),
                                ('mobile', {'width': 390, 'height': 844})]:
            ctx = browser.new_context(viewport=viewport, device_scale_factor=1)
            page = ctx.new_page()
            console_errors = []
            page.on('console', lambda m: console_errors.append(m.text) if m.type == 'error' else None)
            page.on('pageerror', lambda e: console_errors.append(str(e)))

            # Home + directory
            for name, rel_path in [('home', 'index.html'), ('directory', 'calculators/index.html')]:
                page.goto(url(rel_path))
                page.wait_for_timeout(250)
                page.screenshot(path=os.path.join(SHOTS, '%s-%s.png' % (name, label)),
                                full_page=(label == 'desktop'))

            # Directory search must filter
            page.goto(url('calculators/index.html'))
            page.fill('#calc-search', 'ovulation')
            page.wait_for_timeout(150)
            visible = page.eval_on_selector_all(
                '#calc-grid [data-keywords]',
                'els => els.filter(e => !e.hidden).length')
            if visible != 1:
                failures.append('%s: directory search for "ovulation" showed %d cards, expected 1'
                                % (label, visible))

            # Each calculator
            for slug, (actions, expected) in CASES.items():
                page.goto(url('calculators/%s/index.html' % slug))
                page.wait_for_timeout(120)
                for kind, sel, value in actions:
                    if kind == 'fill':
                        page.fill(sel, value)
                    else:
                        page.select_option(sel, value)
                page.click('#calc-form button[type="submit"]')
                page.wait_for_timeout(250)

                result = page.inner_text('#result') if page.is_visible('#result') else ''
                if expected.lower() not in result.lower():
                    failures.append('%s/%s: result missing %r. Got: %s'
                                    % (label, slug, expected, result[:140].replace('\n', ' ')))
                if page.is_visible('#result-placeholder'):
                    failures.append('%s/%s: placeholder still visible after calculating' % (label, slug))

                page.screenshot(path=os.path.join(SHOTS, 'calc-%s-%s.png' % (slug, label)),
                                full_page=(label == 'desktop'))

            # Validation: empty submit must flag fields, not produce a result
            page.goto(url('calculators/bmi/index.html'))
            page.click('#calc-form button[type="submit"]')
            page.wait_for_timeout(150)
            if page.eval_on_selector_all('[aria-invalid="true"]', 'e => e.length') == 0:
                failures.append('%s: empty BMI submit did not flag any field' % label)
            if page.is_visible('#result') and page.inner_text('#result').strip():
                failures.append('%s: empty BMI submit produced a result' % label)
            page.screenshot(path=os.path.join(SHOTS, 'validation-%s.png' % label))

            # Out-of-range value must be rejected
            page.fill('#heightCm', '400')
            page.fill('#weightKg', '70')
            page.click('#calc-form button[type="submit"]')
            page.wait_for_timeout(150)
            if not page.is_visible('#heightCm-error'):
                failures.append('%s: height of 400 cm was not rejected' % label)

            # Unit toggle swaps the visible fields and persists
            page.goto(url('calculators/bmi/index.html'))
            page.click('label[for="units-imperial"]')
            page.wait_for_timeout(100)
            if not page.is_visible('#heightFt') or page.is_visible('#heightCm'):
                failures.append('%s: imperial toggle did not swap the height fields' % label)
            page.fill('#heightFt', '5')
            page.fill('#heightIn', '9')
            page.fill('#weightLb', '150')
            page.click('#calc-form button[type="submit"]')
            page.wait_for_timeout(200)
            imperial_result = page.inner_text('#result')
            # 150 lb / 5 ft 9 in -> 68.0389 kg / 1.7526 m -> BMI 22.15, shown as 22.2
            if '22.2' not in imperial_result:
                failures.append('%s: imperial BMI for 5ft9/150lb was %s, expected 22.2'
                                % (label, imperial_result[:80].replace('\n', ' ')))
            page.goto(url('calculators/bmr/index.html'))
            page.wait_for_timeout(150)
            if not page.is_visible('#weightLb'):
                failures.append('%s: unit preference did not persist across pages' % label)

            # Reset clears result and errors
            page.goto(url('calculators/pace/index.html'))
            page.fill('#distance', '10')
            page.fill('#timeM', '50')
            page.click('#calc-form button[type="submit"]')
            page.wait_for_timeout(200)
            page.click('#calc-form button[type="reset"]')
            page.wait_for_timeout(200)
            if page.is_visible('#result') and page.inner_text('#result').strip():
                failures.append('%s: reset did not clear the result' % label)

            # Conditional fields: hip appears only for female body fat
            # (checks the wrapper, since which of hipCm/hipIn is shown depends
            #  on the unit system the previous step left in localStorage)
            page.goto(url('calculators/body-fat/index.html'))
            page.wait_for_timeout(120)
            hip = '[data-show-when="sex:female"]'
            if page.is_visible(hip):
                failures.append('%s: hip field visible for male body fat' % label)
            page.click('label[for="sex-female"]')
            page.wait_for_timeout(120)
            if not page.is_visible(hip):
                failures.append('%s: hip field hidden for female body fat' % label)
            if page.eval_on_selector(hip, 'e => e.querySelector("input").disabled'):
                failures.append('%s: hip input still disabled when shown' % label)

            # Pace: switching what to solve for swaps the inputs
            page.goto(url('calculators/pace/index.html'))
            page.click('label[for="solveFor-time"]')
            page.wait_for_timeout(120)
            if page.is_visible('#timeM') or not page.is_visible('#paceM'):
                failures.append('%s: solving for time did not swap time/pace inputs' % label)

            # Mobile nav toggle
            if label == 'mobile':
                page.goto(url('index.html'))
                if page.is_visible('#site-nav a'):
                    failures.append('mobile: nav links visible before opening the menu')
                page.click('.nav-toggle')
                page.wait_for_timeout(200)
                if not page.is_visible('#site-nav a'):
                    failures.append('mobile: nav did not open on toggle')
                page.screenshot(path=os.path.join(SHOTS, 'nav-mobile.png'))
                # Menu items must respect the page gutter, not run to the edge
                left = page.eval_on_selector(
                    '#site-nav .nav__link', 'e => e.getBoundingClientRect().left')
                if left < 18:
                    failures.append('mobile: open menu items start at %dpx, expected the 20px gutter' % left)
                cta = page.eval_on_selector(
                    '#site-nav .nav__cta', 'e => e.getBoundingClientRect().width')
                if cta < 300:
                    failures.append('mobile: menu CTA is %dpx wide, expected to fill the row' % cta)
                icon = page.eval_on_selector(
                    '#site-nav .nav__cta svg', 'e => e.getBoundingClientRect().height')
                if icon > 24:
                    failures.append('mobile: menu CTA icon rendered %dpx tall, expected ~18px' % icon)

            # Method sections must render as designed blocks, not code
            page.goto(url('calculators/period/index.html'))
            page.wait_for_timeout(150)
            if page.eval_on_selector_all('pre', 'e => e.length'):
                failures.append('%s: a <pre> code block is still on the period page' % label)
            if page.eval_on_selector_all('.steps > li', 'e => e.length') != 3:
                failures.append('%s: period method should show 3 steps' % label)
            if not page.is_visible('.worked'):
                failures.append('%s: period method is missing its worked example' % label)

            # No horizontal overflow anywhere
            for rel_path in ['index.html', 'calculators/index.html',
                             'calculators/bmi/index.html', 'calculators/pace/index.html',
                             'calculators/body-fat/index.html', 'calculators/bmr/index.html',
                             'calculators/period/index.html', 'privacy/index.html']:
                page.goto(url(rel_path))
                page.wait_for_timeout(150)
                overflow = page.evaluate(
                    'Math.max(0, document.documentElement.scrollWidth - document.documentElement.clientWidth)')
                if overflow > 1:
                    failures.append('%s: %s scrolls horizontally by %dpx' % (label, rel_path, overflow))

            if console_errors:
                failures.append('%s: console errors -> %s' % (label, console_errors[:3]))
            ctx.close()

        # Theme: light by default even when the OS asks for dark, and the
        # header switch must flip it and remember the choice.
        ctx = browser.new_context(viewport={'width': 1360, 'height': 900}, color_scheme='dark')
        page = ctx.new_page()
        page.goto(url('index.html'))
        page.wait_for_timeout(200)
        theme = page.eval_on_selector('html', 'e => e.getAttribute("data-theme")')
        if theme != 'light':
            failures.append('theme: OS dark preference produced data-theme=%r, expected light' % theme)
        bg = page.eval_on_selector('body', 'e => getComputedStyle(e).backgroundColor')
        if bg != 'rgb(255, 248, 242)':
            failures.append('theme: default body background was %s, expected the cream #FFF8F2' % bg)
        page.screenshot(path=os.path.join(SHOTS, 'home-light-on-dark-os.png'))

        page.click('#theme-toggle')
        page.wait_for_timeout(250)
        if page.eval_on_selector('html', 'e => e.getAttribute("data-theme")') != 'dark':
            failures.append('theme: switch did not turn dark mode on')
        if page.eval_on_selector('#theme-color', 'e => e.content') != '#16100D':
            failures.append('theme: theme-color meta not updated for dark')
        if page.eval_on_selector('#theme-toggle', 'e => e.getAttribute("aria-label")') != 'Switch to light theme':
            failures.append('theme: toggle label did not update')

        # Choice persists across a navigation, with no flash of light first
        page.goto(url('calculators/bmi/index.html'))
        if page.eval_on_selector('html', 'e => e.getAttribute("data-theme")') != 'dark':
            failures.append('theme: choice did not persist to the next page')
        page.fill('#heightCm', '175')
        page.fill('#weightKg', '70')
        page.click('#calc-form button[type="submit"]')
        page.wait_for_timeout(300)
        page.screenshot(path=os.path.join(SHOTS, 'calc-bmi-dark.png'), full_page=True)

        # And switching back sticks too
        page.click('#theme-toggle')
        page.wait_for_timeout(200)
        page.goto(url('index.html'))
        if page.eval_on_selector('html', 'e => e.getAttribute("data-theme")') != 'light':
            failures.append('theme: switching back to light did not persist')
        ctx.close()

        # Keyboard-only path: tab to the form and submit with Enter
        ctx = browser.new_context(viewport={'width': 1360, 'height': 900})
        page = ctx.new_page()
        page.goto(url('calculators/bmi/index.html'))
        page.focus('#heightCm')
        page.keyboard.type('175')
        page.keyboard.press('Tab')
        page.keyboard.type('70')
        page.keyboard.press('Enter')
        page.wait_for_timeout(250)
        if 'Healthy' not in page.inner_text('#result'):
            failures.append('keyboard: Enter did not submit the form')
        ctx.close()

        browser.close()

    print('Screenshots -> %s' % SHOTS)
    for f in failures:
        print('  FAIL  %s' % f)
    print('\n%d browser check failure(s)' % len(failures))
    sys.exit(1 if failures else 0)


if __name__ == '__main__':
    run()
