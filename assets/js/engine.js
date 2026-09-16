/* ==========================================================================
   VitaCalc — calculation engine
   Pure, side-effect-free functions. No DOM access lives in this file.
   Every function takes canonical metric units (kg, cm, minutes, ISO dates)
   and returns plain objects, so each one can be unit-tested in isolation.

   Version: 1.0.0
   ========================================================================== */
(function (global) {
  'use strict';

  /* ------------------------------------------------------------------ *
   * Unit conversion (canonical internal units: kg, cm, km, minutes)
   * ------------------------------------------------------------------ */
  var LB_PER_KG = 2.2046226218;
  var CM_PER_IN = 2.54;
  var KM_PER_MI = 1.609344;

  var convert = {
    lbToKg: function (lb) { return lb / LB_PER_KG; },
    kgToLb: function (kg) { return kg * LB_PER_KG; },
    inToCm: function (inches) { return inches * CM_PER_IN; },
    cmToIn: function (cm) { return cm / CM_PER_IN; },
    ftInToCm: function (ft, inches) { return ((ft || 0) * 12 + (inches || 0)) * CM_PER_IN; },
    cmToFtIn: function (cm) {
      var totalIn = cm / CM_PER_IN;
      var ft = Math.floor(totalIn / 12);
      return { ft: ft, inches: totalIn - ft * 12 };
    },
    miToKm: function (mi) { return mi * KM_PER_MI; },
    kmToMi: function (km) { return km / KM_PER_MI; }
  };

  /* ------------------------------------------------------------------ *
   * Small numeric helpers
   * ------------------------------------------------------------------ */
  function round(value, decimals) {
    var f = Math.pow(10, decimals || 0);
    return Math.round((value + Number.EPSILON) * f) / f;
  }

  function clamp(value, min, max) {
    return Math.min(max, Math.max(min, value));
  }

  function isFiniteNumber(value) {
    return typeof value === 'number' && isFinite(value);
  }

  /* ------------------------------------------------------------------ *
   * 1. BMI — Body Mass Index
   *    BMI = weight(kg) / height(m)^2   (adults, 20+)
   * ------------------------------------------------------------------ */
  var BMI_CATEGORIES = [
    { key: 'underweight-severe', label: 'Severe thinness',   min: 0,    max: 16,   color: '#4E7FC4' },
    { key: 'underweight-mod',    label: 'Moderate thinness', min: 16,   max: 17,   color: '#6E9BD6' },
    { key: 'underweight-mild',   label: 'Mild thinness',     min: 17,   max: 18.5, color: '#93B9E6' },
    { key: 'normal',             label: 'Healthy weight',    min: 18.5, max: 25,   color: '#2F8A5B' },
    { key: 'overweight',         label: 'Overweight',        min: 25,   max: 30,   color: '#D9A227' },
    { key: 'obese-1',            label: 'Obese class I',     min: 30,   max: 35,   color: '#E8823C' },
    { key: 'obese-2',            label: 'Obese class II',    min: 35,   max: 40,   color: '#D9542F' },
    { key: 'obese-3',            label: 'Obese class III',   min: 40,   max: Infinity, color: '#B22E1F' }
  ];

  function bmiCategory(bmi) {
    for (var i = 0; i < BMI_CATEGORIES.length; i++) {
      if (bmi < BMI_CATEGORIES[i].max) return BMI_CATEGORIES[i];
    }
    return BMI_CATEGORIES[BMI_CATEGORIES.length - 1];
  }

  /**
   * @param {{weightKg:number, heightCm:number}} input
   * @returns {{bmi:number, category:object, healthyMinKg:number, healthyMaxKg:number, ponderal:number}}
   */
  function calculateBmi(input) {
    var m = input.heightCm / 100;
    var bmi = input.weightKg / (m * m);
    return {
      bmi: round(bmi, 1),
      bmiRaw: bmi,
      category: bmiCategory(bmi),
      healthyMinKg: round(18.5 * m * m, 1),
      healthyMaxKg: round(24.9 * m * m, 1),
      ponderal: round(input.weightKg / (m * m * m), 1)
    };
  }

  /* ------------------------------------------------------------------ *
   * 2. BMR — Basal Metabolic Rate + TDEE
   * ------------------------------------------------------------------ */
  var ACTIVITY_LEVELS = [
    { key: 'sedentary',   factor: 1.200, label: 'Sedentary',        hint: 'Little or no exercise, desk job' },
    { key: 'light',       factor: 1.375, label: 'Lightly active',   hint: 'Light exercise 1-3 days/week' },
    { key: 'moderate',    factor: 1.550, label: 'Moderately active', hint: 'Moderate exercise 3-5 days/week' },
    { key: 'very',        factor: 1.725, label: 'Very active',      hint: 'Hard exercise 6-7 days/week' },
    { key: 'extra',       factor: 1.900, label: 'Extra active',     hint: 'Physical job or twice-daily training' }
  ];

  var BMR_FORMULAS = {
    /* Mifflin-St Jeor (1990) — current default recommendation for adults */
    mifflin: function (i) {
      var base = 10 * i.weightKg + 6.25 * i.heightCm - 5 * i.age;
      return i.sex === 'male' ? base + 5 : base - 161;
    },
    /* Revised Harris-Benedict (Roza & Shizgal, 1984) */
    harris: function (i) {
      return i.sex === 'male'
        ? 88.362 + 13.397 * i.weightKg + 4.799 * i.heightCm - 5.677 * i.age
        : 447.593 + 9.247 * i.weightKg + 3.098 * i.heightCm - 4.330 * i.age;
    },
    /* Katch-McArdle — needs body-fat %, sex-independent */
    katch: function (i) {
      if (!isFiniteNumber(i.bodyFatPct)) return null;
      var lean = i.weightKg * (1 - i.bodyFatPct / 100);
      return 370 + 21.6 * lean;
    }
  };

  /**
   * @param {{sex:string, age:number, heightCm:number, weightKg:number,
   *          formula?:string, activityKey?:string, bodyFatPct?:number}} input
   */
  function calculateBmr(input) {
    var formulaKey = input.formula || 'mifflin';
    var fn = BMR_FORMULAS[formulaKey] || BMR_FORMULAS.mifflin;
    var bmr = fn(input);
    if (bmr === null) return null;

    var level = null;
    for (var i = 0; i < ACTIVITY_LEVELS.length; i++) {
      if (ACTIVITY_LEVELS[i].key === input.activityKey) level = ACTIVITY_LEVELS[i];
    }
    var factor = level ? level.factor : 1.2;

    return {
      bmr: Math.round(bmr),
      formula: formulaKey,
      activity: level,
      tdee: Math.round(bmr * factor),
      mildLoss: Math.round(bmr * factor - 250),
      weightLoss: Math.round(bmr * factor - 500),
      mildGain: Math.round(bmr * factor + 250),
      weightGain: Math.round(bmr * factor + 500),
      byLevel: ACTIVITY_LEVELS.map(function (l) {
        return { key: l.key, label: l.label, hint: l.hint, calories: Math.round(bmr * l.factor) };
      })
    };
  }

  /* ------------------------------------------------------------------ *
   * 3. Ideal weight
   * ------------------------------------------------------------------ */
  var IDEAL_FORMULAS = {
    devine: {
      label: 'Devine (1974)',
      note: 'The most widely used clinical reference, originally created for medication dosing.',
      fn: function (heightCm, sex) {
        var over60 = Math.max(0, convert.cmToIn(heightCm) - 60);
        return sex === 'male' ? 50 + 2.3 * over60 : 45.5 + 2.3 * over60;
      }
    },
    robinson: {
      label: 'Robinson (1983)',
      note: 'A modification of Devine that returns slightly lower values.',
      fn: function (heightCm, sex) {
        var over60 = Math.max(0, convert.cmToIn(heightCm) - 60);
        return sex === 'male' ? 52 + 1.9 * over60 : 49 + 1.7 * over60;
      }
    },
    miller: {
      label: 'Miller (1983)',
      note: 'Another Devine modification, flatter across the height range.',
      fn: function (heightCm, sex) {
        var over60 = Math.max(0, convert.cmToIn(heightCm) - 60);
        return sex === 'male' ? 56.2 + 1.41 * over60 : 53.1 + 1.36 * over60;
      }
    },
    hamwi: {
      label: 'Hamwi (1964)',
      note: 'The oldest of the four, still common in dietetics.',
      fn: function (heightCm, sex) {
        var over60 = Math.max(0, convert.cmToIn(heightCm) - 60);
        return sex === 'male' ? 48 + 2.7 * over60 : 45.5 + 2.2 * over60;
      }
    }
  };

  /**
   * @param {{heightCm:number, sex:string, formula?:string}} input
   */
  function calculateIdealWeight(input) {
    var key = input.formula || 'devine';
    var chosen = IDEAL_FORMULAS[key] || IDEAL_FORMULAS.devine;
    var m = input.heightCm / 100;

    var all = Object.keys(IDEAL_FORMULAS).map(function (k) {
      return {
        key: k,
        label: IDEAL_FORMULAS[k].label,
        note: IDEAL_FORMULAS[k].note,
        weightKg: round(IDEAL_FORMULAS[k].fn(input.heightCm, input.sex), 1)
      };
    });

    return {
      formulaKey: key,
      formulaLabel: chosen.label,
      idealKg: round(chosen.fn(input.heightCm, input.sex), 1),
      healthyMinKg: round(18.5 * m * m, 1),
      healthyMaxKg: round(24.9 * m * m, 1),
      allFormulas: all
    };
  }

  /* ------------------------------------------------------------------ *
   * 4. Body fat — US Navy circumference method + BMI fallback method
   *    All logs are base 10, all measurements in cm.
   * ------------------------------------------------------------------ */
  var BODY_FAT_RANGES = {
    male: [
      { key: 'essential',  label: 'Essential fat', min: 0,  max: 6,  color: '#4E7FC4' },
      { key: 'athletic',   label: 'Athletes',      min: 6,  max: 14, color: '#2F8A5B' },
      { key: 'fitness',    label: 'Fitness',       min: 14, max: 18, color: '#5EA97D' },
      { key: 'average',    label: 'Average',       min: 18, max: 25, color: '#D9A227' },
      { key: 'obese',      label: 'Obese',         min: 25, max: Infinity, color: '#D9542F' }
    ],
    female: [
      { key: 'essential',  label: 'Essential fat', min: 0,  max: 14, color: '#4E7FC4' },
      { key: 'athletic',   label: 'Athletes',      min: 14, max: 21, color: '#2F8A5B' },
      { key: 'fitness',    label: 'Fitness',       min: 21, max: 25, color: '#5EA97D' },
      { key: 'average',    label: 'Average',       min: 25, max: 32, color: '#D9A227' },
      { key: 'obese',      label: 'Obese',         min: 32, max: Infinity, color: '#D9542F' }
    ]
  };

  function bodyFatCategory(pct, sex) {
    var ranges = BODY_FAT_RANGES[sex] || BODY_FAT_RANGES.male;
    for (var i = 0; i < ranges.length; i++) {
      if (pct < ranges[i].max) return ranges[i];
    }
    return ranges[ranges.length - 1];
  }

  /**
   * US Navy method.
   * Men:   495 / (1.0324 - 0.19077*log10(waist - neck) + 0.15456*log10(height)) - 450
   * Women: 495 / (1.29579 - 0.35004*log10(waist + hip - neck) + 0.22100*log10(height)) - 450
   * (measurements in cm)
   * @param {{sex:string, heightCm:number, neckCm:number, waistCm:number,
   *          hipCm?:number, weightKg?:number, age?:number}} input
   */
  function calculateBodyFat(input) {
    var log10 = function (v) { return Math.log(v) / Math.LN10; };
    var pct;

    if (input.sex === 'male') {
      var mGirth = input.waistCm - input.neckCm;
      if (mGirth <= 0) return { error: 'Waist must be larger than neck measurement.' };
      pct = 495 / (1.0324 - 0.19077 * log10(mGirth) + 0.15456 * log10(input.heightCm)) - 450;
    } else {
      var fGirth = input.waistCm + input.hipCm - input.neckCm;
      if (fGirth <= 0) return { error: 'Waist plus hip must be larger than neck measurement.' };
      pct = 495 / (1.29579 - 0.35004 * log10(fGirth) + 0.22100 * log10(input.heightCm)) - 450;
    }

    if (!isFiniteNumber(pct) || pct <= 0 || pct > 75) {
      return { error: 'Those measurements produce an impossible result. Please re-check them.' };
    }

    var out = {
      bodyFatPct: round(pct, 1),
      category: bodyFatCategory(pct, input.sex),
      method: 'US Navy circumference method'
    };

    if (isFiniteNumber(input.weightKg) && input.weightKg > 0) {
      out.fatMassKg = round(input.weightKg * pct / 100, 1);
      out.leanMassKg = round(input.weightKg * (1 - pct / 100), 1);
      /* BMI method (Deurenberg) as a cross-check when height + weight + age exist */
      if (isFiniteNumber(input.age)) {
        var bmi = input.weightKg / Math.pow(input.heightCm / 100, 2);
        var sexFlag = input.sex === 'male' ? 1 : 0;
        out.bmiMethodPct = round(1.20 * bmi + 0.23 * input.age - 10.8 * sexFlag - 5.4, 1);
      }
    }
    return out;
  }

  /* ------------------------------------------------------------------ *
   * 5. Calories burned — MET method
   *    kcal/min = MET * 3.5 * weightKg / 200
   * ------------------------------------------------------------------ */
  /**
   * @param {{met:number, weightKg:number, minutes:number, activityLabel?:string}} input
   */
  function calculateCaloriesBurned(input) {
    var perMinute = input.met * 3.5 * input.weightKg / 200;
    var total = perMinute * input.minutes;
    return {
      total: Math.round(total),
      totalRaw: total,
      perMinute: round(perMinute, 1),
      perHour: Math.round(perMinute * 60),
      met: input.met,
      minutes: input.minutes,
      /* 1 kg body fat ~ 7700 kcal; 1 lb ~ 3500 kcal */
      fatEquivalentG: Math.round(total / 7.7),
      metMinutes: Math.round(input.met * input.minutes),
      activityLabel: input.activityLabel || ''
    };
  }

  /* ------------------------------------------------------------------ *
   * 6. Pace — solve for whichever value is unknown
   * ------------------------------------------------------------------ */
  function hmsToSeconds(h, m, s) {
    return (h || 0) * 3600 + (m || 0) * 60 + (s || 0);
  }

  function secondsToHms(totalSeconds) {
    var t = Math.max(0, Math.round(totalSeconds));
    return {
      h: Math.floor(t / 3600),
      m: Math.floor((t % 3600) / 60),
      s: t % 60,
      total: t
    };
  }

  function formatDuration(totalSeconds) {
    var t = secondsToHms(totalSeconds);
    var pad = function (n) { return n < 10 ? '0' + n : String(n); };
    return t.h > 0
      ? t.h + ':' + pad(t.m) + ':' + pad(t.s)
      : t.m + ':' + pad(t.s);
  }

  var COMMON_DISTANCES = [
    { label: '1 km',          km: 1 },
    { label: '1 mile',        km: KM_PER_MI },
    { label: '5K',            km: 5 },
    { label: '10K',           km: 10 },
    { label: 'Half marathon', km: 21.0975 },
    { label: 'Marathon',      km: 42.195 }
  ];

  /**
   * Provide exactly two of { distanceKm, timeSeconds, paceSecPerKm } and set
   * `solveFor` to the third.
   * @param {{solveFor:string, distanceKm?:number, timeSeconds?:number, paceSecPerKm?:number}} input
   */
  function calculatePace(input) {
    var distanceKm = input.distanceKm;
    var timeSeconds = input.timeSeconds;
    var paceSecPerKm = input.paceSecPerKm;

    if (input.solveFor === 'time') {
      timeSeconds = distanceKm * paceSecPerKm;
    } else if (input.solveFor === 'distance') {
      distanceKm = timeSeconds / paceSecPerKm;
    } else {
      paceSecPerKm = timeSeconds / distanceKm;
    }

    if (!isFiniteNumber(paceSecPerKm) || paceSecPerKm <= 0) {
      return { error: 'Those values do not produce a valid pace.' };
    }

    var speedKmh = 3600 / paceSecPerKm;
    return {
      distanceKm: distanceKm,
      timeSeconds: timeSeconds,
      paceSecPerKm: paceSecPerKm,
      paceSecPerMi: paceSecPerKm * KM_PER_MI,
      speedKmh: round(speedKmh, 2),
      speedMph: round(convert.kmToMi(speedKmh), 2),
      splits: COMMON_DISTANCES.map(function (d) {
        return { label: d.label, km: d.km, seconds: d.km * paceSecPerKm };
      })
    };
  }

  /* ------------------------------------------------------------------ *
   * Date helpers (UTC-safe: dates are built from Y/M/D, never parsed
   * from ambiguous strings, so timezone never shifts a result by a day)
   * ------------------------------------------------------------------ */
  function parseISODate(value) {
    if (!value) return null;
    var parts = String(value).split('-');
    if (parts.length !== 3) return null;
    var y = parseInt(parts[0], 10);
    var mo = parseInt(parts[1], 10);
    var d = parseInt(parts[2], 10);
    if (!y || !mo || !d) return null;
    var date = new Date(y, mo - 1, d);
    /* Rejects things like 2025-02-30 that JS would otherwise roll over */
    if (date.getFullYear() !== y || date.getMonth() !== mo - 1 || date.getDate() !== d) return null;
    date.setHours(0, 0, 0, 0);
    return date;
  }

  function addDays(date, days) {
    var d = new Date(date.getTime());
    d.setDate(d.getDate() + days);
    d.setHours(0, 0, 0, 0);
    return d;
  }

  function daysBetween(a, b) {
    var ms = 86400000;
    var a0 = new Date(a.getFullYear(), a.getMonth(), a.getDate()).getTime();
    var b0 = new Date(b.getFullYear(), b.getMonth(), b.getDate()).getTime();
    return Math.round((b0 - a0) / ms);
  }

  function toISO(date) {
    var pad = function (n) { return n < 10 ? '0' + n : String(n); };
    return date.getFullYear() + '-' + pad(date.getMonth() + 1) + '-' + pad(date.getDate());
  }

  function formatLongDate(date) {
    var months = ['January', 'February', 'March', 'April', 'May', 'June',
      'July', 'August', 'September', 'October', 'November', 'December'];
    var days = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'];
    return days[date.getDay()] + ', ' + date.getDate() + ' ' + months[date.getMonth()] + ' ' + date.getFullYear();
  }

  function formatShortDate(date) {
    var months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
    return date.getDate() + ' ' + months[date.getMonth()] + ' ' + date.getFullYear();
  }

  /* ------------------------------------------------------------------ *
   * 7. Period / menstrual cycle
   *    Ovulation is estimated as (next period - luteal phase length).
   *    Fertile window = ovulation - 5 days ... ovulation + 1 day.
   * ------------------------------------------------------------------ */
  /**
   * @param {{lmp:Date, cycleLength:number, periodLength?:number,
   *          lutealLength?:number, cycles?:number}} input
   */
  function calculatePeriod(input) {
    var cycleLength = input.cycleLength;
    var periodLength = input.periodLength || 5;
    var luteal = input.lutealLength || 14;
    var count = input.cycles || 6;
    var cycles = [];

    for (var i = 1; i <= count; i++) {
      var start = addDays(input.lmp, cycleLength * i);
      var ovulation = addDays(start, -luteal);
      cycles.push({
        index: i,
        periodStart: start,
        periodEnd: addDays(start, periodLength - 1),
        ovulation: ovulation,
        fertileStart: addDays(ovulation, -5),
        fertileEnd: addDays(ovulation, 1)
      });
    }

    var today = new Date();
    today.setHours(0, 0, 0, 0);
    var currentDay = daysBetween(input.lmp, today) % cycleLength;
    if (currentDay < 0) currentDay += cycleLength;

    return {
      next: cycles[0],
      cycles: cycles,
      cycleDay: currentDay + 1,
      daysUntilNext: daysBetween(today, cycles[0].periodStart),
      periodLength: periodLength,
      cycleLength: cycleLength
    };
  }

  /* ------------------------------------------------------------------ *
   * 8. Pregnancy — Naegele's rule with cycle-length adjustment
   *    EDD = LMP + 280 days + (cycleLength - 28)
   * ------------------------------------------------------------------ */
  var MILESTONES = [
    { day: 28,  label: 'End of week 4', note: 'A pregnancy test is usually positive by now.' },
    { day: 56,  label: 'End of week 8', note: 'Most major organs have started forming.' },
    { day: 84,  label: 'End of first trimester', note: 'Week 12 complete. Miscarriage risk drops notably.' },
    { day: 140, label: 'Anatomy scan window', note: 'Week 20. The detailed anomaly scan is usually done around now.' },
    { day: 168, label: 'Viability milestone', note: 'Week 24. Survival outside the womb becomes possible with intensive care.' },
    { day: 189, label: 'End of second trimester', note: 'Week 27 complete.' },
    { day: 259, label: 'Full term begins', note: 'Week 37. Birth from here on is considered term.' },
    { day: 280, label: 'Estimated due date', note: 'Week 40. Only about 1 in 20 babies arrive exactly on this date.' }
  ];

  /**
   * @param {{method:string, date:Date, cycleLength?:number}} input
   *   method: 'lmp' | 'conception' | 'dueDate'
   */
  function calculatePregnancy(input) {
    var cycleLength = input.cycleLength || 28;
    var lmp;

    if (input.method === 'conception') {
      /* Conception is taken as ovulation; LMP sits (cycleLength - 14) days earlier */
      lmp = addDays(input.date, -(cycleLength - 14));
    } else if (input.method === 'dueDate') {
      lmp = addDays(input.date, -280);
    } else {
      lmp = input.date;
    }

    var adjustment = input.method === 'lmp' ? (cycleLength - 28) : 0;
    var edd = addDays(lmp, 280 + adjustment);
    var conception = addDays(lmp, cycleLength - 14);

    var today = new Date();
    today.setHours(0, 0, 0, 0);
    var gestDays = daysBetween(addDays(lmp, adjustment), today);
    var weeks = Math.floor(gestDays / 7);
    var days = gestDays - weeks * 7;

    var trimester;
    if (weeks < 0) trimester = 'Not started yet';
    else if (weeks < 13) trimester = 'First trimester';
    else if (weeks < 27) trimester = 'Second trimester';
    else trimester = 'Third trimester';

    return {
      lmp: lmp,
      edd: edd,
      conception: conception,
      gestationalDays: gestDays,
      weeks: weeks,
      days: days,
      trimester: trimester,
      daysRemaining: daysBetween(today, edd),
      progressPct: clamp(round(gestDays / 280 * 100, 1), 0, 100),
      termStart: addDays(lmp, 259 + adjustment),
      trimester2Start: addDays(lmp, 91 + adjustment),
      trimester3Start: addDays(lmp, 189 + adjustment),
      milestones: MILESTONES.map(function (m) {
        return { label: m.label, note: m.note, date: addDays(lmp, m.day + adjustment), day: m.day };
      })
    };
  }

  /* ------------------------------------------------------------------ *
   * 9. Bra size — region-specific rule sets driven by data tables
   * ------------------------------------------------------------------ */
  /* Cup letters by difference. Index = step count above band. */
  var CUP_SCALES = {
    'uk':    ['AA', 'A', 'B', 'C', 'D', 'DD', 'E', 'F', 'FF', 'G', 'GG', 'H', 'HH', 'J', 'JJ', 'K'],
    'us':    ['AA', 'A', 'B', 'C', 'D', 'DD', 'DDD', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O'],
    'eu':    ['AA', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O'],
    'india': ['AA', 'A', 'B', 'C', 'D', 'DD', 'E', 'F', 'FF', 'G', 'GG', 'H', 'HH', 'J', 'JJ', 'K']
  };

  var REGIONS = {
    india: { label: 'India / UK sizing', note: 'Indian retail mostly follows UK band and cup conventions.' },
    uk:    { label: 'UK sizing',         note: 'UK cups run AA, A, B, C, D, DD, E, F, FF, G...' },
    us:    { label: 'US sizing',         note: 'US cups run AA, A, B, C, D, DD, DDD, then G upward.' },
    eu:    { label: 'EU sizing (cm)',    note: 'EU band numbers are centimetres and step in fives; EU cups skip the doubled letters.' }
  };

  /* Band label per region for a given band measurement in inches.
     EU bands follow the standard conversion chart: UK 28/30/32/34 -> EU 60/65/70/75,
     i.e. EU = UK inches x 2.5 - 10. Deriving every region from one band-and-step
     pair is what keeps the four systems mutually consistent. */
  function bandLabelFor(regionKey, bandIn) {
    return regionKey === 'eu' ? String(bandIn * 2.5 - 10) : String(bandIn);
  }

  function cupFor(regionKey, step) {
    var scale = CUP_SCALES[regionKey] || CUP_SCALES.india;
    return scale[Math.min(Math.max(step, 0), scale.length - 1)];
  }

  /**
   * @param {{underbustCm:number, bustCm:number, region?:string}} input
   */
  function calculateBraSize(input) {
    var regionKey = REGIONS[input.region] ? input.region : 'india';
    var region = REGIONS[regionKey];
    var underbustIn = convert.cmToIn(input.underbustCm);
    var bustIn = convert.cmToIn(input.bustCm);

    if (bustIn <= underbustIn) {
      return { error: 'Bust measurement should be larger than the underbust measurement.' };
    }

    /* Band: underbust in inches, rounded to the nearest even number.
       This is the modern fitting method -- no "+4 inches" is added. */
    var bandIn = clamp(Math.round(underbustIn / 2) * 2, 28, 54);

    /* Cup: one letter per inch of difference between bust and band. */
    var diff = bustIn - bandIn;
    var step = Math.max(0, Math.round(diff));

    var bandLabel = bandLabelFor(regionKey, bandIn);
    var cup = cupFor(regionKey, step);

    /* Sister sizes hold roughly the same cup volume on a different band. */
    var downIn = Math.max(28, bandIn - 2);
    var upIn = Math.min(54, bandIn + 2);

    return {
      region: regionKey,
      regionLabel: region.label,
      regionNote: region.note,
      band: bandLabel,
      cup: cup,
      size: bandLabel + cup,
      bandIn: bandIn,
      differenceIn: round(diff, 1),
      differenceCm: round(diff * CM_PER_IN, 1),
      cupIndex: step,
      sisterSizes: [
        { size: bandLabelFor(regionKey, downIn) + cupFor(regionKey, step + 1), note: 'Tighter band, roomier cup' },
        { size: bandLabelFor(regionKey, upIn) + cupFor(regionKey, step - 1), note: 'Looser band, smaller cup' }
      ],
      allRegions: Object.keys(REGIONS).map(function (k) {
        return {
          key: k,
          label: REGIONS[k].label,
          size: bandLabelFor(k, bandIn) + cupFor(k, step)
        };
      })
    };
  }

  /* ------------------------------------------------------------------ *
   * Public API
   * ------------------------------------------------------------------ */
  global.VitaEngine = {
    version: '1.0.0',
    convert: convert,
    round: round,
    clamp: clamp,
    isFiniteNumber: isFiniteNumber,

    BMI_CATEGORIES: BMI_CATEGORIES,
    BODY_FAT_RANGES: BODY_FAT_RANGES,
    ACTIVITY_LEVELS: ACTIVITY_LEVELS,
    IDEAL_FORMULAS: IDEAL_FORMULAS,
    COMMON_DISTANCES: COMMON_DISTANCES,
    CUP_SCALES: CUP_SCALES,
    REGIONS: REGIONS,

    bmiCategory: bmiCategory,
    bodyFatCategory: bodyFatCategory,

    calculateBmi: calculateBmi,
    calculateBmr: calculateBmr,
    calculateIdealWeight: calculateIdealWeight,
    calculateBodyFat: calculateBodyFat,
    calculateCaloriesBurned: calculateCaloriesBurned,
    calculatePace: calculatePace,
    calculatePeriod: calculatePeriod,
    calculatePregnancy: calculatePregnancy,
    calculateBraSize: calculateBraSize,

    hmsToSeconds: hmsToSeconds,
    secondsToHms: secondsToHms,
    formatDuration: formatDuration,
    parseISODate: parseISODate,
    addDays: addDays,
    daysBetween: daysBetween,
    toISO: toISO,
    formatLongDate: formatLongDate,
    formatShortDate: formatShortDate
  };

  if (typeof module === 'object' && module.exports) {
    module.exports = global.VitaEngine;
  }
})(typeof globalThis !== 'undefined' ? globalThis : this);
