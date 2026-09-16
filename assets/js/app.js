/* ==========================================================================
   VitaCalc — UI layer
   Reads the form, validates, calls VitaEngine (pure), renders the result.
   No formula lives in this file.
   ========================================================================== */
(function () {
  'use strict';

  var E = window.VitaEngine;
  var D = window.VitaData;
  var STORE_KEY = 'vitacalc.units';
  var THEME_KEY = 'vitacalc.theme';

  /* ------------------------------------------------------------------ *
   * Tiny DOM helpers
   * ------------------------------------------------------------------ */
  function $(sel, ctx) { return (ctx || document).querySelector(sel); }
  function $$(sel, ctx) { return Array.prototype.slice.call((ctx || document).querySelectorAll(sel)); }

  function esc(str) {
    return String(str).replace(/[&<>"']/g, function (c) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c];
    });
  }

  function fmt(n, decimals) {
    var d = decimals === undefined ? 0 : decimals;
    return Number(n).toLocaleString(undefined, { minimumFractionDigits: d, maximumFractionDigits: d });
  }

  var WARN_ICON = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>';

  /* ------------------------------------------------------------------ *
   * Theme: light by default. The visitor's choice is remembered on this
   * device only; the OS preference is deliberately not followed, so the
   * site looks the same for everyone until they ask for something else.
   * A matching inline script in <head> applies the stored value before
   * first paint, so there is no flash on a return visit.
   * ------------------------------------------------------------------ */
  function applyTheme(theme) {
    document.documentElement.setAttribute('data-theme', theme);
    var meta = document.getElementById('theme-color');
    if (meta) meta.setAttribute('content', theme === 'dark' ? '#16100D' : '#FFF8F2');
    var btn = document.getElementById('theme-toggle');
    if (btn) {
      var next = theme === 'dark' ? 'light' : 'dark';
      btn.setAttribute('aria-label', 'Switch to ' + next + ' theme');
      btn.setAttribute('title', 'Switch to ' + next + ' theme');
      btn.setAttribute('aria-pressed', String(theme === 'dark'));
    }
  }

  function initTheme() {
    var stored = null;
    try { stored = localStorage.getItem(THEME_KEY); } catch (e) { stored = null; }
    applyTheme(stored === 'dark' ? 'dark' : 'light');

    var btn = document.getElementById('theme-toggle');
    if (!btn) return;
    btn.addEventListener('click', function () {
      var next = document.documentElement.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
      applyTheme(next);
      try { localStorage.setItem(THEME_KEY, next); } catch (e) { /* storage blocked */ }
    });
  }

  /* ------------------------------------------------------------------ *
   * Site chrome: mobile nav, footer year
   * ------------------------------------------------------------------ */
  function initChrome() {
    var toggle = $('.nav-toggle');
    var nav = $('#site-nav');
    if (toggle && nav) {
      toggle.addEventListener('click', function () {
        var open = toggle.getAttribute('aria-expanded') === 'true';
        toggle.setAttribute('aria-expanded', String(!open));
        nav.classList.toggle('is-open', !open);
      });
      document.addEventListener('keydown', function (e) {
        if (e.key === 'Escape' && nav.classList.contains('is-open')) {
          nav.classList.remove('is-open');
          toggle.setAttribute('aria-expanded', 'false');
          toggle.focus();
        }
      });
    }
    $$('[data-year]').forEach(function (n) { n.textContent = new Date().getFullYear(); });
  }

  /* ------------------------------------------------------------------ *
   * Validation helpers
   * ------------------------------------------------------------------ */
  function setError(input, message) {
    if (!input) return;
    input.setAttribute('aria-invalid', 'true');
    var box = document.getElementById(input.id + '-error');
    if (box) {
      box.innerHTML = WARN_ICON + '<span>' + esc(message) + '</span>';
      box.classList.add('is-visible');
    }
  }

  function clearError(input) {
    if (!input) return;
    input.removeAttribute('aria-invalid');
    var box = document.getElementById(input.id + '-error');
    if (box) { box.classList.remove('is-visible'); box.innerHTML = ''; }
  }

  function clearAllErrors(form) {
    $$('[aria-invalid="true"]', form).forEach(clearError);
    $$('.error-msg', form).forEach(function (b) { b.classList.remove('is-visible'); b.innerHTML = ''; });
    var summary = $('[data-error-summary]', form);
    if (summary) { summary.textContent = ''; }
  }

  /**
   * Reads a numeric input and validates it against data-min / data-max.
   * Returns null (and flags the field) when invalid.
   */
  function num(form, id, opts) {
    opts = opts || {};
    var input = form.querySelector('#' + id);
    if (!input) return null;
    var raw = input.value.trim();

    if (raw === '') {
      if (opts.optional) return undefined;
      setError(input, opts.requiredMsg || 'This field is required.');
      return null;
    }
    var value = Number(raw);
    if (!isFinite(value)) {
      setError(input, 'Enter a number.');
      return null;
    }
    var min = opts.min !== undefined ? opts.min : parseFloat(input.getAttribute('data-min'));
    var max = opts.max !== undefined ? opts.max : parseFloat(input.getAttribute('data-max'));
    if (isFinite(min) && value < min) {
      setError(input, 'Enter a value of at least ' + min + (opts.unit ? ' ' + opts.unit : '') + '.');
      return null;
    }
    if (isFinite(max) && value > max) {
      setError(input, 'Enter a value no higher than ' + max + (opts.unit ? ' ' + opts.unit : '') + '.');
      return null;
    }
    clearError(input);
    return value;
  }

  function radioValue(form, name) {
    var checked = form.querySelector('input[name="' + name + '"]:checked');
    return checked ? checked.value : null;
  }

  function announceInvalid(form, count) {
    var summary = $('[data-error-summary]', form);
    if (summary) {
      summary.textContent = count === 1
        ? 'One field needs attention. See the message below the highlighted field.'
        : count + ' fields need attention. See the messages below the highlighted fields.';
    }
    var firstBad = form.querySelector('[aria-invalid="true"]');
    if (firstBad) firstBad.focus();
  }

  function countInvalid(form) { return $$('[aria-invalid="true"]', form).length; }

  /* ------------------------------------------------------------------ *
   * Unit system: toggles [data-unit="metric" | "imperial"] blocks
   * ------------------------------------------------------------------ */
  function currentUnits(form) {
    return radioValue(form, 'units') || 'metric';
  }

  function applyUnits(form, system) {
    $$('[data-unit]', form).forEach(function (node) {
      node.hidden = node.getAttribute('data-unit') !== system;
    });
    $$('[data-unit-label]', form).forEach(function (node) {
      var map = node.getAttribute('data-unit-label').split('|');
      node.textContent = system === 'metric' ? map[0] : map[1];
    });
  }

  function initUnits(form) {
    var radios = $$('input[name="units"]', form);
    if (!radios.length) return;
    var saved = null;
    try { saved = localStorage.getItem(STORE_KEY); } catch (e) { saved = null; }
    if (saved === 'metric' || saved === 'imperial') {
      radios.forEach(function (r) { r.checked = r.value === saved; });
    }
    applyUnits(form, currentUnits(form));
    radios.forEach(function (r) {
      r.addEventListener('change', function () {
        applyUnits(form, r.value);
        try { localStorage.setItem(STORE_KEY, r.value); } catch (e) { /* storage blocked */ }
      });
    });
  }

  /* Canonical readers ------------------------------------------------- */
  function readHeightCm(form) {
    if (currentUnits(form) === 'metric') {
      return num(form, 'heightCm', { unit: 'cm' });
    }
    var ft = num(form, 'heightFt', { unit: 'ft' });
    var inch = num(form, 'heightIn', { optional: true, unit: 'in' });
    if (ft === null || inch === null) return null;
    var cm = E.convert.ftInToCm(ft, inch === undefined ? 0 : inch);
    if (cm < 60 || cm > 260) {
      setError(form.querySelector('#heightFt'), 'Enter a height between 2 ft and 8 ft 6 in.');
      return null;
    }
    return cm;
  }

  function readWeightKg(form, opts) {
    opts = opts || {};
    if (currentUnits(form) === 'metric') {
      return num(form, 'weightKg', { unit: 'kg', optional: opts.optional });
    }
    var lb = num(form, 'weightLb', { unit: 'lb', optional: opts.optional });
    if (lb === null || lb === undefined) return lb;
    return E.convert.lbToKg(lb);
  }

  function readLengthCm(form, id, label) {
    var metric = currentUnits(form) === 'metric';
    var value = num(form, metric ? id + 'Cm' : id + 'In', { unit: metric ? 'cm' : 'in' });
    if (value === null) return null;
    return metric ? value : E.convert.inToCm(value);
  }

  /* Display formatters ------------------------------------------------ */
  function weightOut(kg, system) {
    return system === 'metric'
      ? fmt(kg, 1) + ' kg'
      : fmt(E.convert.kgToLb(kg), 1) + ' lb';
  }

  /* ------------------------------------------------------------------ *
   * Result plumbing
   * ------------------------------------------------------------------ */
  function showResult(form, html) {
    var box = document.getElementById('result');
    if (!box) return;
    box.innerHTML = html;
    box.classList.add('is-visible');
    box.setAttribute('aria-busy', 'false');
    var placeholder = document.getElementById('result-placeholder');
    if (placeholder) placeholder.hidden = true;
    if (window.matchMedia('(max-width: 999px)').matches) {
      box.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
    var heading = box.querySelector('[tabindex="-1"]');
    if (heading) heading.focus({ preventScroll: true });
  }

  function hideResult() {
    var box = document.getElementById('result');
    if (box) { box.classList.remove('is-visible'); box.innerHTML = ''; }
    var placeholder = document.getElementById('result-placeholder');
    if (placeholder) placeholder.hidden = false;
  }

  function resultCard(label, value, unit, tag, sub) {
    return '<div class="result-card">' +
      '<p class="result-card__label" id="result-heading" tabindex="-1">' + esc(label) + '</p>' +
      '<div class="result-card__value">' + value + (unit ? '<span>' + esc(unit) + '</span>' : '') + '</div>' +
      (tag ? '<div class="result-card__tag">' + esc(tag) + '</div>' : '') +
      (sub ? '<p class="result-card__sub">' + sub + '</p>' : '') +
      '</div>';
  }

  function stats(items) {
    return '<dl class="stat-grid">' + items.map(function (i) {
      return '<div class="stat"><dt>' + esc(i.label) + '</dt><dd>' + i.value +
        (i.unit ? '<small>' + esc(i.unit) + '</small>' : '') + '</dd></div>';
    }).join('') + '</dl>';
  }

  function callout(text, variant) {
    return '<div class="callout' + (variant ? ' callout--' + variant : '') + '">' + WARN_ICON +
      '<p>' + text + '</p></div>';
  }

  /**
   * Horizontal category gauge. `ranges` is a list of {label,min,max,color}.
   */
  function gauge(ranges, value, displayMin, displayMax, unitSuffix) {
    var span = displayMax - displayMin;
    var segs = ranges.map(function (r) {
      var lo = Math.max(r.min, displayMin);
      var hi = Math.min(r.max === Infinity ? displayMax : r.max, displayMax);
      var width = Math.max(0, (hi - lo) / span * 100);
      if (width <= 0) return '';
      return '<div class="gauge__seg" style="flex:' + width.toFixed(2) + ';background:' + r.color + '"></div>';
    }).join('');

    var pos = E.clamp((value - displayMin) / span * 100, 0, 100);
    var legend = ranges.map(function (r) {
      return '<span><i class="gauge__dot" style="background:' + r.color + '"></i>' + esc(r.label) + '</span>';
    }).join('');

    return '<div class="gauge">' +
      '<div class="gauge__bar">' + segs + '</div>' +
      '<div class="gauge__marker"><div class="gauge__pin" style="left:' + pos.toFixed(2) + '%">' +
      esc(fmt(value, 1)) + (unitSuffix || '') + '</div></div>' +
      '<div class="gauge__legend">' + legend + '</div>' +
      '</div>';
  }

  function table(head, rows, caption) {
    return '<div class="table-scroll"><table class="data">' +
      (caption ? '<caption>' + esc(caption) + '</caption>' : '') +
      '<thead><tr>' + head.map(function (h) {
        return '<th' + (h.num ? ' class="num" scope="col"' : ' scope="col"') + '>' + esc(h.label) + '</th>';
      }).join('') + '</tr></thead><tbody>' +
      rows.map(function (r) {
        return '<tr' + (r.active ? ' class="is-active"' : '') + '>' + r.cells.map(function (c, i) {
          return '<td' + (head[i] && head[i].num ? ' class="num"' : '') + '>' + c + '</td>';
        }).join('') + '</tr>';
      }).join('') + '</tbody></table></div>';
  }

  var DISCLAIMER = 'These results are estimates for general information only. They are not a diagnosis and not medical advice. Talk to a qualified healthcare professional before acting on them.';

  /* ================================================================== *
   * Calculator modules
   * ================================================================== */
  var modules = {};

  /* ---------------------------- BMI --------------------------------- */
  modules.bmi = function (form) {
    var system = currentUnits(form);
    var heightCm = readHeightCm(form);
    var weightKg = readWeightKg(form);
    var age = num(form, 'age', { optional: true, min: 2, max: 120, unit: 'years' });
    if (heightCm === null || weightKg === null || age === null) return false;

    var r = E.calculateBmi({ heightCm: heightCm, weightKg: weightKg });

    var rows = E.BMI_CATEGORIES.map(function (c) {
      var range = c.max === Infinity ? c.min.toFixed(1) + ' and above'
        : (c.min === 0 ? 'Under ' + c.max.toFixed(1) : c.min.toFixed(1) + ' – ' + (c.max - 0.1).toFixed(1));
      return { active: c.key === r.category.key, cells: [esc(c.label), range] };
    });

    var html = resultCard('Your BMI', fmt(r.bmi, 1), '', r.category.label,
      'Based on ' + esc(weightOut(weightKg, system)) + ' at ' +
      esc(system === 'metric' ? fmt(heightCm, 0) + ' cm' : formatFtIn(heightCm)) + '.');

    html += gauge(E.BMI_CATEGORIES, E.clamp(r.bmiRaw, 14, 42), 14, 42, '');

    html += stats([
      { label: 'Healthy weight range', value: system === 'metric'
          ? fmt(r.healthyMinKg, 1) + '–' + fmt(r.healthyMaxKg, 1)
          : fmt(E.convert.kgToLb(r.healthyMinKg), 0) + '–' + fmt(E.convert.kgToLb(r.healthyMaxKg), 0),
        unit: system === 'metric' ? 'kg' : 'lb' },
      { label: 'Ponderal index', value: fmt(r.ponderal, 1), unit: 'kg/m³' }
    ]);

    html += '<h3 class="mt-3">Where your BMI sits</h3>' +
      table([{ label: 'Category' }, { label: 'BMI range' }], rows, null);

    if (age !== undefined && age < 20) {
      html += callout('<strong>BMI works differently under 20.</strong> For children and teenagers, BMI is interpreted against age- and sex-specific growth percentiles rather than these adult categories. Please use this figure only as a rough reference and speak to a paediatrician.', 'warn');
    }
    html += callout(DISCLAIMER);
    return html;
  };

  function formatFtIn(cm) {
    var v = E.convert.cmToFtIn(cm);
    return v.ft + " ft " + Math.round(v.inches) + ' in';
  }

  /* ---------------------------- BMR --------------------------------- */
  modules.bmr = function (form) {
    var system = currentUnits(form);
    var sex = radioValue(form, 'sex');
    var age = num(form, 'age', { min: 15, max: 100, unit: 'years' });
    var heightCm = readHeightCm(form);
    var weightKg = readWeightKg(form);
    var formula = $('#formula', form).value;
    var activityKey = $('#activity', form).value;
    var bodyFatPct = num(form, 'bodyFat', { optional: true, min: 3, max: 65, unit: '%' });
    if (age === null || heightCm === null || weightKg === null || bodyFatPct === null) return false;

    if (formula === 'katch' && bodyFatPct === undefined) {
      setError($('#bodyFat', form), 'The Katch-McArdle formula needs your body-fat percentage.');
      return false;
    }

    var r = E.calculateBmr({
      sex: sex, age: age, heightCm: heightCm, weightKg: weightKg,
      formula: formula, activityKey: activityKey, bodyFatPct: bodyFatPct
    });
    if (!r) return false;

    var label = { mifflin: 'Mifflin-St Jeor', harris: 'Revised Harris-Benedict', katch: 'Katch-McArdle' }[formula];

    var html = resultCard('Basal metabolic rate', fmt(r.bmr, 0), 'kcal/day', label + ' formula',
      'This is roughly what your body burns over 24 hours at complete rest.');

    html += stats([
      { label: 'Maintenance calories (TDEE)', value: fmt(r.tdee, 0), unit: 'kcal' },
      { label: 'Mild weight loss (~0.25 kg/wk)', value: fmt(r.mildLoss, 0), unit: 'kcal' },
      { label: 'Weight loss (~0.5 kg/wk)', value: fmt(r.weightLoss, 0), unit: 'kcal' },
      { label: 'Weight gain (~0.5 kg/wk)', value: fmt(r.weightGain, 0), unit: 'kcal' }
    ]);

    html += '<h3 class="mt-3">Daily calories by activity level</h3>' +
      table(
        [{ label: 'Activity level' }, { label: 'Typical week' }, { label: 'Calories/day', num: true }],
        r.byLevel.map(function (l) {
          return { active: l.key === activityKey, cells: [esc(l.label), esc(l.hint), fmt(l.calories, 0)] };
        })
      );

    html += callout('<strong>BMR is an estimate, not a measurement.</strong> Prediction equations are typically within about 10% of lab-measured resting metabolic rate for most adults, but individual metabolism varies. Use the number as a starting point and adjust based on real-world results over 2–3 weeks.');
    html += callout(DISCLAIMER);
    return html;
  };

  /* ------------------------ Ideal weight ---------------------------- */
  modules['ideal-weight'] = function (form) {
    var system = currentUnits(form);
    var sex = radioValue(form, 'sex');
    var heightCm = readHeightCm(form);
    var formula = $('#formula', form).value;
    var weightKg = readWeightKg(form, { optional: true });
    if (heightCm === null || weightKg === null) return false;

    var r = E.calculateIdealWeight({ heightCm: heightCm, sex: sex, formula: formula });

    var sub = 'For ' + esc(system === 'metric' ? fmt(heightCm, 0) + ' cm' : formatFtIn(heightCm)) +
      ', using the ' + esc(r.formulaLabel) + ' formula.';
    var html = resultCard('Reference weight', system === 'metric' ? fmt(r.idealKg, 1) : fmt(E.convert.kgToLb(r.idealKg), 1),
      system === 'metric' ? 'kg' : 'lb', null, sub);

    var statItems = [
      { label: 'Healthy BMI range', value: system === 'metric'
          ? fmt(r.healthyMinKg, 1) + '–' + fmt(r.healthyMaxKg, 1)
          : fmt(E.convert.kgToLb(r.healthyMinKg), 0) + '–' + fmt(E.convert.kgToLb(r.healthyMaxKg), 0),
        unit: system === 'metric' ? 'kg' : 'lb' }
    ];
    if (weightKg !== undefined) {
      var diff = weightKg - r.idealKg;
      statItems.push({
        label: 'Difference from your weight',
        value: (diff >= 0 ? '+' : '−') + (system === 'metric' ? fmt(Math.abs(diff), 1) : fmt(Math.abs(E.convert.kgToLb(diff)), 1)),
        unit: system === 'metric' ? 'kg' : 'lb'
      });
      var bmi = E.calculateBmi({ weightKg: weightKg, heightCm: heightCm });
      statItems.push({ label: 'Your current BMI', value: fmt(bmi.bmi, 1), unit: bmi.category.label });
    }
    html += stats(statItems);

    html += '<h3 class="mt-3">All four formulas compared</h3>' +
      table(
        [{ label: 'Formula' }, { label: 'Result', num: true }, { label: 'About' }],
        r.allFormulas.map(function (f) {
          return {
            active: f.key === r.formulaKey,
            cells: [
              esc(f.label),
              system === 'metric' ? fmt(f.weightKg, 1) + ' kg' : fmt(E.convert.kgToLb(f.weightKg), 1) + ' lb',
              esc(f.note)
            ]
          };
        })
      );

    html += callout('<strong>There is no single ideal weight.</strong> These formulas were built for clinical dosing and population averages in the 1960s–1980s. They ignore frame size, muscle mass and body composition, so an athlete can sit well above the figure and be perfectly healthy. Treat the healthy BMI range as the more useful target.');
    html += callout(DISCLAIMER);
    return html;
  };

  /* -------------------------- Body fat ------------------------------ */
  modules['body-fat'] = function (form) {
    var system = currentUnits(form);
    var sex = radioValue(form, 'sex');
    var heightCm = readHeightCm(form);
    var neckCm = readLengthCm(form, 'neck');
    var waistCm = readLengthCm(form, 'waist');
    var hipCm = sex === 'female' ? readLengthCm(form, 'hip') : undefined;
    var weightKg = readWeightKg(form, { optional: true });
    var age = num(form, 'age', { optional: true, min: 15, max: 100, unit: 'years' });
    if (heightCm === null || neckCm === null || waistCm === null || hipCm === null ||
        weightKg === null || age === null) return false;

    var r = E.calculateBodyFat({
      sex: sex, heightCm: heightCm, neckCm: neckCm, waistCm: waistCm,
      hipCm: hipCm, weightKg: weightKg, age: age
    });

    if (r.error) {
      setError($('#' + (system === 'metric' ? 'waistCm' : 'waistIn'), form), r.error);
      return false;
    }

    var ranges = E.BODY_FAT_RANGES[sex];
    var html = resultCard('Estimated body fat', fmt(r.bodyFatPct, 1), '%', r.category.label, esc(r.method));
    html += gauge(ranges, E.clamp(r.bodyFatPct, 2, sex === 'male' ? 40 : 46), 2, sex === 'male' ? 40 : 46, '%');

    var statItems = [];
    if (r.fatMassKg !== undefined) {
      statItems.push({ label: 'Fat mass', value: system === 'metric' ? fmt(r.fatMassKg, 1) : fmt(E.convert.kgToLb(r.fatMassKg), 1), unit: system === 'metric' ? 'kg' : 'lb' });
      statItems.push({ label: 'Lean mass', value: system === 'metric' ? fmt(r.leanMassKg, 1) : fmt(E.convert.kgToLb(r.leanMassKg), 1), unit: system === 'metric' ? 'kg' : 'lb' });
    }
    if (r.bmiMethodPct !== undefined) {
      statItems.push({ label: 'BMI method cross-check', value: fmt(r.bmiMethodPct, 1), unit: '%' });
    }
    if (statItems.length) html += stats(statItems);

    html += '<h3 class="mt-3">Reference ranges for ' + esc(sex === 'male' ? 'men' : 'women') + '</h3>' +
      table(
        [{ label: 'Category' }, { label: 'Body fat' }],
        ranges.map(function (c) {
          var range = c.max === Infinity ? c.min + '% and above' : c.min + '% – ' + c.max + '%';
          return { active: c.key === r.category.key, cells: [esc(c.label), range] };
        })
      );

    html += callout('<strong>Tape measurements are sensitive.</strong> A 1 cm difference in waist measurement can shift the result by more than a full percentage point. Measure at the same time of day, relaxed, without pulling the tape tight, and re-measure twice to average. For a precise figure, DEXA or hydrostatic weighing is the reference standard.');
    html += callout(DISCLAIMER);
    return html;
  };

  /* ---------------------- Calories burned --------------------------- */
  modules['calories-burned'] = function (form) {
    var system = currentUnits(form);
    var weightKg = readWeightKg(form);
    var select = $('#activity', form);
    var met = parseFloat(select.value);
    var hours = num(form, 'durationHours', { optional: true, min: 0, max: 24, unit: 'hours' });
    var minutes = num(form, 'durationMinutes', { optional: true, min: 0, max: 59, unit: 'minutes' });
    if (weightKg === null || hours === null || minutes === null) return false;

    var totalMinutes = (hours === undefined ? 0 : hours) * 60 + (minutes === undefined ? 0 : minutes);
    if (totalMinutes <= 0) {
      setError($('#durationMinutes', form), 'Enter a duration of at least one minute.');
      return false;
    }
    if (totalMinutes > 1440) {
      setError($('#durationHours', form), 'Duration cannot exceed 24 hours.');
      return false;
    }

    var label = select.options[select.selectedIndex].textContent.replace(/\s*\(MET.*$/, '');
    var r = E.calculateCaloriesBurned({ met: met, weightKg: weightKg, minutes: totalMinutes, activityLabel: label });

    var durationText = (totalMinutes >= 60 ? Math.floor(totalMinutes / 60) + ' h ' : '') +
      (totalMinutes % 60) + ' min';

    var html = resultCard('Calories burned', fmt(r.total, 0), 'kcal', label,
      esc(durationText) + ' at ' + esc(weightOut(weightKg, system)) + ' body weight.');

    html += stats([
      { label: 'Per minute', value: fmt(r.perMinute, 1), unit: 'kcal' },
      { label: 'Per hour', value: fmt(r.perHour, 0), unit: 'kcal' },
      { label: 'MET value', value: fmt(r.met, 1) },
      { label: 'MET-minutes', value: fmt(r.metMinutes, 0) }
    ]);

    var weekly = Math.round(r.metMinutes);
    html += '<h3 class="mt-3">If you repeat this session</h3>' +
      table(
        [{ label: 'Frequency' }, { label: 'Calories', num: true }, { label: 'MET-minutes', num: true }],
        [3, 4, 5, 7].map(function (n) {
          return { cells: [n + '× per week', fmt(r.total * n, 0), fmt(weekly * n, 0)] };
        })
      );

    html += callout('The WHO recommends at least <strong>500–1000 MET-minutes per week</strong> of physical activity for adults, which is roughly 150–300 minutes of moderate activity. Your single session above is worth ' + fmt(r.metMinutes, 0) + ' MET-minutes.');
    html += callout('<strong>MET values are population averages.</strong> Real energy expenditure varies with fitness, technique, terrain and body composition, so treat this as a ballpark rather than an exact count. Dataset: Compendium of Physical Activities (2011), version ' + esc(D.METS_VERSION) + '.');
    return html;
  };

  /* ----------------------------- Pace ------------------------------- */
  modules.pace = function (form) {
    var solveFor = radioValue(form, 'solveFor') || 'pace';
    var distUnit = radioValue(form, 'distUnit') || 'km';
    var paceUnit = radioValue(form, 'paceUnit') || 'km';

    var distanceKm = null, timeSeconds = null, paceSecPerKm = null;

    if (solveFor !== 'distance') {
      var dist = num(form, 'distance', { min: 0.01, max: 2000, unit: distUnit });
      if (dist === null) return false;
      distanceKm = distUnit === 'km' ? dist : E.convert.miToKm(dist);
    }
    if (solveFor !== 'time') {
      var h = num(form, 'timeH', { optional: true, min: 0, max: 99, unit: 'hours' });
      var m = num(form, 'timeM', { optional: true, min: 0, max: 59, unit: 'minutes' });
      var s = num(form, 'timeS', { optional: true, min: 0, max: 59, unit: 'seconds' });
      if (h === null || m === null || s === null) return false;
      timeSeconds = E.hmsToSeconds(h || 0, m || 0, s || 0);
      if (timeSeconds <= 0) {
        setError($('#timeM', form), 'Enter a total time greater than zero.');
        return false;
      }
    }
    if (solveFor !== 'pace') {
      var pm = num(form, 'paceM', { min: 0, max: 99, unit: 'minutes' });
      var ps = num(form, 'paceS', { optional: true, min: 0, max: 59, unit: 'seconds' });
      if (pm === null || ps === null) return false;
      var paceSec = pm * 60 + (ps || 0);
      if (paceSec <= 0) {
        setError($('#paceM', form), 'Enter a pace greater than zero.');
        return false;
      }
      paceSecPerKm = paceUnit === 'km' ? paceSec : paceSec / 1.609344;
    }

    var r = E.calculatePace({
      solveFor: solveFor, distanceKm: distanceKm,
      timeSeconds: timeSeconds, paceSecPerKm: paceSecPerKm
    });
    if (r.error) {
      setError($('#distance', form), r.error);
      return false;
    }

    var headline, headlineLabel, headlineUnit = '';
    if (solveFor === 'pace') {
      headlineLabel = 'Your pace';
      headline = E.formatDuration(paceUnit === 'km' ? r.paceSecPerKm : r.paceSecPerMi);
      headlineUnit = paceUnit === 'km' ? 'min/km' : 'min/mi';
    } else if (solveFor === 'time') {
      headlineLabel = 'Finish time';
      headline = E.formatDuration(r.timeSeconds);
    } else {
      headlineLabel = 'Distance';
      headline = fmt(distUnit === 'km' ? r.distanceKm : E.convert.kmToMi(r.distanceKm), 2);
      headlineUnit = distUnit;
    }

    var html = resultCard(headlineLabel, headline, headlineUnit, null,
      fmt(distUnit === 'km' ? r.distanceKm : E.convert.kmToMi(r.distanceKm), 2) + ' ' + distUnit +
      ' in ' + E.formatDuration(r.timeSeconds));

    html += stats([
      { label: 'Pace per km', value: E.formatDuration(r.paceSecPerKm), unit: 'min' },
      { label: 'Pace per mile', value: E.formatDuration(r.paceSecPerMi), unit: 'min' },
      { label: 'Speed', value: fmt(r.speedKmh, 2), unit: 'km/h' },
      { label: 'Speed', value: fmt(r.speedMph, 2), unit: 'mph' }
    ]);

    html += '<h3 class="mt-3">Split times at this pace</h3>' +
      table(
        [{ label: 'Distance' }, { label: 'Time', num: true }],
        r.splits.map(function (s) {
          return { cells: [esc(s.label), E.formatDuration(s.seconds)] };
        })
      );

    html += callout('Race predictions from a single pace assume you can hold that effort for the full distance. Most runners slow by 4–6% per doubling of race distance, so treat longer projections as optimistic.');
    return html;
  };

  /* ---------------------------- Period ------------------------------ */
  modules.period = function (form) {
    var lmpInput = $('#lmp', form);
    var lmp = E.parseISODate(lmpInput.value);
    if (!lmp) {
      setError(lmpInput, 'Choose the first day of your last period.');
      return false;
    }
    var today = new Date(); today.setHours(0, 0, 0, 0);
    if (lmp > today) {
      setError(lmpInput, 'That date is in the future. Enter the date your last period started.');
      return false;
    }
    if (E.daysBetween(lmp, today) > 365) {
      setError(lmpInput, 'That date is more than a year ago. Enter your most recent period start date.');
      return false;
    }
    clearError(lmpInput);

    var cycleLength = num(form, 'cycleLength', { min: 20, max: 45, unit: 'days' });
    var periodLength = num(form, 'periodLength', { optional: true, min: 1, max: 14, unit: 'days' });
    if (cycleLength === null || periodLength === null) return false;

    var r = E.calculatePeriod({
      lmp: lmp, cycleLength: cycleLength,
      periodLength: periodLength === undefined ? 5 : periodLength, cycles: 6
    });

    var daysText = r.daysUntilNext === 0 ? 'today'
      : r.daysUntilNext > 0 ? 'in ' + r.daysUntilNext + ' day' + (r.daysUntilNext === 1 ? '' : 's')
      : Math.abs(r.daysUntilNext) + ' day' + (Math.abs(r.daysUntilNext) === 1 ? '' : 's') + ' ago';

    var html = resultCard('Next period expected', E.formatShortDate(r.next.periodStart), '', 'Expected ' + daysText,
      'You are on day ' + r.cycleDay + ' of a ' + r.cycleLength + '-day cycle.');

    html += stats([
      { label: 'Period window', value: '<span style="font-size:.72em">' + esc(E.formatShortDate(r.next.periodStart)) + ' – ' + esc(E.formatShortDate(r.next.periodEnd)) + '</span>' },
      { label: 'Estimated ovulation', value: '<span style="font-size:.72em">' + esc(E.formatShortDate(r.next.ovulation)) + '</span>' },
      { label: 'Fertile window', value: '<span style="font-size:.72em">' + esc(E.formatShortDate(r.next.fertileStart)) + ' – ' + esc(E.formatShortDate(r.next.fertileEnd)) + '</span>' }
    ]);

    html += '<h3 class="mt-3">Your next six cycles</h3>' +
      table(
        [{ label: 'Cycle' }, { label: 'Period starts' }, { label: 'Fertile window' }, { label: 'Ovulation' }],
        r.cycles.map(function (c) {
          return {
            active: c.index === 1,
            cells: [
              String(c.index),
              esc(E.formatShortDate(c.periodStart)),
              esc(E.formatShortDate(c.fertileStart)) + ' – ' + esc(E.formatShortDate(c.fertileEnd)),
              esc(E.formatShortDate(c.ovulation))
            ]
          };
        })
      );

    html += callout('<strong>Ovulation timing varies.</strong> These dates assume a consistent cycle with a 14-day luteal phase. In practice ovulation shifts between cycles even for people with regular periods, so the fertile window is a probability, not a guarantee — in either direction.', 'warn');
    html += callout(DISCLAIMER);
    return html;
  };

  /* --------------------------- Pregnancy ---------------------------- */
  modules.pregnancy = function (form) {
    var method = radioValue(form, 'method') || 'lmp';
    var dateInput = $('#refDate', form);
    var date = E.parseISODate(dateInput.value);
    if (!date) {
      setError(dateInput, 'Choose a valid date.');
      return false;
    }
    var today = new Date(); today.setHours(0, 0, 0, 0);
    if (method !== 'dueDate' && date > today) {
      setError(dateInput, 'That date is in the future.');
      return false;
    }
    if (method === 'lmp' && E.daysBetween(date, today) > 320) {
      setError(dateInput, 'That is more than 45 weeks ago. Please check the date.');
      return false;
    }
    if (method === 'dueDate' && (E.daysBetween(today, date) > 300 || E.daysBetween(today, date) < -60)) {
      setError(dateInput, 'That due date is outside a plausible range.');
      return false;
    }
    clearError(dateInput);

    var cycleLength = num(form, 'cycleLength', { optional: true, min: 20, max: 45, unit: 'days' });
    if (cycleLength === null) return false;

    var r = E.calculatePregnancy({
      method: method, date: date, cycleLength: cycleLength === undefined ? 28 : cycleLength
    });

    var gestText = r.weeks < 0 ? 'Not yet started'
      : r.weeks + ' weeks' + (r.days ? ' ' + r.days + ' days' : '');

    var html = resultCard('Estimated due date', E.formatShortDate(r.edd), '', r.trimester,
      'You are approximately <strong>' + esc(gestText) + '</strong> pregnant' +
      (r.daysRemaining > 0 ? ', with about ' + r.daysRemaining + ' days to go.' : '.'));

    html += stats([
      { label: 'Gestational age', value: '<span style="font-size:.8em">' + esc(gestText) + '</span>' },
      { label: 'Estimated conception', value: '<span style="font-size:.72em">' + esc(E.formatShortDate(r.conception)) + '</span>' },
      { label: 'Progress', value: fmt(r.progressPct, 0), unit: '%' },
      { label: 'Full term begins', value: '<span style="font-size:.72em">' + esc(E.formatShortDate(r.termStart)) + '</span>' }
    ]);

    html += '<h3 class="mt-3">Milestone dates</h3>' +
      table(
        [{ label: 'Milestone' }, { label: 'Date' }, { label: 'What it means' }],
        r.milestones.map(function (m) {
          return {
            active: m.date >= today && (r.milestones.filter(function (x) { return x.date >= today; })[0] === m),
            cells: [esc(m.label), esc(E.formatShortDate(m.date)), esc(m.note)]
          };
        })
      );

    html += callout('<strong>Only about 4% of babies arrive on their estimated due date.</strong> Most births happen within two weeks either side. An early ultrasound is a more accurate dating method than the last menstrual period, so your clinician’s date takes precedence over this one.', 'warn');
    html += callout(DISCLAIMER);
    return html;
  };

  /* --------------------------- Bra size ----------------------------- */
  modules['bra-size'] = function (form) {
    var unit = radioValue(form, 'measureUnit') || 'cm';
    var under = num(form, 'underbust', { min: unit === 'cm' ? 55 : 22, max: unit === 'cm' ? 160 : 63, unit: unit });
    var bust = num(form, 'bust', { min: unit === 'cm' ? 60 : 24, max: unit === 'cm' ? 190 : 75, unit: unit });
    if (under === null || bust === null) return false;

    var underbustCm = unit === 'cm' ? under : E.convert.inToCm(under);
    var bustCm = unit === 'cm' ? bust : E.convert.inToCm(bust);
    var region = $('#region', form).value;

    var r = E.calculateBraSize({ underbustCm: underbustCm, bustCm: bustCm, region: region });
    if (r.error) {
      setError($('#bust', form), r.error);
      return false;
    }

    var html = resultCard('Your estimated size', esc(r.size), '', r.regionLabel,
      'Band ' + esc(r.band) + ', cup ' + esc(r.cup) + ' — a ' + fmt(r.differenceIn, 1) +
      ' in (' + fmt(r.differenceCm, 1) + ' cm) difference between bust and band.');

    html += stats([
      { label: 'Band size', value: esc(r.band) },
      { label: 'Cup size', value: esc(r.cup) },
      { label: 'Bust − band', value: fmt(r.differenceCm, 1), unit: 'cm' }
    ]);

    html += '<h3 class="mt-3">The same measurements in other systems</h3>' +
      table(
        [{ label: 'Sizing system' }, { label: 'Size' }],
        r.allRegions.map(function (x) {
          return { active: x.key === r.region, cells: [esc(x.label), '<strong>' + esc(x.size) + '</strong>'] };
        })
      );

    html += '<h3 class="mt-3">Sister sizes to try</h3>' +
      table(
        [{ label: 'Size' }, { label: 'Fit difference' }],
        r.sisterSizes.map(function (s) {
          return { cells: ['<strong>' + esc(s.size) + '</strong>', esc(s.note)] };
        })
      );

    html += callout('<strong>Sizing is not standardised.</strong> ' + esc(r.regionNote) +
      ' The same labelled size fits differently between brands, styles and even between two bras from one brand, so use this as a starting point for trying on rather than a fixed answer.');
    return html;
  };

  /* ================================================================== *
   * Form wiring
   * ================================================================== */
  function initCalculator() {
    var form = $('#calc-form');
    if (!form) return;
    var key = document.body.getAttribute('data-calc');
    var run = modules[key];
    if (!run) return;

    initUnits(form);
    initConditionalFields(form);

    form.addEventListener('submit', function (e) {
      e.preventDefault();
      clearAllErrors(form);
      var html;
      try {
        html = run(form);
      } catch (err) {
        if (window.console) console.error(err);
        html = false;
      }
      if (html === false || !html) {
        hideResult();
        announceInvalid(form, Math.max(1, countInvalid(form)));
        return;
      }
      showResult(form, html);
    });

    form.addEventListener('reset', function () {
      window.setTimeout(function () {
        clearAllErrors(form);
        hideResult();
        applyUnits(form, currentUnits(form));
        initConditionalFields(form, true);
      }, 0);
    });

    /* Clear a field's error as soon as the user starts fixing it */
    form.addEventListener('input', function (e) {
      if (e.target.matches('[aria-invalid="true"]')) clearError(e.target);
    });
  }

  /**
   * Fields that appear or disappear based on another control, declared in
   * markup as data-show-when="name:value1,value2".
   */
  function initConditionalFields(form, silent) {
    var conditionals = $$('[data-show-when]', form);
    if (!conditionals.length) return;

    function sync() {
      conditionals.forEach(function (node) {
        var parts = node.getAttribute('data-show-when').split(':');
        var name = parts[0];
        var allowed = parts[1].split(',');
        var value = radioValue(form, name) || (form.querySelector('#' + name) ? form.querySelector('#' + name).value : null);
        var show = allowed.indexOf(value) !== -1;
        node.hidden = !show;
        $$('input, select', node).forEach(function (f) {
          f.disabled = !show;
          if (!show) clearError(f);
        });
      });
    }

    if (!silent) {
      form.addEventListener('change', sync);
    }
    sync();
  }

  /* Populates the activity <select> from the MET dataset */
  function initActivitySelect() {
    var select = document.getElementById('activity');
    if (!select || !select.hasAttribute('data-met-source')) return;
    var groups = {};
    var order = [];
    D.ACTIVITIES.forEach(function (a) {
      if (!groups[a.g]) { groups[a.g] = []; order.push(a.g); }
      groups[a.g].push(a);
    });
    var html = '';
    order.forEach(function (g) {
      html += '<optgroup label="' + esc(g) + '">';
      groups[g].forEach(function (a) {
        html += '<option value="' + a.m + '">' + esc(a.l) + ' (MET ' + a.m + ')</option>';
      });
      html += '</optgroup>';
    });
    select.innerHTML = html;
    /* Sensible default: brisk walking */
    var defaultIndex = 0;
    $$('option', select).forEach(function (o, i) {
      if (o.textContent.indexOf('Walking, brisk') === 0) defaultIndex = i;
    });
    select.selectedIndex = defaultIndex;
  }

  /* Default today's date into date inputs that ask for it */
  function initDateDefaults() {
    $$('input[type="date"][data-max-today]').forEach(function (input) {
      var today = new Date();
      input.max = E.toISO(today);
    });
  }

  /* ------------------------------------------------------------------ *
   * Directory search + filter
   * ------------------------------------------------------------------ */
  function initDirectory() {
    var search = document.getElementById('calc-search');
    var grid = document.getElementById('calc-grid');
    if (!grid) return;
    var cards = $$('[data-keywords]', grid);
    var empty = document.getElementById('calc-empty');
    var chips = $$('.chip');
    var activeTag = 'all';

    function apply() {
      var q = search ? search.value.trim().toLowerCase() : '';
      var shown = 0;
      cards.forEach(function (card) {
        var hay = card.getAttribute('data-keywords').toLowerCase();
        var tags = card.getAttribute('data-tags') || '';
        var matchesText = !q || hay.indexOf(q) !== -1;
        var matchesTag = activeTag === 'all' || tags.indexOf(activeTag) !== -1;
        var show = matchesText && matchesTag;
        card.hidden = !show;
        if (show) shown++;
      });
      if (empty) empty.classList.toggle('is-visible', shown === 0);
    }

    if (search) search.addEventListener('input', apply);
    chips.forEach(function (chip) {
      chip.addEventListener('click', function () {
        activeTag = chip.getAttribute('data-tag');
        chips.forEach(function (c) { c.setAttribute('aria-pressed', String(c === chip)); });
        apply();
      });
    });
  }

  /* ------------------------------------------------------------------ *
   * Boot
   * ------------------------------------------------------------------ */
  function boot() {
    initTheme();
    initChrome();
    initActivitySelect();
    initDateDefaults();
    initCalculator();
    initDirectory();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', boot);
  } else {
    boot();
  }
})();
