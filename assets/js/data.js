/* ==========================================================================
   VitaCalc — static data tables
   Kept separate from both the engine and the UI so values can be updated
   without touching calculation or presentation code.

   MET values follow the 2011 Compendium of Physical Activities
   (Ainsworth et al.). Dataset version is stamped below and shown in the UI.
   ========================================================================== */
(function (global) {
  'use strict';

  var MET_DATASET_VERSION = '2011-compendium.r1';

  /* group | label | met */
  var ACTIVITIES = [
    /* --- Walking & running --- */
    { g: 'Walking & running', l: 'Walking, slow (3.2 km/h)', m: 2.8 },
    { g: 'Walking & running', l: 'Walking, moderate (4.8 km/h)', m: 3.5 },
    { g: 'Walking & running', l: 'Walking, brisk (5.6 km/h)', m: 4.3 },
    { g: 'Walking & running', l: 'Walking, very brisk (6.4 km/h)', m: 5.0 },
    { g: 'Walking & running', l: 'Walking uphill, 5% grade', m: 6.0 },
    { g: 'Walking & running', l: 'Hiking, cross country', m: 6.0 },
    { g: 'Walking & running', l: 'Jogging, general', m: 7.0 },
    { g: 'Walking & running', l: 'Running, 8 km/h (7:30 /km)', m: 8.3 },
    { g: 'Walking & running', l: 'Running, 9.7 km/h (6:12 /km)', m: 9.8 },
    { g: 'Walking & running', l: 'Running, 11.3 km/h (5:19 /km)', m: 11.0 },
    { g: 'Walking & running', l: 'Running, 12.9 km/h (4:39 /km)', m: 11.8 },
    { g: 'Walking & running', l: 'Running, 14.5 km/h (4:08 /km)', m: 12.8 },
    { g: 'Walking & running', l: 'Running, 16.1 km/h (3:44 /km)', m: 14.5 },
    { g: 'Walking & running', l: 'Stair climbing, fast', m: 8.8 },

    /* --- Cycling --- */
    { g: 'Cycling', l: 'Cycling, leisure (<16 km/h)', m: 4.0 },
    { g: 'Cycling', l: 'Cycling, light (16-19 km/h)', m: 6.8 },
    { g: 'Cycling', l: 'Cycling, moderate (19-22 km/h)', m: 8.0 },
    { g: 'Cycling', l: 'Cycling, vigorous (22-25 km/h)', m: 10.0 },
    { g: 'Cycling', l: 'Cycling, racing (25-30 km/h)', m: 12.0 },
    { g: 'Cycling', l: 'Mountain biking', m: 8.5 },
    { g: 'Cycling', l: 'Stationary bike, light', m: 5.5 },
    { g: 'Cycling', l: 'Stationary bike, moderate', m: 7.0 },
    { g: 'Cycling', l: 'Stationary bike, vigorous', m: 10.5 },
    { g: 'Cycling', l: 'Spinning class', m: 8.5 },

    /* --- Gym & conditioning --- */
    { g: 'Gym & conditioning', l: 'Weight training, light', m: 3.5 },
    { g: 'Gym & conditioning', l: 'Weight training, vigorous', m: 6.0 },
    { g: 'Gym & conditioning', l: 'Circuit training, general', m: 7.2 },
    { g: 'Gym & conditioning', l: 'Calisthenics, light', m: 3.8 },
    { g: 'Gym & conditioning', l: 'Calisthenics, vigorous (push-ups, burpees)', m: 8.0 },
    { g: 'Gym & conditioning', l: 'HIIT / interval training', m: 8.0 },
    { g: 'Gym & conditioning', l: 'Rowing machine, moderate', m: 7.0 },
    { g: 'Gym & conditioning', l: 'Rowing machine, vigorous', m: 8.5 },
    { g: 'Gym & conditioning', l: 'Elliptical trainer, moderate', m: 5.0 },
    { g: 'Gym & conditioning', l: 'Stair-stepper machine', m: 9.0 },
    { g: 'Gym & conditioning', l: 'Skipping rope, moderate', m: 11.8 },
    { g: 'Gym & conditioning', l: 'Kettlebell training', m: 8.0 },

    /* --- Mind & body --- */
    { g: 'Mind & body', l: 'Yoga, hatha', m: 2.5 },
    { g: 'Mind & body', l: 'Yoga, power / vinyasa', m: 4.0 },
    { g: 'Mind & body', l: 'Surya namaskar, brisk', m: 4.5 },
    { g: 'Mind & body', l: 'Pilates, general', m: 3.0 },
    { g: 'Mind & body', l: 'Stretching / mobility', m: 2.3 },
    { g: 'Mind & body', l: 'Tai chi', m: 3.0 },

    /* --- Sports --- */
    { g: 'Sports', l: 'Badminton, casual', m: 5.5 },
    { g: 'Sports', l: 'Badminton, competitive', m: 7.0 },
    { g: 'Sports', l: 'Basketball, general', m: 6.5 },
    { g: 'Sports', l: 'Cricket, batting / bowling', m: 4.8 },
    { g: 'Sports', l: 'Football (soccer), casual', m: 7.0 },
    { g: 'Sports', l: 'Football (soccer), competitive', m: 10.0 },
    { g: 'Sports', l: 'Table tennis', m: 4.0 },
    { g: 'Sports', l: 'Tennis, singles', m: 8.0 },
    { g: 'Sports', l: 'Tennis, doubles', m: 6.0 },
    { g: 'Sports', l: 'Volleyball, casual', m: 3.0 },
    { g: 'Sports', l: 'Boxing, sparring', m: 7.8 },
    { g: 'Sports', l: 'Martial arts / kickboxing', m: 10.3 },
    { g: 'Sports', l: 'Golf, walking with clubs', m: 4.8 },
    { g: 'Sports', l: 'Squash', m: 12.0 },

    /* --- Water --- */
    { g: 'Water activities', l: 'Swimming, leisurely', m: 6.0 },
    { g: 'Water activities', l: 'Swimming, freestyle moderate', m: 8.3 },
    { g: 'Water activities', l: 'Swimming, freestyle vigorous', m: 9.8 },
    { g: 'Water activities', l: 'Swimming, breaststroke', m: 10.3 },
    { g: 'Water activities', l: 'Water aerobics', m: 5.5 },
    { g: 'Water activities', l: 'Kayaking / rowing, moderate', m: 5.0 },

    /* --- Dance --- */
    { g: 'Dance', l: 'Dancing, general / social', m: 5.0 },
    { g: 'Dance', l: 'Dancing, aerobic / zumba', m: 7.3 },
    { g: 'Dance', l: 'Bhangra / garba, energetic', m: 7.8 },
    { g: 'Dance', l: 'Classical dance practice', m: 5.0 },
    { g: 'Dance', l: 'Aerobics, low impact', m: 5.0 },
    { g: 'Dance', l: 'Aerobics, high impact', m: 7.3 },

    /* --- Daily life --- */
    { g: 'Daily life & work', l: 'Sitting, desk work', m: 1.5 },
    { g: 'Daily life & work', l: 'Standing, light work', m: 2.5 },
    { g: 'Daily life & work', l: 'Cooking / kitchen work', m: 3.3 },
    { g: 'Daily life & work', l: 'Cleaning house, moderate', m: 3.5 },
    { g: 'Daily life & work', l: 'Mopping / scrubbing floors', m: 4.5 },
    { g: 'Daily life & work', l: 'Gardening, general', m: 3.8 },
    { g: 'Daily life & work', l: 'Carrying groceries upstairs', m: 7.5 },
    { g: 'Daily life & work', l: 'Childcare, active play', m: 4.0 },
    { g: 'Daily life & work', l: 'Shopping, walking', m: 2.3 },
    { g: 'Daily life & work', l: 'Construction / manual labour', m: 5.5 },
    { g: 'Daily life & work', l: 'Driving a car', m: 2.5 },
    { g: 'Daily life & work', l: 'Sleeping', m: 0.95 },

    /* --- Outdoors --- */
    { g: 'Outdoor & adventure', l: 'Rock climbing, ascending', m: 8.0 },
    { g: 'Outdoor & adventure', l: 'Trekking with a backpack', m: 7.8 },
    { g: 'Outdoor & adventure', l: 'Skating / rollerblading', m: 7.5 },
    { g: 'Outdoor & adventure', l: 'Skiing, downhill moderate', m: 5.3 },
    { g: 'Outdoor & adventure', l: 'Horse riding, trotting', m: 5.8 }
  ];

  /* Calculator metadata — powers the directory, search and related links.
     `href` values are root-relative for the live site. */
  var CALCULATORS = [
    {
      slug: 'bmi',
      title: 'BMI Calculator',
      short: 'BMI',
      tags: ['body composition'],
      keywords: 'bmi body mass index weight height obesity healthy weight range',
      blurb: 'Find your Body Mass Index and see which weight category it falls in.',
      icon: 'scale'
    },
    {
      slug: 'bmr',
      title: 'BMR Calculator',
      short: 'BMR',
      tags: ['energy'],
      keywords: 'bmr basal metabolic rate tdee maintenance calories mifflin st jeor harris benedict',
      blurb: 'Calculate the calories your body burns at complete rest, plus daily maintenance calories.',
      icon: 'flame'
    },
    {
      slug: 'ideal-weight',
      title: 'Ideal Weight Calculator',
      short: 'Ideal weight',
      tags: ['body composition'],
      keywords: 'ideal weight devine robinson miller hamwi healthy weight for height',
      blurb: 'Compare four clinical formulas for a reference weight at your height.',
      icon: 'target'
    },
    {
      slug: 'body-fat',
      title: 'Body Fat Calculator',
      short: 'Body fat',
      tags: ['body composition'],
      keywords: 'body fat percentage us navy method lean mass fat mass waist neck hip',
      blurb: 'Estimate body-fat percentage, fat mass and lean mass from tape measurements.',
      icon: 'body'
    },
    {
      slug: 'calories-burned',
      title: 'Calories Burned Calculator',
      short: 'Calories burned',
      tags: ['energy'],
      keywords: 'calories burned met activity exercise workout energy expenditure',
      blurb: 'Estimate the energy you burned across 80+ activities using MET values.',
      icon: 'bolt'
    },
    {
      slug: 'pace',
      title: 'Pace Calculator',
      short: 'Pace',
      tags: ['training'],
      keywords: 'pace running walking split finish time speed marathon 5k 10k',
      blurb: 'Solve for pace, finish time or distance, with a full split table.',
      icon: 'run'
    },
    {
      slug: 'period',
      title: 'Period Calculator',
      short: 'Period',
      tags: ["women's health"],
      keywords: 'period menstrual cycle ovulation fertile window next period tracker',
      blurb: 'Project your next six cycles, ovulation days and fertile windows.',
      icon: 'calendar'
    },
    {
      slug: 'pregnancy',
      title: 'Pregnancy Calculator',
      short: 'Pregnancy',
      tags: ["women's health"],
      keywords: 'pregnancy due date edd gestational age trimester naegele conception',
      blurb: 'Estimate your due date, current gestational age and milestone dates.',
      icon: 'heart'
    },
    {
      slug: 'bra-size',
      title: 'Bra Size Calculator',
      short: 'Bra size',
      tags: ["women's health"],
      keywords: 'bra size band cup underbust bust india uk us eu sister size',
      blurb: 'Convert bust and underbust measurements into band and cup sizes.',
      icon: 'ruler'
    }
  ];

  global.VitaData = {
    METS_VERSION: MET_DATASET_VERSION,
    ACTIVITIES: ACTIVITIES,
    CALCULATORS: CALCULATORS
  };

  if (typeof module === 'object' && module.exports) {
    module.exports = global.VitaData;
  }
})(typeof globalThis !== 'undefined' ? globalThis : this);
