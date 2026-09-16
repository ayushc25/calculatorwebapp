# -*- coding: utf-8 -*-
"""How-it-is-calculated blocks for each calculator.

These replace the monospace <pre> blocks the pages used to carry. A formula
is set in the body typeface with the quantities the visitor actually types
highlighted; a procedure is a numbered list in plain language; values that
are data rather than maths are shown as a small table. Every block is
followed by a worked example using round numbers.
"""

from parts import DIV, MINUS, PLUS, TIMES, equation, procedure, ref_table, var, worked

# --------------------------------------------------------------------- BMI
EQ_BMI = equation(
    [('BMI', '%s %s %s&sup2;' % (var('your weight in kilograms'), DIV,
                                 var('your height in metres')))],
    tag='The formula',
    caption='Height is squared because weight grows roughly with the square of height across '
            'a population, not in direct proportion to it.',
) + worked(
    'At <b>70 kg</b> and <b>1.75 m</b>: 1.75 &times; 1.75 = 3.06, then 70 &divide; 3.06 = '
    '<b>BMI 22.9</b> &mdash; inside the healthy band of 18.5 to 24.9.'
) + '<p>Working in pounds and inches, the same calculation is <strong>703 &times; weight (lb) &divide; height (in)&sup2;</strong>. The 703 is only there to convert the units, so both routes give the same number.</p>'

# --------------------------------------------------------------------- BMR
def _mifflin(tail):
    return '10 %s %s %s 6.25 %s %s %s 5 %s %s %s' % (
        TIMES, var('weight in kg'), PLUS, TIMES, var('height in cm'), MINUS,
        TIMES, var('age'), tail)


EQ_BMR_MIFFLIN = equation(
    [
        ('BMR, men', _mifflin('%s 5' % PLUS)),
        ('BMR, women', _mifflin('%s 161' % MINUS)),
    ],
    tag='Mifflin-St Jeor (1990)',
    caption='The two versions differ only in the final constant &mdash; everything before it is identical.',
) + worked(
    'A 30-year-old man, <b>80 kg</b> at <b>180 cm</b>: 800 + 1,125 &minus; 150 + 5 = '
    '<b>1,780 kcal a day</b> at complete rest.'
)

EQ_BMR_HARRIS = equation(
    [
        ('BMR, men', '88.362 %s 13.397 %s %s %s 4.799 %s %s %s 5.677 %s %s' % (
            PLUS, TIMES, var('weight in kg'), PLUS, TIMES, var('height in cm'),
            MINUS, TIMES, var('age'))),
        ('BMR, women', '447.593 %s 9.247 %s %s %s 3.098 %s %s %s 4.330 %s %s' % (
            PLUS, TIMES, var('weight in kg'), PLUS, TIMES, var('height in cm'),
            MINUS, TIMES, var('age'))),
    ],
    tag='Revised Harris-Benedict (1984)',
)

EQ_BMR_KATCH = equation(
    [
        ('Lean body mass', '%s %s (100%% %s %s) %s 100' % (
            var('weight in kg'), TIMES, MINUS, var('body fat percentage'), DIV)),
        ('BMR', '370 %s 21.6 %s lean body mass' % (PLUS, TIMES)),
    ],
    tag='Katch-McArdle',
    caption='Sex does not appear anywhere in this one: lean mass already carries that information.',
) + worked(
    'Someone <b>80 kg</b> at <b>20% body fat</b> carries 64 kg of lean mass, so '
    '370 + (21.6 &times; 64) = <b>1,752 kcal a day</b>.'
)

TBL_ACTIVITY = ref_table(
    'Activity multipliers used to turn BMR into daily maintenance calories',
    [('Activity level', False), ('Typical week', False), ('Multiplier', True)],
    [
        ('Sedentary', 'Little or no exercise, desk job', '&times; 1.20'),
        ('Lightly active', 'Light exercise 1&ndash;3 days a week', '&times; 1.375'),
        ('Moderately active', 'Moderate exercise 3&ndash;5 days a week', '&times; 1.55'),
        ('Very active', 'Hard exercise 6&ndash;7 days a week', '&times; 1.725'),
        ('Extra active', 'Physical job or twice-daily training', '&times; 1.90'),
    ],
)

# ------------------------------------------------------------ Ideal weight
TBL_IDEAL = ref_table(
    'What each formula adds for every inch above five feet',
    [('Formula', False), ('Men', False), ('Women', False)],
    [
        ('Devine (1974)', '50.0 kg + 2.30 kg/in', '45.5 kg + 2.30 kg/in'),
        ('Robinson (1983)', '52.0 kg + 1.90 kg/in', '49.0 kg + 1.70 kg/in'),
        ('Miller (1983)', '56.2 kg + 1.41 kg/in', '53.1 kg + 1.36 kg/in'),
        ('Hamwi (1964)', '48.0 kg + 2.70 kg/in', '45.5 kg + 2.20 kg/in'),
    ],
) + worked(
    'A man of <b>5 ft 10 in</b> is 10 inches above five feet, so Devine gives '
    '50.0 + (10 &times; 2.30) = <b>73 kg</b>, while Robinson gives <b>71 kg</b> and Hamwi <b>75 kg</b>. '
    'That four-kilogram spread between published formulas is the point: there is no single ideal weight.'
)

# ---------------------------------------------------------------- Body fat
EQ_BODYFAT = equation(
    [
        ('Body fat %, men',
         '495 %s (1.0324 %s 0.19077 %s log(%s %s %s) %s 0.15456 %s log(%s)) %s 450' % (
             DIV, MINUS, TIMES, var('waist'), MINUS, var('neck'), PLUS, TIMES,
             var('height'), MINUS)),
        ('Body fat %, women',
         '495 %s (1.29579 %s 0.35004 %s log(%s %s %s %s %s) %s 0.22100 %s log(%s)) %s 450' % (
             DIV, MINUS, TIMES, var('waist'), PLUS, var('hips'), MINUS, var('neck'),
             PLUS, TIMES, var('height'), MINUS)),
    ],
    tag='US Navy circumference method',
    caption='All measurements in centimetres; log is base 10. You never have to work this out '
            'yourself &mdash; it is here so you can see exactly what the page is doing.',
) + worked(
    'A man <b>180 cm</b> tall with a <b>38 cm</b> neck and <b>85 cm</b> waist comes out around '
    '<b>17% body fat</b>. Add your weight and the page also splits that into fat mass and lean mass.'
)

# --------------------------------------------------------- Calories burned
EQ_CALORIES = equation(
    [
        ('Calories per minute', '%s %s 3.5 %s %s %s 200' % (
            var('MET value'), TIMES, TIMES, var('your weight in kg'), DIV)),
        ('Calories burned', 'calories per minute %s %s' % (TIMES, var('minutes of activity'))),
    ],
    tag='The MET method',
    caption='One MET is the energy you use sitting quietly. An activity rated at 8 METs costs '
            'eight times that much.',
) + worked(
    'Half an hour of swimming (8 METs) at <b>70 kg</b>: 8 &times; 3.5 &times; 70 &divide; 200 = '
    '9.8 calories a minute, so 9.8 &times; 30 = <b>294 calories</b>.'
)

# -------------------------------------------------------------------- Pace
EQ_PACE = equation(
    [
        ('Pace', '%s %s %s' % (var('time'), DIV, var('distance'))),
        ('Finish time', '%s %s %s' % (var('pace'), TIMES, var('distance'))),
        ('Distance', '%s %s %s' % (var('time'), DIV, var('pace'))),
    ],
    tag='One relationship, rearranged three ways',
    caption='Speed follows from the same figure: 3,600 &divide; pace in seconds per kilometre '
            'gives kilometres per hour.',
) + worked(
    '<b>10 km</b> in <b>50 minutes</b> is 3,000 seconds &divide; 10 = 300 seconds per kilometre, '
    'or <b>5:00 /km</b> &mdash; which is 8:03 per mile and 12.0 km/h.'
)

TBL_DISTANCES = ref_table(
    'Standard race distances',
    [('Race', False), ('Kilometres', True), ('Miles', True)],
    [
        ('5K', '5.000', '3.107'),
        ('10K', '10.000', '6.214'),
        ('Half marathon', '21.0975', '13.109'),
        ('Marathon', '42.195', '26.219'),
    ],
)

# ------------------------------------------------------------------ Period
STEPS_PERIOD = procedure([
    ('When your next period starts',
     'The first day of your last period %s %s' % (PLUS, var('your cycle length')),
     'On a 28-day cycle, that is 28 days after bleeding last began.'),
    ('When you probably ovulate',
     'That next period date %s 14 days' % MINUS,
     'Counted <b>backwards</b> from the next period, not forwards from the last one &mdash; '
     'see why below.'),
    ('Your fertile window',
     'From 5 days before ovulation until 1 day after it',
     'Six days in total, because sperm can survive up to five days and an egg about a day.'),
])

WORKED_PERIOD = worked(
    'Last period started <b>1 September</b>, cycle length <b>28 days</b>. Next period: '
    '<b>29 September</b>. Ovulation: <b>15 September</b>. Fertile window: '
    '<b>10&ndash;16 September</b>.'
)

# --------------------------------------------------------------- Pregnancy
STEPS_PREGNANCY = procedure([
    ('Your estimated due date',
     'The first day of your last period %s 280 days (40 weeks)' % PLUS,
     'This is Naegele&rsquo;s rule, the standard clinical starting point.'),
    ('Adjusted for your cycle length',
     'Add %s %s 28 days' % (var('your cycle length'), MINUS),
     'A 35-day cycle moves the due date a week later, because ovulation happened a week later.'),
    ('How far along you are today',
     'Days since that starting point, shown as weeks and days',
     'Which is why a positive test usually lands you at &ldquo;4 weeks pregnant&rdquo; already.'),
])

WORKED_PREGNANCY = worked(
    'Last period <b>1 January</b> on a <b>28-day</b> cycle gives a due date of '
    '<b>8 October</b>. On a <b>35-day</b> cycle the same start date gives <b>15 October</b>.'
)

TBL_TRIMESTERS = ref_table(
    'How the weeks are grouped',
    [('Stage', False), ('Weeks', False)],
    [
        ('First trimester', 'Week 0 to the end of week 12'),
        ('Second trimester', 'Week 13 to the end of week 26'),
        ('Third trimester', 'Week 27 until birth'),
        ('Full term begins', 'Week 37'),
    ],
)

# ---------------------------------------------------------------- Bra size
STEPS_BRA = procedure([
    ('Your band size',
     'Your %s in inches, rounded to the nearest even number' % var('underbust measurement'),
     'Nothing is added. The old advice to add four or five inches is what leaves so many '
     'people in a band far too loose.'),
    ('Your cup size',
     '%s %s %s, one cup letter per inch of difference' % (
         var('bust measurement'), MINUS, 'band size'),
     'One inch of difference is an A cup, two inches a B, four inches a D, and so on.'),
    ('The same size in another system',
     'The band and cup step stay the same; only the labels change',
     'EU band numbers are the inch band &times; 2.5 &minus; 10, so a UK 34 is an EU 75. '
     'EU and US cup letters then diverge from UK above a D.'),
])

WORKED_BRA = worked(
    'An underbust of <b>78 cm</b> is 30.7 inches, so the band is <b>30</b>. A bust of '
    '<b>92 cm</b> is 36.2 inches, six inches more than the band &mdash; a <b>UK 30E</b>, '
    'which is a US 30DDD and an EU 65F.'
)
