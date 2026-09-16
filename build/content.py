# -*- coding: utf-8 -*-
"""Page content for every VitaCalc calculator.

Each entry drives one crawlable page at /calculators/<slug>/.
Keep copy, formulas and FAQ text here; markup helpers live in parts.py.
"""

from parts import (actions, date_field, height_field, length_field, number,
                   segmented, select, sex_field, units_toggle, weight_field)
from methods import (EQ_BMI, EQ_BMR_HARRIS, EQ_BMR_KATCH, EQ_BMR_MIFFLIN,
                     EQ_BODYFAT, EQ_CALORIES, EQ_PACE, STEPS_BRA, STEPS_PERIOD,
                     STEPS_PREGNANCY, TBL_ACTIVITY, TBL_DISTANCES, TBL_IDEAL,
                     TBL_TRIMESTERS, WORKED_BRA, WORKED_PERIOD, WORKED_PREGNANCY)

ACTIVITY_OPTIONS = [
    ('sedentary', 'Sedentary &mdash; little or no exercise', False),
    ('light', 'Lightly active &mdash; light exercise 1-3 days/week', False),
    ('moderate', 'Moderately active &mdash; exercise 3-5 days/week', True),
    ('very', 'Very active &mdash; hard exercise 6-7 days/week', False),
    ('extra', 'Extra active &mdash; physical job or 2x daily training', False),
]

CALCULATORS = [
    # ------------------------------------------------------------------ BMI
    {
        'slug': 'bmi',
        'icon': 'scale',
        'nav': 'BMI',
        'h1': 'BMI Calculator',
        'meta_title': 'BMI Calculator &mdash; Metric &amp; Imperial',
        'meta_desc': 'Free BMI calculator. Enter height and weight in metric or imperial units to get your Body Mass Index, weight category and healthy weight range instantly.',
        'blurb': 'Find your Body Mass Index and see which weight category it falls in.',
        'keywords': 'bmi body mass index weight height obesity healthy weight range underweight overweight',
        'tags': ['body-composition'],
        'intro': 'Body Mass Index compares your weight to your height in a single number. It is the quickest screening figure in health care &mdash; not a measure of body fat, but a useful first look at whether your weight sits in a healthy band for your height.',
        'form_title': 'Your measurements',
        'form': (
            units_toggle()
            + height_field()
            + weight_field()
            + number('age', 'Age', unit='years', placeholder='30', minimum=2,
                     maximum=120, step='1', required=False, inputmode='numeric',
                     hint='Only used to warn you if adult BMI categories do not apply.')
            + actions('Calculate BMI')
        ),
        'method_title': 'How BMI is calculated',
        'method': '''
<p>BMI divides your weight in kilograms by the square of your height in metres. Everything else on this page &mdash; the category, the healthy weight range &mdash; follows from that one number.</p>
''' + EQ_BMI + '''
<p>Your healthy weight range is the reverse calculation: the weights that would place you at a BMI of 18.5 and 24.9 at your height.</p>

<h3>The categories we use</h3>
<p>This calculator uses the <strong>World Health Organization adult cut-off points</strong>, which are the international standard for adults aged 20 and over:</p>
<ul>
  <li><strong>Below 18.5</strong> &mdash; underweight (split into mild, moderate and severe thinness)</li>
  <li><strong>18.5 to 24.9</strong> &mdash; healthy weight</li>
  <li><strong>25.0 to 29.9</strong> &mdash; overweight</li>
  <li><strong>30.0 and above</strong> &mdash; obese, in three classes</li>
</ul>
<p>Some health bodies in Asia use lower thresholds &mdash; often 23 for overweight and 27.5 for obesity &mdash; because cardiometabolic risk appears at a lower BMI in many South and East Asian populations. If that applies to you, read your number against those figures rather than the WHO defaults, and discuss it with your doctor.</p>

<h3>What BMI cannot tell you</h3>
<p>BMI knows nothing about what your weight is made of. Muscle is denser than fat, so a lean, heavily trained athlete can land in the &ldquo;overweight&rdquo; band while carrying very little fat. In the other direction, someone with low muscle mass can sit inside the healthy band while carrying more fat than is ideal. It also says nothing about <em>where</em> fat is stored, and abdominal fat carries more metabolic risk than fat elsewhere.</p>
<p>If you want a fuller picture, pair this with the <a href="../body-fat/index.html">body fat calculator</a> and a simple waist measurement.</p>
''',
        'faqs': [
            ('What is a healthy BMI?',
             'For adults aged 20 and over, the World Health Organization treats 18.5 to 24.9 as the healthy range. Below 18.5 is classed as underweight and 25 or above as overweight. These are screening bands for populations, not a personal target &mdash; your own healthiest weight depends on body composition, fat distribution, fitness and medical history.'),
            ('Is BMI accurate for athletes and muscular people?',
             'No. BMI cannot distinguish muscle from fat, so people with a lot of lean mass are routinely misclassified as overweight or obese. A rugby player and a sedentary person of the same height and weight get the same BMI despite completely different body composition. If you train seriously with weights, use a body-fat estimate and waist measurement instead.'),
            ('Does BMI work for children and teenagers?',
             'Not with these categories. For anyone under 20, BMI is plotted on age- and sex-specific growth charts and read as a percentile, because healthy body composition changes throughout growth. A BMI of 19 means something very different at age 8 than at age 28. Ask a paediatrician to interpret a child’s BMI percentile.'),
            ('Should Asian populations use different BMI cut-offs?',
             'Often, yes. The WHO has noted that many Asian populations show elevated risk of type 2 diabetes and cardiovascular disease at a lower BMI than European populations. Several national guidelines, including in India and China, use roughly 23 for overweight and 27.5 for obesity. This calculator shows the standard WHO bands, so compare your figure to your local guidance too.'),
            ('Does BMI change with age?',
             'The formula does not, but its meaning shifts. Older adults tend to lose muscle and gain fat at the same weight, so an unchanged BMI can hide a real change in body composition. Some research also suggests a slightly higher BMI is protective in later life. The number is best read as one signal among several.'),
        ],
    },

    # ------------------------------------------------------------------ BMR
    {
        'slug': 'bmr',
        'icon': 'flame',
        'nav': 'BMR',
        'h1': 'BMR Calculator',
        'meta_title': 'BMR Calculator &mdash; Basal Metabolic Rate',
        'meta_desc': 'Calculate your Basal Metabolic Rate with the Mifflin-St Jeor, Harris-Benedict or Katch-McArdle formula, plus maintenance calories (TDEE) for your activity level.',
        'blurb': 'Calculate the calories your body burns at rest, plus daily maintenance calories.',
        'keywords': 'bmr basal metabolic rate tdee maintenance calories mifflin st jeor harris benedict katch mcardle metabolism',
        'tags': ['energy'],
        'intro': 'Your Basal Metabolic Rate is the energy your body spends doing nothing at all &mdash; breathing, circulating blood, keeping your brain and organs running. It is the floor your daily calorie needs are built on, and typically accounts for 60&ndash;70% of everything you burn in a day.',
        'form_title': 'About you',
        'form': (
            units_toggle()
            + sex_field()
            + number('age', 'Age', unit='years', placeholder='30', minimum=15,
                     maximum=100, step='1', inputmode='numeric')
            + height_field()
            + weight_field()
            + select('formula', 'Formula', [
                ('mifflin', 'Mifflin-St Jeor (recommended)', True),
                ('harris', 'Revised Harris-Benedict', False),
                ('katch', 'Katch-McArdle (needs body fat %)', False),
            ], hint='Mifflin-St Jeor is the most accurate general-purpose equation for adults.')
            + '<div data-show-when="formula:katch" hidden>'
            + number('bodyFat', 'Body fat percentage', unit='%', placeholder='20',
                     minimum=3, maximum=65, step='0.1',
                     hint='Not sure? Estimate it with the body fat calculator first.')
            + '</div>'
            + select('activity', 'Activity level', ACTIVITY_OPTIONS,
                     hint='Used to turn your BMR into daily maintenance calories.')
            + actions('Calculate BMR')
        ),
        'method_title': 'How BMR is calculated',
        'method': '''
<p>This calculator offers three published equations. All three predict resting energy expenditure from body size; they differ in the data they were derived from.</p>

<h3>Mifflin-St Jeor (1990) &mdash; the default</h3>
''' + EQ_BMR_MIFFLIN + '''
<p>Derived from a modern population and recommended by the American Dietetic Association as the most reliable general-purpose prediction for healthy adults.</p>

<h3>Revised Harris-Benedict (1984)</h3>
''' + EQ_BMR_HARRIS + '''
<p>The Roza and Shizgal revision of the original 1919 equation. It tends to run slightly higher than Mifflin-St Jeor.</p>

<h3>Katch-McArdle</h3>
''' + EQ_BMR_KATCH + '''
<p>Works from lean mass rather than total weight, so it needs a body-fat figure. If you have a reliable measurement, it is usually the most accurate of the three for very lean or very muscular people, because it does not need to guess at body composition.</p>

<h3>From BMR to daily calories (TDEE)</h3>
<p>Total Daily Energy Expenditure multiplies BMR by an activity factor:</p>
''' + TBL_ACTIVITY + '''
<p>Weight-change targets assume roughly 7,700 kcal per kilogram of body fat, so a 500 kcal daily deficit works out near half a kilogram per week. Real-world results run slower than the arithmetic because your body adapts &mdash; expect to adjust after a few weeks.</p>
''',
        'faqs': [
            ('What is the difference between BMR and TDEE?',
             'BMR is what you burn at complete rest &mdash; lying still, fasted, in a neutral temperature. TDEE is everything you burn in a real day: BMR plus digestion, walking, fidgeting and exercise. TDEE is the number that matters for eating to maintain, lose or gain weight, and it is always higher than BMR.'),
            ('Which BMR formula should I use?',
             'Mifflin-St Jeor for most people &mdash; it is the current general recommendation and is derived from a more representative modern population than Harris-Benedict. Use Katch-McArdle only if you have a genuinely reliable body-fat measurement, in which case it handles very lean or very muscular bodies better.'),
            ('How accurate is a calculated BMR?',
             'Prediction equations land within about 10% of lab-measured resting metabolic rate for most healthy adults, which means a 1,600 kcal estimate could really be anywhere from about 1,440 to 1,760. Accuracy drops further at the extremes of body size, in older adults, and with thyroid or metabolic conditions. Use it as a starting point, then adjust based on what actually happens to your weight over two to three weeks.'),
            ('Can I eat below my BMR to lose weight faster?',
             'It is generally a poor idea. Very low intakes make it hard to meet protein and micronutrient needs, tend to cost you lean mass along with fat, and are difficult to sustain. A moderate deficit from your TDEE &mdash; not your BMR &mdash; is the usual recommendation. Anyone considering a very low calorie diet should do it under medical supervision.'),
            ('Why did my BMR go down after losing weight?',
             'A smaller body needs less energy, so BMR falls as weight falls. There is also an adaptive component: sustained dieting reduces energy expenditure a little beyond what the size change alone predicts. This is why weight loss slows over time and why recalculating every few kilograms is worthwhile.'),
        ],
    },

    # --------------------------------------------------------- Ideal weight
    {
        'slug': 'ideal-weight',
        'icon': 'target',
        'nav': 'Ideal weight',
        'h1': 'Ideal Weight Calculator',
        'meta_title': 'Ideal Weight Calculator &mdash; 4 Formulas',
        'meta_desc': 'Compare four clinical ideal body weight formulas for your height, alongside the healthy weight range from BMI. Metric and imperial units supported.',
        'blurb': 'Compare four clinical formulas for a reference weight at your height.',
        'keywords': 'ideal weight ideal body weight devine robinson miller hamwi healthy weight for height reference weight',
        'tags': ['body-composition'],
        'intro': 'There is no single ideal weight for a given height &mdash; but there are several published reference formulas, and a healthy BMI range that is usually more useful than any of them. This calculator shows you all of it side by side so you can see how much the answers differ.',
        'form_title': 'Your details',
        'form': (
            units_toggle()
            + sex_field()
            + height_field()
            + select('formula', 'Reference formula', [
                ('devine', 'Devine (1974) &mdash; most widely used', True),
                ('robinson', 'Robinson (1983)', False),
                ('miller', 'Miller (1983)', False),
                ('hamwi', 'Hamwi (1964)', False),
            ], hint='All four are shown in the results regardless of which you pick.')
            + weight_field(required=False, label='Current weight',
                           hint='Optional &mdash; adds a comparison and your current BMI.')
            + actions('Calculate ideal weight')
        ),
        'method_title': 'How ideal weight is calculated',
        'method': '''
<p>All four formulas share the same shape: a base weight at five feet, plus a fixed amount for every inch above that. They differ only in the constants, which is why they disagree by several kilograms at the same height.</p>
''' + TBL_IDEAL + '''

<h3>Where these formulas came from</h3>
<p>The Devine formula was not designed to tell anyone what to weigh. B.J. Devine published it in 1974 as a way to scale <em>medication doses</em> &mdash; particularly gentamicin &mdash; to body size. It was an estimate for clinicians, built on population averages of the era, and it stuck. Robinson, Miller and Hamwi are all modifications of the same idea from the same period.</p>
<p>This history matters because it explains the formulas&rsquo; blind spots: they use only height and sex. Frame size, muscle mass, age and body composition do not appear anywhere in them. A 180 cm powerlifter and a 180 cm sedentary office worker get the same answer.</p>

<h3>The healthy BMI range is usually the better target</h3>
<p>The range shown alongside your result is the span of weights that put you between a BMI of 18.5 and 24.9 at your height. It is wider than a single number for good reason &mdash; there is a genuine range of healthy weights at any height, and a range is far easier to live inside than a single figure. For most people this is the more meaningful reference. You can explore it further with the <a href="../bmi/index.html">BMI calculator</a>.</p>
''',
        'faqs': [
            ('Which ideal weight formula is the most accurate?',
             'None of them is accurate in the way people expect, because none was validated against health outcomes. Devine is the most widely used and remains a clinical standard for drug dosing; Robinson and Miller were attempts to fit observed data better. For judging your own weight, the healthy BMI range is a more defensible reference than any single formula.'),
            ('Why do the four formulas give different answers?',
             'They were derived at different times from different reference populations, using different assumptions about how weight should scale with height. The spread between them &mdash; often 5 to 8 kg at the same height &mdash; is itself the useful information: it shows there is no precise ideal weight to hit.'),
            ('Do these formulas account for body frame size?',
             'No. Only height and sex go in. A large-framed person with broad shoulders and dense bone can be several kilograms above the formula weight and completely healthy. Some older clinical practice adjusted the result by about 10% for small or large frames, measured by wrist circumference or elbow breadth, but that adjustment has no strong evidence behind it.'),
            ('Should I try to reach my ideal body weight?',
             'Not as a goal in itself. Health outcomes track much more closely with body composition, waist measurement, fitness, blood markers and habits than with hitting a specific number on a scale. If you want a weight target, discuss a realistic range with a doctor or dietitian rather than aiming at a 1970s dosing formula.'),
            ('Does ideal weight differ for athletes?',
             'Substantially. Muscle is denser than fat, so trained athletes routinely weigh well above the formula figure while carrying low body fat and excellent health markers. For anyone who trains seriously, body-fat percentage and performance are far more informative than total weight.'),
        ],
    },

    # ------------------------------------------------------------- Body fat
    {
        'slug': 'body-fat',
        'icon': 'body',
        'nav': 'Body fat',
        'h1': 'Body Fat Calculator',
        'meta_title': 'Body Fat Calculator &mdash; US Navy Method',
        'meta_desc': 'Estimate body fat percentage from neck, waist and hip measurements using the US Navy circumference method. Includes fat mass, lean mass and reference ranges.',
        'blurb': 'Estimate body-fat percentage, fat mass and lean mass from tape measurements.',
        'keywords': 'body fat percentage calculator us navy method lean mass fat mass waist neck hip circumference',
        'tags': ['body-composition'],
        'intro': 'Body fat percentage tells you what your weight is actually made of &mdash; which is the thing BMI cannot see. This calculator uses the US Navy circumference method: a few tape measurements, no equipment, and an estimate that is usually within about 3&ndash;4 percentage points of a proper body composition scan.',
        'form_title': 'Your measurements',
        'form': (
            units_toggle()
            + sex_field()
            + number('age', 'Age', unit='years', placeholder='30', minimum=15,
                     maximum=100, step='1', required=False, inputmode='numeric',
                     hint='Optional &mdash; enables a second cross-check estimate.')
            + height_field()
            + length_field('neck', 'Neck circumference',
                           hint='Measure just below the larynx, tape sloping slightly downward at the front.',
                           metric_ph='38', imperial_ph='15',
                           metric_min=20, metric_max=70, imperial_min=8, imperial_max=28)
            + length_field('waist', 'Waist circumference',
                           hint='Men: at the navel. Women: at the narrowest point. Relax, do not suck in.',
                           metric_ph='85', imperial_ph='33',
                           metric_min=40, metric_max=200, imperial_min=16, imperial_max=79)
            + '<div data-show-when="sex:female" hidden>'
            + length_field('hip', 'Hip circumference',
                           hint='At the widest point around the buttocks.',
                           metric_ph='98', imperial_ph='38',
                           metric_min=50, metric_max=220, imperial_min=20, imperial_max=87)
            + '</div>'
            + weight_field(required=False, hint='Optional &mdash; adds fat mass and lean mass to your result.')
            + actions('Calculate body fat')
        ),
        'method_title': 'How body fat is calculated',
        'method': '''
<p>The US Navy method estimates body density from the ratio between fat-storing circumferences (waist, hips) and a largely fat-free one (neck), scaled by height. All logarithms are base 10 and all measurements are in centimetres.</p>
''' + EQ_BODYFAT + '''
<p>If you supply your weight, fat mass is simply your weight multiplied by that percentage, and lean mass is the remainder &mdash; muscle, bone, organs, water and connective tissue together.</p>

<h3>How to measure properly</h3>
<p>The method is only as good as the tape work, and this is where most of the error comes from.</p>
<ul>
  <li><strong>Use a flexible, non-stretch tape.</strong> A cloth sewing tape is ideal; a metal builder&rsquo;s tape is not.</li>
  <li><strong>Keep the tape level</strong> all the way around and snug against skin without compressing it.</li>
  <li><strong>Measure first thing in the morning</strong>, before eating, and stay consistent about timing between measurements.</li>
  <li><strong>Breathe normally and relax your abdomen.</strong> Measure at the end of a normal exhale. Do not pull your stomach in.</li>
  <li><strong>Take each measurement twice</strong> and average them. If two readings differ by more than a centimetre, take a third.</li>
</ul>

<h3>How accurate is it?</h3>
<p>Validation studies typically find a standard error around 3&ndash;4 percentage points against hydrostatic weighing or DEXA. That is respectable for a tape measure and useful for tracking change over time, but it is not a precise figure. The method also assumes a typical fat distribution, so it performs less well at the extremes &mdash; very lean athletes and people with obesity &mdash; and for anyone who carries fat unusually.</p>
<p>What it does well is trend. Measured the same way each month, the direction of change is far more reliable than any single reading. For a precise number, DEXA is the practical reference standard.</p>
''',
        'faqs': [
            ('How accurate is the US Navy body fat method?',
             'Roughly within 3 to 4 percentage points of a DEXA scan for most adults, provided the measurements are taken carefully. It is more accurate than bioelectrical impedance scales for many people and far more accurate than estimating from BMI alone, but it is still an estimate derived from a population equation, not a measurement of your actual tissue.'),
            ('What is a healthy body fat percentage?',
             'For men, roughly 14 to 24% is typically considered healthy, with athletes often between 6 and 14%. For women, roughly 21 to 31% is typical, with athletes between 14 and 21%. Women carry more essential fat than men for hormonal and reproductive function &mdash; around 10 to 13% versus 2 to 5% &mdash; so the ranges are not interchangeable.'),
            ('Why does the female formula need a hip measurement?',
             'Women store proportionally more fat around the hips and thighs, so waist circumference alone does not capture body composition well. Including the hip measurement lets the equation account for that distribution. The male equation was validated without it.'),
            ('Can body fat percentage be too low?',
             'Yes, and it is dangerous. Below roughly 5% for men and 12% for women, you are cutting into essential fat needed for organ protection, hormone production and temperature regulation. Very low body fat is associated with hormonal disruption, loss of menstruation, bone density loss, weakened immunity and mood disturbance.'),
            ('How often should I re-measure?',
             'Every two to four weeks is plenty. Body composition changes slowly, and week-to-week differences in a tape measurement are usually noise from hydration, food intake, bloating or tape placement rather than real change. Measure under the same conditions each time and watch the trend across several months.'),
        ],
    },

    # ------------------------------------------------------- Calories burned
    {
        'slug': 'calories-burned',
        'icon': 'bolt',
        'nav': 'Calories burned',
        'h1': 'Calories Burned Calculator',
        'meta_title': 'Calories Burned Calculator &mdash; MET Based',
        'meta_desc': 'Estimate calories burned during exercise and daily activities using MET values from the Compendium of Physical Activities. Covers 80+ activities in metric and imperial.',
        'blurb': 'Estimate the energy you burned across 80+ activities using MET values.',
        'keywords': 'calories burned calculator met values exercise workout activity energy expenditure walking running cycling gym',
        'tags': ['energy'],
        'intro': 'Every activity has a MET value &mdash; a multiple of the energy you spend sitting still. Pick what you did, how long you did it and what you weigh, and this calculator turns those MET values into an estimated calorie burn.',
        'form_title': 'Your activity',
        'form': (
            units_toggle()
            + weight_field(hint='Energy cost scales directly with body weight.')
            + select('activity', 'Activity', [], extra_attr='data-met-source',
                     hint='80+ activities, grouped by type. MET value is shown beside each.')
            + '<fieldset class="field">'
            + '<legend class="field__legend">Duration <span class="req" aria-hidden="true">*</span></legend>'
            + '<div class="input-row">'
            + '<div><div class="input-group"><input class="input" id="durationHours" name="durationHours" '
              'type="number" inputmode="numeric" step="1" data-min="0" data-max="24" placeholder="0" '
              'aria-label="Duration, hours" aria-describedby="durationHours-error"><span class="unit">h</span></div></div>'
            + '<div><div class="input-group"><input class="input" id="durationMinutes" name="durationMinutes" '
              'type="number" inputmode="numeric" step="1" data-min="0" data-max="59" placeholder="45" '
              'aria-label="Duration, minutes" aria-describedby="durationMinutes-error"><span class="unit">min</span></div></div>'
            + '</div>'
            + '<p class="error-msg" id="durationHours-error" role="alert"></p>'
            + '<p class="error-msg" id="durationMinutes-error" role="alert"></p>'
            + '</fieldset>'
            + actions('Calculate calories burned')
        ),
        'method_title': 'How calories burned is calculated',
        'method': '''
<p>MET stands for Metabolic Equivalent of Task. One MET is the energy cost of sitting quietly &mdash; about 3.5 millilitres of oxygen per kilogram of body weight per minute. An activity rated at 8 METs costs eight times that.</p>
''' + EQ_CALORIES + '''
<p>Two things follow from the formula. First, calorie burn scales directly with body weight &mdash; a 90 kg person burns roughly 50% more than a 60 kg person doing exactly the same thing. Second, duration and intensity matter equally in the arithmetic: 60 minutes at 4 METs and 30 minutes at 8 METs give the same total.</p>

<h3>MET-minutes and activity guidelines</h3>
<p>Multiplying METs by minutes gives MET-minutes, the unit public health guidance is written in. The World Health Organization recommends adults accumulate <strong>500 to 1,000 MET-minutes per week</strong>, which corresponds to 150&ndash;300 minutes of moderate activity or 75&ndash;150 minutes of vigorous activity. The results panel shows how your session contributes.</p>

<h3>Where the numbers come from</h3>
<p>MET values in this calculator are drawn from the <strong>2011 Compendium of Physical Activities</strong> (Ainsworth et al.), the reference dataset used across exercise science. The dataset version is stamped in the results so you can tell when values change.</p>

<h3>Why your smartwatch disagrees</h3>
<p>MET values are population averages measured in laboratories on groups of adults. They do not know your fitness level, technique, terrain, altitude, temperature or body composition &mdash; all of which move the real number. A trained cyclist is more efficient than a beginner and burns <em>less</em> at the same speed. Heart-rate-based devices capture some of this, but they have their own error, often 10&ndash;20% or worse for non-steady-state activity.</p>
<p>Also worth knowing: this is <em>gross</em> energy expenditure, which includes the calories you would have burned anyway just existing during that time. For a one-hour session that baseline is roughly 60&ndash;90 kcal of the total.</p>
''',
        'faqs': [
            ('How accurate are MET-based calorie estimates?',
             'Expect roughly 15 to 25% error for an individual. MET values are group averages from laboratory measurements, so they cannot account for your fitness, efficiency, technique or the specific conditions of your session. They are most useful for comparing activities against each other and for tracking your own trend, rather than as an exact count.'),
            ('Does body weight change how many calories I burn?',
             'Yes, directly and proportionally. The MET formula multiplies by body weight in kilograms, so moving a heavier body costs more energy for the same activity. This is why calorie burn falls as you lose weight while doing the same workout &mdash; and why re-entering your weight periodically matters.'),
            ('Should I eat back the calories I burned exercising?',
             'Partly, if at all. Because these estimates run optimistic and appetite tends to rise after exercise, eating back the full figure is a common reason weight loss stalls. A frequent recommendation is to eat back around half, and to judge by how your weight actually moves over two to three weeks.'),
            ('What is the difference between gross and net calories burned?',
             'Gross is everything you burned during the activity. Net subtracts what you would have burned resting for that same period &mdash; roughly one MET-hour, about 60 to 90 kcal per hour for most adults. This calculator reports gross, which is the standard for MET calculations and what most fitness apps display.'),
            ('Which activities burn the most calories per hour?',
             'At the top of the compendium sit running at pace, squash, competitive football, skipping rope and martial arts, all around 10 to 14 METs. But the activity you will actually do three times a week beats a higher-MET one you will abandon. Consistency outperforms intensity over any horizon longer than a month.'),
        ],
    },

    # ----------------------------------------------------------------- Pace
    {
        'slug': 'pace',
        'icon': 'run',
        'nav': 'Pace',
        'h1': 'Pace Calculator',
        'meta_title': 'Pace Calculator &mdash; Pace, Time &amp; Splits',
        'meta_desc': 'Calculate running or walking pace, finish time or distance. Enter any two values and get the third, plus split times for 5K, 10K, half marathon and marathon.',
        'blurb': 'Solve for pace, finish time or distance, with a full split table.',
        'keywords': 'pace calculator running walking split times finish time speed marathon half marathon 5k 10k min per km',
        'tags': ['training'],
        'intro': 'Pace, time and distance are three sides of the same equation &mdash; give this calculator any two and it solves for the third, then shows your split times for every common race distance.',
        'form_title': 'What are you solving for?',
        'form': (
            segmented('solveFor', 'Calculate', [
                ('pace', 'Pace', True),
                ('time', 'Finish time', False),
                ('distance', 'Distance', False),
            ], hint='Fill in the other two values and we work out the one you picked.')
            + '<div data-show-when="solveFor:pace,time">'
            + '<div class="field">'
            + '<label for="distance">Distance <span class="req" aria-hidden="true">*</span></label>'
            + '<div class="input-row input-row--dist">'
            + '<div><input class="input" id="distance" name="distance" type="number" inputmode="decimal" '
              'step="0.01" data-min="0.01" data-max="2000" placeholder="10" aria-required="true" '
              'aria-describedby="distance-error"></div>'
            + '<fieldset class="segmented"><legend class="visually-hidden">Distance unit</legend>'
              '<input type="radio" name="distUnit" id="distUnit-km" value="km" checked>'
              '<label for="distUnit-km">km</label>'
              '<input type="radio" name="distUnit" id="distUnit-mi" value="mi">'
              '<label for="distUnit-mi">mi</label></fieldset>'
            + '</div>'
            + '<p class="error-msg" id="distance-error" role="alert"></p>'
            + '</div></div>'
            + '<div data-show-when="solveFor:pace,distance">'
            + '<fieldset class="field">'
            + '<legend class="field__legend">Time <span class="req" aria-hidden="true">*</span></legend>'
            + '<div class="input-row input-row--3">'
            + '<div><div class="input-group"><input class="input" id="timeH" name="timeH" type="number" '
              'inputmode="numeric" step="1" data-min="0" data-max="99" placeholder="0" aria-label="Hours" '
              'aria-describedby="timeH-error"><span class="unit">h</span></div></div>'
            + '<div><div class="input-group"><input class="input" id="timeM" name="timeM" type="number" '
              'inputmode="numeric" step="1" data-min="0" data-max="59" placeholder="52" aria-label="Minutes" '
              'aria-describedby="timeM-error"><span class="unit">m</span></div></div>'
            + '<div><div class="input-group"><input class="input" id="timeS" name="timeS" type="number" '
              'inputmode="numeric" step="1" data-min="0" data-max="59" placeholder="30" aria-label="Seconds" '
              'aria-describedby="timeS-error"><span class="unit">s</span></div></div>'
            + '</div>'
            + '<p class="error-msg" id="timeH-error" role="alert"></p>'
            + '<p class="error-msg" id="timeM-error" role="alert"></p>'
            + '<p class="error-msg" id="timeS-error" role="alert"></p>'
            + '</fieldset></div>'
            + '<div data-show-when="solveFor:time,distance" hidden>'
            + '<fieldset class="field">'
            + '<legend class="field__legend">Pace <span class="req" aria-hidden="true">*</span></legend>'
            + '<div class="input-row input-row--pace">'
            + '<div><div class="input-group"><input class="input" id="paceM" name="paceM" type="number" '
              'inputmode="numeric" step="1" data-min="0" data-max="99" placeholder="5" aria-label="Pace minutes" '
              'aria-describedby="paceM-error"><span class="unit">m</span></div></div>'
            + '<div><div class="input-group"><input class="input" id="paceS" name="paceS" type="number" '
              'inputmode="numeric" step="1" data-min="0" data-max="59" placeholder="15" aria-label="Pace seconds" '
              'aria-describedby="paceS-error"><span class="unit">s</span></div></div>'
            + '<fieldset class="segmented"><legend class="visually-hidden">Pace unit</legend>'
              '<input type="radio" name="paceUnit" id="paceUnit-km" value="km" checked>'
              '<label for="paceUnit-km">/km</label>'
              '<input type="radio" name="paceUnit" id="paceUnit-mi" value="mi">'
              '<label for="paceUnit-mi">/mi</label></fieldset>'
            + '</div>'
            + '<p class="error-msg" id="paceM-error" role="alert"></p>'
            + '<p class="error-msg" id="paceS-error" role="alert"></p>'
            + '</fieldset></div>'
            + actions('Calculate')
        ),
        'method_title': 'How pace is calculated',
        'method': '''
<p>The whole page rests on one relationship, rearranged three ways:</p>
''' + EQ_PACE + '''
<p>Distances convert through 1 mile = 1.609344 km exactly, and pace per mile is pace per kilometre multiplied by that same factor.</p>

<h3>Standard race distances</h3>
''' + TBL_DISTANCES + '''

<h3>Reading the split table</h3>
<p>The splits assume an even pace throughout &mdash; every kilometre at exactly the same speed. Real races rarely work that way. Most runners are slightly faster in the first half and slow in the second, and the gap widens with distance and heat.</p>
<p>A rough rule from race data: expect to slow by about <strong>4 to 6% each time the distance doubles</strong>. If you can run 10K at 5:00/km, a half marathon closer to 5:15&ndash;5:20/km is a more realistic target than 5:00. Use the split table as a pacing plan for a distance you have actually trained for, not as a prediction for one you have not.</p>

<h3>Negative splits</h3>
<p>Running the second half slightly faster than the first &mdash; a negative split &mdash; is how most distance records are set. Starting 5 to 10 seconds per kilometre slower than target pace for the first few kilometres usually costs less overall time than going out too hard and fading.</p>
''',
        'faqs': [
            ('What is a good running pace for a beginner?',
             'Most new runners settle somewhere between 7:00 and 9:00 per kilometre (roughly 11:15 to 14:30 per mile), and plenty start slower. The more useful test is conversational pace: if you can speak in full sentences while running, you are in the right zone for building an aerobic base. Speed comes from consistent easy mileage long before it comes from running hard.'),
            ('How do I convert pace per kilometre to pace per mile?',
             'Multiply your per-kilometre pace by 1.609344. A 5:00/km pace is 8:02/mile; 6:00/km is 9:39/mile. The calculator shows both automatically, whichever unit you enter.'),
            ('Can I predict my marathon time from a 10K?',
             'Approximately, with caution. Common predictors multiply 10K time by about 4.6 to 4.7 for a marathon, but they assume you have done marathon-specific training and adequate long runs. Without that endurance base, the real result is usually considerably slower. The prediction is a ceiling, not a promise.'),
            ('What are negative splits and are they worth aiming for?',
             'A negative split means running the second half of a race faster than the first. It is how most world records and personal bests are run, because starting conservatively preserves glycogen and delays fatigue. For most runners, going out 5 to 10 seconds per kilometre slower than goal pace for the opening kilometres pays for itself several times over in the closing ones.'),
            ('Does this calculator work for walking and cycling?',
             'Yes. The mathematics is identical for any steady-speed activity &mdash; only the typical numbers change. Brisk walking generally falls between 9:00 and 12:00 per kilometre, and cycling paces are usually discussed in km/h, which the results panel also shows.'),
        ],
    },

    # --------------------------------------------------------------- Period
    {
        'slug': 'period',
        'icon': 'calendar',
        'nav': 'Period',
        'h1': 'Period Calculator',
        'meta_title': 'Period &amp; Ovulation Calculator',
        'meta_desc': 'Estimate your next six periods, ovulation dates and fertile windows from your last period date and average cycle length. Private, calculated entirely in your browser.',
        'blurb': 'Project your next six cycles, ovulation days and fertile windows.',
        'keywords': 'period calculator menstrual cycle ovulation calculator fertile window next period date tracker',
        'tags': ['womens-health'],
        'intro': 'Enter the first day of your last period and your usual cycle length, and this calculator projects your next six cycles &mdash; period dates, estimated ovulation and the fertile window around it.',
        'form_title': 'Your cycle',
        'form': (
            date_field('lmp', 'First day of your last period',
                       hint='The day bleeding started, not the day it ended.')
            + number('cycleLength', 'Average cycle length', unit='days', placeholder='28',
                     minimum=20, maximum=45, step='1', inputmode='numeric',
                     hint='Count from the first day of one period to the day before the next. Typically 21&ndash;35 days.')
            + number('periodLength', 'How long your period lasts', unit='days', placeholder='5',
                     minimum=1, maximum=14, step='1', required=False, inputmode='numeric',
                     hint='Optional &mdash; used to show the full period window. Defaults to 5 days.')
            + actions('Calculate my cycle')
        ),
        'method_title': 'How these dates are calculated',
        'method': '''
<p>The projection works forward from the first day of your last period, called the LMP.</p>
''' + STEPS_PERIOD + WORKED_PERIOD + '''
<p>Each subsequent cycle adds another full cycle length, which is how the six-cycle table is built.</p>

<h3>Why ovulation is counted backwards</h3>
<p>The luteal phase &mdash; from ovulation to the next period &mdash; is the more consistent half of the cycle, usually 12 to 16 days and averaging 14. The follicular phase before ovulation is the part that stretches and shrinks, and it is what makes one person&rsquo;s cycle 26 days and another&rsquo;s 34.</p>
<p>So counting back 14 days from the <em>next</em> expected period gives a better estimate than counting forward 14 days from the last one. On a 32-day cycle, ovulation is estimated around day 18, not day 14 &mdash; a difference that matters if you are using these dates for anything.</p>

<h3>Why the fertile window is six days</h3>
<p>Sperm can survive in the reproductive tract for up to five days in fertile cervical mucus, while an egg is viable for roughly 12 to 24 hours after release. The window therefore opens about five days <em>before</em> ovulation and closes about a day after it, with the highest probability of conception in the two days immediately before ovulation.</p>

<h3>The limits of calendar prediction</h3>
<p>Calendar methods assume the next cycle will behave like the average of the last ones. Cycles vary &mdash; even regular ones. Illness, travel, stress, poor sleep, hard training, weight change, breastfeeding, perimenopause, thyroid conditions and PCOS all shift ovulation timing. One large study of app users found that even people who described their cycles as regular ovulated across a spread of several days from month to month.</p>
<p>If you need to know when you ovulated rather than when you probably will, ovulation predictor kits, basal body temperature charting and cervical mucus observation track your actual cycle instead of a projected one.</p>
''',
        'faqs': [
            ('How accurate is a period calculator?',
             'It is as accurate as your cycle is regular. If your cycles vary by only a day or two, the next period estimate is usually close. If they swing by a week or more, treat the dates as a rough guide. Ovulation estimates are inherently less certain than period dates, because ovulation timing shifts between cycles even in regular ones.'),
            ('Can I use this as contraception?',
             'No. Calendar-based prediction is not a reliable contraceptive method &mdash; typical-use failure rates for calendar methods are high because ovulation moves and sperm survive for days. If you are preventing pregnancy, use a method designed for it, and talk to a healthcare provider about the options. Even formal fertility awareness methods require training plus daily temperature and mucus tracking, not a calendar alone.'),
            ('What is a normal cycle length?',
             'Anywhere from 21 to 35 days is considered within the normal range for adults, and around 21 to 45 days for teenagers in the first few years after menarche. The variation between your own cycles matters more than the absolute number &mdash; consistently varying by more than seven to nine days is worth raising with a doctor.'),
            ('Why is my period late when the calculator said otherwise?',
             'Late periods are common and usually not a sign of anything wrong. Stress, illness, travel across time zones, disrupted sleep, intense training, significant weight change and starting or stopping hormonal contraception can all delay ovulation, which pushes the period back. If a period is more than a week late and pregnancy is possible, take a test. Repeated missed periods without pregnancy are worth investigating.'),
            ('Is my data sent anywhere?',
             'No. Every calculation on this site runs in your browser using JavaScript. Your dates are never transmitted to a server, never stored in an account and never logged. Close the tab and nothing remains except an optional unit preference. See the privacy policy for the full detail.'),
        ],
    },

    # ------------------------------------------------------------ Pregnancy
    {
        'slug': 'pregnancy',
        'icon': 'heart',
        'nav': 'Pregnancy',
        'h1': 'Pregnancy Due Date Calculator',
        'meta_title': 'Pregnancy Due Date Calculator',
        'meta_desc': 'Estimate your due date from your last menstrual period, conception date or a known due date. Shows gestational age, trimester and key pregnancy milestone dates.',
        'blurb': 'Estimate your due date, current gestational age and milestone dates.',
        'keywords': 'pregnancy calculator due date calculator edd gestational age trimester naegele rule conception date weeks pregnant',
        'tags': ['womens-health'],
        'intro': 'Work out your estimated due date and exactly how far along you are today &mdash; from your last period, a known conception date, or a due date you have already been given.',
        'form_title': 'Dating your pregnancy',
        'form': (
            segmented('method', 'Calculate from', [
                ('lmp', 'Last period', True),
                ('conception', 'Conception date', False),
                ('dueDate', 'Known due date', False),
            ], hint='Last menstrual period is the standard clinical starting point.')
            + date_field('refDate', 'Date', hint='The first day of your last period, unless you switched the option above.')
            + '<div data-show-when="method:lmp">'
            + number('cycleLength', 'Average cycle length', unit='days', placeholder='28',
                     minimum=20, maximum=45, step='1', required=False, inputmode='numeric',
                     hint='Optional &mdash; adjusts the due date if your cycle is not 28 days. Defaults to 28.')
            + '</div>'
            + actions('Calculate due date')
        ),
        'method_title': 'How the due date is calculated',
        'method': '''
<p>The standard method is Naegele&rsquo;s rule, which dates pregnancy from the first day of the last menstrual period &mdash; roughly two weeks before conception actually occurs.</p>
''' + STEPS_PREGNANCY + WORKED_PREGNANCY + '''
<p>Gestational age is then simply the number of days elapsed since that adjusted starting point, expressed as weeks and days &mdash; which is why you are already counted as &ldquo;4 weeks pregnant&rdquo; around the time of a first positive test.</p>

<h3>Why 40 weeks from a date before conception?</h3>
<p>It is a historical convention that turned out to be practical. The last period is a date most people can actually remember, while the moment of conception usually is not. Since ovulation typically follows about 14 days later, the 280-day count includes roughly two weeks when you were not yet pregnant. Actual gestation from conception averages about 38 weeks.</p>

<h3>The cycle-length adjustment</h3>
<p>Naegele&rsquo;s rule assumes a 28-day cycle with ovulation on day 14. On a 35-day cycle, ovulation happens closer to day 21, so the pregnancy is effectively a week younger than the LMP suggests and the due date moves a week later. That is what the adjustment corrects for.</p>

<h3>Trimesters and milestones</h3>
''' + TBL_TRIMESTERS + '''

<h3>Ultrasound dating takes precedence</h3>
<p>A first-trimester ultrasound measuring crown-rump length dates a pregnancy to within about five days, and is more accurate than LMP dating &mdash; which depends on remembering a date correctly and on ovulating when the formula assumes. Standard obstetric practice is to redate the pregnancy if the ultrasound differs from the LMP estimate by more than about five to seven days in the first trimester. <strong>Your clinician&rsquo;s date always takes precedence over this calculator.</strong></p>
''',
        'faqs': [
            ('How accurate is a due date calculator?',
             'Only about 4% of babies are born on their estimated due date, and roughly 80% arrive within two weeks either side of it. The due date is best understood as the centre of a likely range rather than an appointment. An early ultrasound narrows that range considerably; LMP dating alone is the least precise method.'),
            ('Can I calculate my due date if I do not know my last period date?',
             'Yes, if you know roughly when conception happened &mdash; switch the method above to conception date. Failing that, an ultrasound is the reliable route: a first-trimester scan can date a pregnancy to within about five days from measurements alone, without needing any remembered dates.'),
            ('Why does the calculator say I am pregnant before I conceived?',
             'Because gestational age is counted from the first day of your last period, not from conception. Around two of those first weeks happen before conception occurs. It is a convention, not an error &mdash; and it is the same convention your clinician and every scan report uses, which is why keeping to it avoids confusion.'),
            ('Does cycle length really change the due date?',
             'It can shift it by up to a week. The 280-day rule assumes ovulation on day 14 of a 28-day cycle. If your cycles run 35 days, you likely ovulate around day 21, so the pregnancy is about a week younger than the LMP implies and the due date moves later. If your cycles are short, it moves earlier.'),
            ('What does full term mean?',
             'Modern obstetric definitions divide the end of pregnancy into bands: early term is 37 weeks 0 days to 38 weeks 6 days, full term is 39 weeks 0 days to 40 weeks 6 days, late term is 41 weeks, and post-term is 42 weeks and beyond. This distinction was introduced because outcomes at 37 weeks are measurably different from those at 39 weeks.'),
        ],
    },

    # -------------------------------------------------------------- Bra size
    {
        'slug': 'bra-size',
        'icon': 'ruler',
        'nav': 'Bra size',
        'h1': 'Bra Size Calculator',
        'meta_title': 'Bra Size Calculator &mdash; India, UK, US, EU',
        'meta_desc': 'Calculate your bra band and cup size from underbust and bust measurements. Converts between India, UK, US and EU sizing systems and shows sister sizes.',
        'blurb': 'Convert bust and underbust measurements into band and cup sizes.',
        'keywords': 'bra size calculator band size cup size underbust bust measurement india uk us eu sister size conversion',
        'tags': ['womens-health'],
        'intro': 'Two tape measurements are all it takes to get a starting size. This calculator shows your band and cup in Indian, UK, US and EU conventions at once, along with the sister sizes worth trying when the first one is not quite right.',
        'form_title': 'Your measurements',
        'form': (
            segmented('measureUnit', 'Measure in', [
                ('cm', 'Centimetres', True),
                ('in', 'Inches', False),
            ])
            + number('underbust', 'Underbust (band) measurement', unit='cm / in', placeholder='78',
                     minimum=22, maximum=190, step='0.1',
                     hint='Snug around the ribcage directly under the bust, tape level all the way round.')
            + number('bust', 'Bust measurement', unit='cm / in', placeholder='92',
                     minimum=24, maximum=200, step='0.1',
                     hint='Around the fullest part of the bust, tape loose enough not to compress.')
            + select('region', 'Sizing system', [
                ('india', 'India (follows UK conventions)', True),
                ('uk', 'United Kingdom', False),
                ('us', 'United States', False),
                ('eu', 'Europe (cm bands)', False),
            ], hint='Cup letters diverge between systems above a D cup.')
            + actions('Calculate bra size')
        ),
        'method_title': 'How bra size is calculated',
        'method': '''
<p>A bra size has two independent parts. The <strong>band</strong> comes from your underbust measurement and carries most of the support. The <strong>cup</strong> comes from the difference between your bust and your band &mdash; it is not an absolute volume.</p>
''' + STEPS_BRA + WORKED_BRA + '''

<h3>Cup letters are not universal</h3>
<p>Below a D cup the systems agree. Above it they part company, which is the single biggest source of sizing confusion:</p>
<ul>
  <li><strong>UK and India:</strong> D, DD, E, F, FF, G, GG, H, HH, J&hellip;</li>
  <li><strong>US:</strong> D, DD, DDD, then G, H, I, J&hellip; (many US brands skip F)</li>
  <li><strong>EU:</strong> D, E, F, G, H&hellip; with no doubled letters</li>
</ul>
<p>So a UK 34F is close to a US 34DDD and an EU 75F. This is why a size that fits one brand can be two letters off in another, and why the results panel shows all four systems side by side.</p>

<h3>Sister sizes</h3>
<p>Cup volume depends on the band it sits on. Going down a band size while going up a cup letter keeps roughly the same cup volume with a tighter band &mdash; a 36C and a 34D hold a similar volume. These are sister sizes, and they are the first thing to try when a bra is close but not right: right cup, loose band? Try one band smaller and one cup bigger.</p>

<h3>Signs of a poor fit</h3>
<ul>
  <li><strong>Band riding up at the back</strong> &mdash; band is too loose. Go down a band, up a cup.</li>
  <li><strong>Straps digging in</strong> &mdash; usually the band is not doing its job; it should carry about 80% of the support.</li>
  <li><strong>Tissue spilling over the top or sides</strong> &mdash; cup is too small.</li>
  <li><strong>Gaping or wrinkling at the top of the cup</strong> &mdash; cup is too large, or the style does not suit your shape.</li>
  <li><strong>Underwire sitting on breast tissue</strong> rather than on the ribcage &mdash; cup is too small or the wire is the wrong width.</li>
</ul>
<p>Measurements give you a starting point. Fit is decided in front of a mirror.</p>
''',
        'faqs': [
            ('How do I measure myself for a bra correctly?',
             'Take both measurements without a padded bra on &mdash; a thin unlined bra or nothing at all. For the band, wrap the tape snugly around your ribcage directly beneath the bust, level all the way around and parallel to the floor. For the bust, measure around the fullest point without compressing the tissue. Stand upright, breathe normally and measure at the end of a normal exhale.'),
            ('Why is my calculated size different from what I usually wear?',
             'Very commonly because the old rule of adding four or five inches to the underbust measurement is still widely used and produces bands that are far too loose. A loose band shifts support onto the straps, which is why so many people end up in a band two sizes too big and a cup two sizes too small. Brand variation accounts for much of the rest.'),
            ('What are sister sizes?',
             'Sizes that hold approximately the same cup volume on a different band &mdash; for example 34D, 36C and 32DD. If a bra fits in the cup but the band is loose, go down one band size and up one cup letter. If the band fits but the cup is tight, stay on the band and go up a cup.'),
            ('Does bra size change over time?',
             'Frequently. Weight change, pregnancy, breastfeeding, hormonal cycles, ageing and contraception can all alter both band and cup. Re-measuring every six to twelve months, and after any significant weight change or pregnancy, is sensible.'),
            ('Are bra sizes standardised between brands?',
             'No, and that is the honest answer to most fitting frustration. There is no enforced standard for cup volume or band tension, so the same labelled size varies between brands, between styles within one brand, and over time as a brand changes its patterns. Use the calculated size to decide which two or three sizes to try on, not as a final answer.'),
        ],
    },
]

CALC_BY_SLUG = {c['slug']: c for c in CALCULATORS}

# Order shown in the directory and in "related calculators" lists
DIRECTORY_ORDER = ['bmi', 'bmr', 'ideal-weight', 'body-fat', 'calories-burned',
                   'pace', 'period', 'pregnancy', 'bra-size']

TAG_LABELS = [
    ('all', 'All calculators'),
    ('body-composition', 'Body composition'),
    ('energy', 'Energy &amp; calories'),
    ('training', 'Training'),
    ('womens-health', "Women's health"),
]
