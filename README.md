# VitaCalc — health & fitness calculators

A static website with nine health calculators, built to the requirements in
`Health_Calculator_Website_Requirements.docx`. Plain HTML, CSS and vanilla
JavaScript — no framework, no build step needed to *serve* it, no backend.

Every calculation runs in the visitor's browser. No measurement is ever sent
to a server.

---

## Quick start

Open `index.html` in a browser. That is the whole thing.

To serve it locally over HTTP (recommended, so relative URLs behave exactly as
they will in production):

```bash
python -m http.server 8000
# then visit http://localhost:8000/
```

---

## What is in here

```
index.html                  Home
calculators/index.html      Directory with live search + category filters
calculators/<slug>/         One folder per calculator (9 of them)
about/  privacy/  terms/  disclaimer/
404.html
sitemap.xml  robots.txt  site.webmanifest

assets/css/main.css         Design system (light + dark, mobile-first)
assets/js/engine.js         Calculation engine — pure functions, no DOM
assets/js/data.js           MET activity table + calculator metadata
assets/js/app.js            UI layer — reads form, validates, renders result
assets/img/                 Favicon, apple touch icon, per-page OG images

build/build.py              Static site generator (regenerates every .html)
build/content.py            All page copy, method prose and FAQs
build/methods.py            The "how it is calculated" blocks for each tool
build/parts.py              Reusable form and method markup helpers
build/test_engine.js        97 reference-value tests for the engine
build/check_site.py         HTML structure, links, a11y wiring, SEO checks
build/check_browser.py      End-to-end browser tests + screenshots
build/check_responsive.py   Layout audit across 11 viewport widths
```

### The nine calculators

| URL | Method used |
|---|---|
| `/calculators/bmi/` | `weight(kg) / height(m)²`, WHO adult categories |
| `/calculators/bmr/` | Mifflin-St Jeor, revised Harris-Benedict, Katch-McArdle + TDEE |
| `/calculators/ideal-weight/` | Devine, Robinson, Miller, Hamwi + healthy BMI range |
| `/calculators/body-fat/` | US Navy circumference method, Deurenberg cross-check |
| `/calculators/calories-burned/` | MET method, 2011 Compendium of Physical Activities |
| `/calculators/pace/` | Solves pace, time or distance; split table |
| `/calculators/period/` | LMP + cycle length, 14-day luteal phase, 6 cycles ahead |
| `/calculators/pregnancy/` | Naegele's rule with cycle-length adjustment |
| `/calculators/bra-size/` | Band/cup from tape, converted across India/UK/US/EU |

---

## Architecture

The SRS asked for the calculation layer to be isolated from presentation, and
it is:

- **`engine.js`** contains every formula as a pure function. It touches no DOM,
  reads no globals, and takes canonical metric units (kg, cm, minutes, `Date`
  objects). It exports through `window.VitaEngine` and also as a CommonJS
  module, which is how the Node test suite loads it.
- **`data.js`** holds the tables that change independently of code: MET values
  (version-stamped), and calculator metadata.
- **`app.js`** does everything else: reads the form, validates, converts units
  to canonical form, calls the engine, and renders the result.

Unit conversion happens *before* calculation and again for display, so a
formula never sees imperial input. Rounding is applied once, at display time.

### Theming

**Light is the default for every visitor**, regardless of their operating
system setting. Dark mode is opt-in through the switch in the header, which
stamps `data-theme="dark"` on `<html>` and stores the choice in `localStorage`
under `vitacalc.theme`.

A small inline script in `<head>` (`THEME_BOOT` in `build/build.py`) applies
the stored choice before first paint, so a returning dark-mode visitor never
sees a flash of light. The dark palette lives in a single
`:root[data-theme="dark"]` block in `main.css` that redefines the colour tokens
and nothing else — `prefers-color-scheme` is deliberately not consulted.

### Explaining the maths

Every calculator carries a "How it is calculated" section. These are **not**
code blocks — a monospace `<pre>` reads like developer output, which is the
wrong register for someone checking their due date. Three components in
`build/parts.py` cover it, and the per-calculator content lives in
`build/methods.py`:

- `equation(...)` — a named formula set in the body typeface, with the
  quantities the visitor actually types highlighted in the brand colour
- `procedure([...])` — a numbered list for date and rule-based logic, each
  step written in plain language with the arithmetic as a second line
- `ref_table(...)` — for values that are data rather than maths (activity
  multipliers, race distances, trimester weeks)

Each block is followed by `worked(...)`, a short example using round numbers,
so a reader can check the page is doing what it says.

### How a calculator page is wired

Markup conventions `app.js` relies on:

| Attribute | Effect |
|---|---|
| `<body data-calc="bmi">` | Selects which engine module runs on submit |
| `[data-unit="metric"\|"imperial"]` | Shown/hidden by the unit toggle |
| `[data-show-when="sex:female"]` | Shown only for those control values; hidden inputs are disabled too |
| `#<inputId>-error` | Inline error message container for that input |
| `data-min` / `data-max` | Validation range, with a readable message on failure |
| `data-met-source` | Populates a `<select>` from the MET dataset |

There is deliberately **no `required` attribute** on inputs. Native validation
cannot focus a hidden field, and half the fields are hidden at any time by the
unit toggle. Validation is done in JS so messages appear inline, are announced
to screen readers, and focus lands on the first bad field.

---

## Rebuilding the HTML

The `.html` files are generated. Edit copy in `build/content.py` (or the shell
in `build/build.py`), then:

```bash
python build/build.py
```

This rewrites every page, the sitemap, robots.txt, the manifest, the favicon
and all OG images. Pillow is required for image generation; if it is missing,
the build still completes and skips the images.

You can also edit the `.html` directly — but a rebuild overwrites it, so put
lasting changes in `build/`.

---

## Before going live

1. **Set your domain.** `BASE_URL` at the top of `build/build.py` is currently
   `https://www.vitacalc.in`. It feeds canonical URLs, Open Graph tags, JSON-LD
   and `sitemap.xml`. Change it and rebuild.
2. **Set the contact address.** `EMAIL` in the same block appears in the footer,
   privacy policy and terms.
3. **Clean URLs.** Internal links point at `.../index.html` so the site works
   when opened from the filesystem. Any static host (Netlify, Vercel, GitHub
   Pages, S3, nginx) will also serve them at `/calculators/bmi/`, which is what
   the canonical tags declare. If you want the `.html` hidden from visitors,
   add a redirect rule from `/calculators/bmi/index.html` → `/calculators/bmi/`.
4. **Legal review.** The privacy policy, terms and health disclaimer are
   written to match how the site actually behaves, but they are drafts — have
   someone qualified read them before publishing.
5. **Submit the sitemap** in Google Search Console.

---

## Testing

```bash
node build/test_engine.js         # 97 formula + date + conversion tests
python build/check_site.py        # structure, links, a11y wiring, SEO
python build/check_browser.py     # drives all 9 calculators in a real browser
python build/check_responsive.py  # layout audit, 16 pages x 11 viewports
```

`test_engine.js` checks every formula against hand-computed reference values,
plus boundary cases (BMI exactly 18.5 and 25.0), leap years, invalid dates like
`2025-02-30`, and impossible measurement combinations.

`check_responsive.py` loads every page at 11 widths from 320px to 1920px and
fails on horizontal overflow, elements past the viewport edge, touch targets
under 40px, text below 12px, number fields squeezed too narrow to read, an
over-wide reading measure, or a viewport where neither the full nav nor the
menu button is reachable. It repeats the check with conditional fields
revealed, since those are hidden on first load. `--shots` also writes
screenshots at each width.

`check_browser.py` fills and submits each calculator at 1360px and 390px,
asserts the expected result text appears, and also checks: empty-submit
validation, out-of-range rejection, the unit toggle and its persistence across
pages, reset behaviour, conditional fields, keyboard-only submission, the theme
switch and its persistence, mobile nav layout, and horizontal overflow. It writes screenshots to `build/screens/` (override
with the `VITACALC_SHOTS` environment variable).

---

## SEO

- One crawlable URL per calculator, unique title and meta description each
- Canonical URLs, Open Graph and Twitter card tags, a generated 1200×630 OG
  image per calculator
- JSON-LD: `WebSite` + `ItemList` on the home page, `ItemList` on the directory,
  and `WebApplication` + `FAQPage` + `BreadcrumbList` on every calculator
- Five substantive FAQs per calculator, written to match real search queries
- `sitemap.xml`, `robots.txt`, `site.webmanifest`, semantic heading structure
- Internal linking between related calculators on every page

## Responsive behaviour

Mobile-first, with four deliberate breakpoints:

| Width | What changes |
|---|---|
| &lt; 480px | Unit badges move under the field as captions, so a three-field time row keeps readable inputs |
| &lt; 560px | A value's own unit picker (pace per km/mi) drops to its own line |
| &lt; 860px | Nav collapses to the menu button; the theme switch stays visible beside it |
| 600&ndash;999px | The calculator stack is capped at 680px and centred, so a tablet does not stretch an age field across 700px |
| &ge; 1000px | Two-column calculator layout: form and article left, result and links right |
| &ge; 1500px | Content width grows from 1140px to 1240px |

Verified at 320, 360, 390, 430, 540, 768, 820, 1024, 1280, 1440 and 1920px.

## Accessibility

- Labelled inputs, `aria-describedby` on hints and errors, `aria-invalid` +
  inline messages on failure, focus moved to the first bad field
- Result panel is an `aria-live` region, so results are announced
- Visible focus rings, ≥48px touch targets, skip link, landmark elements
- Colour contrast meets WCAG AA — the filled coral used behind white text is a
  deeper tone (`--coral-solid`, 4.85:1) than the bright accent coral used for
  borders and icons
- Respects `prefers-reduced-motion`
- The theme switch is a real button with `aria-pressed` and a label that says
  which mode it will switch to

---

## Notes on the requirements document

Two intentional deviations, both agreed in the brief:

- **The SRS suggested React/Next.js.** This is plain HTML per the request. The
  separation the SRS actually cared about — pure calculation layer, isolated
  data tables, no backend — is preserved, and a Python generator keeps the
  shared shell DRY rather than duplicating a header across 16 files by hand.
- **The SRS titled the scope "8 calculators" but listed 9** (BMR was added as an
  extra requirement). All nine are built.

One judgement call worth flagging: **EU bra sizing**. Deriving the EU band from
the underbust in centimetres and the cup from a rounded centimetre band
produces results that contradict the standard UK↔EU conversion chart by up to
two cup letters. The engine instead computes one band-and-cup-step pair from
the inch measurements and maps it into each system (EU band = UK inches × 2.5 −
10), so the four systems it reports are mutually consistent. Bra sizing is not
standardised between brands in any case, which the page says plainly.
