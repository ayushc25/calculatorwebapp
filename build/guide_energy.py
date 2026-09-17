# -*- coding: utf-8 -*-
"""Educational articles for the energy and training calculators.

bmr, calories-burned, pace. Rendered below the calculator by build.py.
"""

from guide import callout, guide
from parts import ref_table, worked

GUIDES_ENERGY = {}

# ==========================================================================
# BMR
# ==========================================================================
GUIDES_ENERGY['bmr'] = guide(
    intro='''
<p>Almost everything your body spends energy on happens without you deciding to do it. Your heart beats, your kidneys filter, your brain consumes glucose at a steady clip, your cells rebuild themselves. Basal Metabolic Rate is the price of all of that &mdash; the energy required simply to stay alive and at rest.</p>
<p>It is also the largest single component of what you burn in a day, which makes it the natural starting point for any calculation about eating to maintain, lose or gain weight. This article covers what BMR includes, how it relates to the total you actually burn, what genuinely changes it, and which widely repeated claims about metabolism do not survive contact with the evidence.</p>
''',
    sections=[
        ('what-is-bmr', 'What BMR measures', '''
<p>Basal Metabolic Rate is the energy your body uses at complete rest: lying still, awake, in a thermally neutral room, at least twelve hours after your last meal and without recent exercise. Those conditions are strict because they strip out everything except the baseline cost of being alive.</p>
<p>That baseline is not evenly distributed. The liver, brain, heart and kidneys are small in mass but metabolically expensive, and together account for a large share of resting energy use. Skeletal muscle is much heavier but cheaper per kilogram at rest &mdash; which is why adding muscle raises BMR less dramatically than fitness marketing tends to suggest.</p>
<h3>BMR and RMR are not quite the same</h3>
<p>You will see both terms used interchangeably. Strictly, <strong>Resting Metabolic Rate</strong> is measured under less rigid conditions &mdash; rested rather than fully fasted and undisturbed &mdash; and typically comes out a few per cent higher than true BMR. Prediction equations, including the three this calculator offers, sit somewhere between the two. The distinction rarely matters in practice, but it is one reason two sources can quote different numbers for the same person.</p>
'''),
        ('daily-energy-components', 'Where your daily energy actually goes', '''
<p>BMR is the biggest piece of daily energy expenditure, but it is not the only one. Total Daily Energy Expenditure &mdash; TDEE &mdash; is the sum of four components.</p>
''' + ref_table(
    'The four components of daily energy expenditure',
    [('Component', False), ('What it covers', False), ('Typical share', True)],
    [
        ('Basal metabolic rate', 'Organ function, cell maintenance, breathing, circulation', '60&ndash;70%'),
        ('Thermic effect of food', 'Digesting, absorbing and storing what you eat', 'About 10%'),
        ('Non-exercise activity (NEAT)', 'Walking, standing, fidgeting, housework, posture', '15&ndash;30%'),
        ('Exercise activity', 'Deliberate training sessions', '0&ndash;20%'),
    ]) + '''
<p>The shares in that last column vary widely between people, and NEAT is where most of that variation lives. Two people with similar bodies and similar gym habits can differ by several hundred calories a day purely in how much they move outside training &mdash; a difference that accumulates far faster than most single workouts.</p>
<p>The thermic effect of food also varies by what you eat. Protein costs proportionally more to process than carbohydrate or fat, which is part of why higher-protein diets tend to perform slightly better in weight-loss studies than the calorie arithmetic alone predicts.</p>
'''),
        ('what-affects-bmr', 'What genuinely changes your BMR', '''
<p>In rough order of how much they matter:</p>
<ul>
  <li><strong>Body size.</strong> More tissue costs more energy to maintain. This is the dominant factor and the reason every prediction equation is built around weight and height.</li>
  <li><strong>Lean body mass.</strong> Muscle, organs and bone are metabolically active in a way that stored fat is not. Two people of the same weight with different body composition will have different BMRs &mdash; which is why the Katch-McArdle equation asks for body fat. If you do not have a figure, the <a href="../body-fat/index.html">body fat calculator</a> estimates one.</li>
  <li><strong>Sex.</strong> On average, men carry proportionally more lean mass, which accounts for most of the BMR difference between the sexes at the same weight.</li>
  <li><strong>Age.</strong> BMR falls across a lifetime, though not as steadily as commonly believed &mdash; see the myths section below.</li>
  <li><strong>Genetics.</strong> People of the same size, sex and age can differ by roughly 10% in measured resting metabolic rate for no identifiable reason.</li>
  <li><strong>Thyroid function.</strong> Thyroid hormones set the pace of cellular metabolism directly. Both under- and overactive thyroid conditions shift BMR measurably, which is one reason estimates go astray for people with untreated thyroid disease.</li>
  <li><strong>Illness, injury and fever.</strong> Infection, burns and recovery from major surgery all raise energy requirements, sometimes substantially.</li>
  <li><strong>Sustained energy restriction.</strong> Prolonged dieting reduces energy expenditure somewhat more than the loss of body mass alone would predict.</li>
  <li><strong>Environment.</strong> Sustained cold exposure raises energy use modestly. Ordinary indoor temperature variation does not do much.</li>
</ul>
'''),
        ('using-bmr-for-goals', 'Turning BMR into a daily calorie target', '''
<p>BMR on its own is not a target for anything. It becomes useful once it has been multiplied by an activity factor to give TDEE, and TDEE is what you adjust.</p>
<h3>Maintenance</h3>
<p>Eating at TDEE should hold your weight roughly steady. In practice both the estimate and your real intake carry error, so treat it as a starting hypothesis and check it against two to three weeks of actual weight data before adjusting.</p>
<h3>Losing weight</h3>
<p>A deficit below TDEE is what drives fat loss. A commonly used reference point is that roughly 7,700 kcal corresponds to a kilogram of body fat, which makes a 500 kcal daily deficit look like half a kilogram a week on paper. Real results run slower than the arithmetic, because the body adapts, because activity tends to fall as intake does, and because self-reported intake is systematically underestimated in almost every study that has checked it.</p>
<p>The activity side of the equation has its own page: the <a href="../calories-burned/index.html">calories burned calculator</a> estimates what individual sessions add on top of your resting rate.</p>
<h3>Gaining weight</h3>
<p>A modest surplus alongside resistance training is the usual approach. Large surpluses add fat faster than muscle, because the rate at which muscle can be built has a ceiling that eating more does not lift.</p>
''' + callout('<p><strong>Do not use BMR as a calorie floor.</strong> Eating at or below your BMR is sometimes presented as an aggressive-but-safe strategy. It generally is not: very low intakes make protein and micronutrient needs hard to meet, tend to cost lean mass alongside fat, and are hard to sustain. Set targets from TDEE, not BMR, and get medical supervision for any very low calorie approach.</p>', warn=True)),
        ('metabolism-myths', 'Four claims about metabolism worth checking', '''
<h3>&ldquo;Metabolism slows steadily from your twenties&rdquo;</h3>
<p>A large 2021 analysis published in <em>Science</em>, pooling doubly-labelled-water measurements from thousands of people across the lifespan, found that energy expenditure adjusted for body composition was broadly stable from around age 20 to age 60, with decline setting in after that. Weight gain through middle age is therefore less about a collapsing metabolism than about changes in activity, muscle mass and intake.</p>
<h3>&ldquo;Eating frequently keeps your metabolism running&rdquo;</h3>
<p>The thermic effect of food scales with how much you eat, not with how many sittings you spread it across. Controlled comparisons of meal frequency at matched total intake have generally found no meaningful difference in total energy expenditure. Meal timing can still matter for appetite, adherence and training &mdash; just not through metabolic rate.</p>
<h3>&ldquo;Certain foods burn fat&rdquo;</h3>
<p>Some compounds &mdash; caffeine and capsaicin among them &mdash; produce small, short-lived increases in energy expenditure in laboratory studies. The effects are modest and do not amount to a weight-management strategy on their own.</p>
<h3>&ldquo;Muscle burns a huge number of calories at rest&rdquo;</h3>
<p>Skeletal muscle uses roughly 13 kcal per kilogram per day at rest, so several kilograms of new muscle adds a few dozen calories daily, not hundreds. Resistance training is genuinely valuable &mdash; for strength, for bone, for preserving lean mass in a deficit, for the energy used during and after training &mdash; but its effect on resting metabolic rate alone is small.</p>
''' + worked(
    'Adding <b>3 kg of muscle</b> raises resting energy use by roughly <b>40 kcal a day</b> &mdash; about '
    'half a banana. The training that built it, and the lean mass it preserves while dieting, matter far '
    'more than the resting number does.', tag='Putting it in scale')),
    ],
    limits='''
<ul>
  <li><strong>Every figure on this page is an estimate from a population equation</strong>, typically within about 10% of a measured value for healthy adults, and less reliable outside that group.</li>
  <li><strong>Activity multipliers are coarse.</strong> Five bands cannot capture the real range of human movement, and NEAT alone varies by hundreds of calories a day between similar people.</li>
  <li><strong>Accuracy falls at the extremes</strong> of body size and age, and for people with thyroid, metabolic or muscle-wasting conditions.</li>
  <li><strong>The 7,700 kcal per kilogram rule is a simplification.</strong> It ignores metabolic adaptation, changes in activity, and the mix of fat and lean tissue actually lost.</li>
  <li><strong>These equations are for adults.</strong> They are not valid for children, and they are not designed for pregnancy or breastfeeding, both of which raise energy requirements.</li>
  <li><strong>The calculator cannot see your medical history</strong>, your medications or your training history, all of which affect both the number and what you should do with it.</li>
</ul>
''',
    seek_title='When to talk to a healthcare professional',
    seek='''
<p>It is worth involving a doctor or registered dietitian if:</p>
<ul>
  <li>You are considering a very low calorie intake, or a substantial deficit sustained over months.</li>
  <li>Your weight is changing in a way the numbers do not explain, in either direction.</li>
  <li>You have or suspect a thyroid condition, diabetes, or another condition that affects metabolism or appetite.</li>
  <li>You take medication that affects weight, appetite or blood glucose.</li>
  <li>You are pregnant, breastfeeding, or planning a pregnancy, since energy needs change and general-purpose equations do not account for it.</li>
  <li>You are an athlete managing weight for a competition category, where supervised planning makes a real difference.</li>
  <li>Eating has started to feel controlled by numbers, or tracking is causing distress. This is common and there is effective support for it.</li>
</ul>
''',
    disclaimer='''
<p><strong>This calculator is for general information and education.</strong> It estimates energy requirements from published prediction equations and does not provide medical or dietetic advice, diagnosis or treatment. The figures are population averages and may differ substantially from your own requirements. Before making significant changes to your diet &mdash; particularly alongside a health condition, a medication, pregnancy or breastfeeding &mdash; speak with a qualified healthcare professional.</p>
''',
    faqs=[
        ('What is the difference between BMR and RMR?',
         'BMR is measured under strict conditions: fully rested, fasted at least twelve hours, in a thermally neutral room. RMR is measured under more relaxed conditions and usually comes out a few per cent higher. Prediction equations sit between the two, which is why different sources can quote slightly different numbers for the same person. For everyday planning the difference is not material.'),
        ('Does BMR really slow down as you get older?',
         'Less, and later, than the common belief. A large 2021 analysis in Science found that energy expenditure adjusted for body composition stayed broadly stable between roughly age 20 and age 60, with decline becoming apparent after that. Weight gain in middle age is usually better explained by reduced activity and lost muscle mass than by a falling metabolic rate.'),
        ('How much does building muscle raise my BMR?',
         'Less than most people expect. Skeletal muscle uses roughly 13 kcal per kilogram per day at rest, so three kilograms of new muscle adds around 40 kcal daily. Resistance training is still well worth doing &mdash; for strength, bone health, and preserving lean mass during weight loss &mdash; but not primarily as a way to raise resting metabolism.'),
        ('Why do two calculators give me different BMR numbers?',
         'Because they are probably using different equations. Mifflin-St Jeor, Harris-Benedict and Katch-McArdle were derived from different populations and return different values for the same inputs, often differing by 100 kcal or more. Pick one equation, use it consistently, and judge it against what actually happens to your weight.'),
        ('Does metabolic adaptation make weight loss impossible?',
         'No, but it does make it slower than a straight calculation suggests. Sustained energy restriction reduces expenditure somewhat beyond what the loss of body mass alone predicts, and spontaneous daily movement often falls too. The practical response is to recalculate every few kilograms, protect lean mass with resistance training and adequate protein, and expect progress to require periodic adjustment.'),
    ],
)

# ==========================================================================
# Calories burned
# ==========================================================================
GUIDES_ENERGY['calories-burned'] = guide(
    intro='''
<p>Every activity has an energy cost, and that cost can be expressed as a multiple of what your body spends sitting still. That multiple is the MET value, and it is the basis of nearly every calories-burned estimate you will encounter &mdash; in this calculator, in gym equipment, and inside most fitness apps.</p>
<p>The arithmetic is straightforward. What is less obvious is how wide the error bars are, why your watch disagrees, and why the calories burned in a workout rarely translate into the weight change people expect. This article covers all three.</p>
''',
    sections=[
        ('met-values', 'MET values and intensity bands', '''
<p>One MET is the energy cost of sitting quietly, conventionally defined as about 3.5 millilitres of oxygen per kilogram of body weight per minute. An activity rated at 6 METs costs six times that.</p>
<p>The MET values used here come from the <strong>Compendium of Physical Activities</strong>, the reference dataset compiled by Ainsworth and colleagues that exercise science has used since 1993 and revised since. Public health guidance groups activities into three bands:</p>
''' + ref_table(
    'Activity intensity bands',
    [('Band', False), ('METs', True), ('Examples', False)],
    [
        ('Light', 'Under 3.0', 'Slow walking, desk work, light housework, gentle stretching'),
        ('Moderate', '3.0 &ndash; 5.9', 'Brisk walking, easy cycling, doubles tennis, general gardening'),
        ('Vigorous', '6.0 and above', 'Running, fast cycling, singles squash, circuit training, skipping'),
    ]) + '''
<p>The bands matter because physical activity guidelines are written in them. The World Health Organization recommends adults accumulate 150 to 300 minutes of moderate activity per week, or 75 to 150 minutes of vigorous activity, or an equivalent combination &mdash; plus muscle-strengthening work on two or more days.</p>
'''),
        ('comparing-activities', 'What different activities actually cost', '''
<p>Because the formula multiplies by body weight, the same activity costs a heavier person more. This table shows estimated energy for a 30-minute session at three body weights, calculated the same way the calculator does.</p>
''' + ref_table(
    'Estimated kcal for 30 minutes of activity, by body weight',
    [('Activity', False), ('MET', True), ('60 kg', True), ('75 kg', True), ('90 kg', True)],
    [
        ('Hatha yoga', '2.5', '79', '98', '118'),
        ('Cleaning, general housework', '3.3', '104', '130', '156'),
        ('Walking, 5 km/h, level', '3.5', '110', '138', '165'),
        ('Swimming, freestyle, moderate', '5.8', '183', '228', '274'),
        ('Resistance training, vigorous', '6.0', '189', '236', '284'),
        ('Cycling, 16&ndash;19 km/h', '6.8', '214', '268', '321'),
        ('Football, casual game', '7.0', '220', '276', '331'),
        ('Running, 8 km/h', '8.3', '261', '327', '392'),
        ('Running, 12 km/h', '11.5', '362', '453', '543'),
        ('Skipping rope, moderate', '11.8', '372', '465', '558'),
    ]) + '''
<p>Two patterns are worth noticing. A 90 kg person burns roughly 50% more than a 60 kg person doing exactly the same thing &mdash; which is also why calorie burn falls as you lose weight and why re-entering your weight periodically matters. And duration substitutes for intensity in the arithmetic: 60 minutes of brisk walking and 30 minutes of easy running land in much the same place.</p>
''' + worked(
    'A <b>75 kg</b> person cycling at 16&ndash;19 km/h (6.8 METs) for <b>45 minutes</b>: '
    '6.8 &times; 3.5 &times; 75 &divide; 200 = 8.9 kcal per minute, and 8.9 &times; 45 = '
    '<b>about 402 kcal</b> &mdash; gross, including the energy they would have spent resting anyway.')),
        ('what-changes-your-burn', 'What moves your real number away from the estimate', '''
<p>MET values are population averages measured on groups of adults in laboratories. Your session is not a laboratory. The things that shift the real figure:</p>
<ul>
  <li><strong>Body weight and composition.</strong> Built into the formula for weight; not built in for composition, though lean mass raises the true cost slightly.</li>
  <li><strong>Fitness and efficiency.</strong> A trained cyclist uses <em>less</em> energy than a beginner at the same speed, because technique and economy improve with practice. This is the counter-intuitive one: getting fitter lowers the cost of a fixed workload.</li>
  <li><strong>Terrain and gradient.</strong> Hills, sand, snow and rough ground can raise the cost substantially over the flat-surface values in the compendium.</li>
  <li><strong>Temperature and humidity.</strong> Both heat and cold raise energy cost, through thermoregulation and through reduced efficiency.</li>
  <li><strong>Altitude.</strong> Working at altitude raises the physiological cost of the same external workload.</li>
  <li><strong>Real intensity within an activity.</strong> &ldquo;Weight training&rdquo; covers everything from a gentle circuit to heavy sets with short rest. A single MET value cannot span that.</li>
  <li><strong>Equipment, load and technique.</strong> Carrying a pack, pushing a pram or using poor form all change the cost.</li>
</ul>
<p>Taken together, these are why 15 to 25% error for an individual session is a realistic expectation rather than a pessimistic one.</p>
'''),
        ('gross-vs-net', 'Gross calories, net calories and the afterburn', '''
<h3>Gross versus net</h3>
<p>This calculator reports <strong>gross</strong> energy expenditure &mdash; everything you burned during the activity. Some of that you would have burned anyway just by existing for the same period: roughly one MET-hour, or about 60 to 90 kcal per hour for most adults.</p>
<p><strong>Net</strong> expenditure subtracts that baseline and represents the additional cost of choosing to exercise. It is the more honest figure when you are thinking about energy balance, and it is meaningfully smaller: a one-hour session showing 400 gross kcal represents closer to 320 net. Gross is the standard convention for MET calculations and what most apps display, so it is what appears here &mdash; but the distinction is worth carrying.</p>
<h3>EPOC, the &ldquo;afterburn&rdquo;</h3>
<p>Energy expenditure stays slightly raised after exercise while the body restores oxygen stores, clears metabolites and repairs tissue. This is excess post-exercise oxygen consumption, or EPOC. It is real, it is larger after intense or prolonged sessions, and it is usually modest &mdash; commonly measured in the range of a few per cent to around 15% of the session&rsquo;s own cost. It is not the large hidden bonus it is sometimes marketed as.</p>
'''),
        ('exercise-and-weight', 'Exercise, appetite and energy balance', '''
<p>Exercise is one of the best-supported interventions in health, with effects on cardiovascular risk, blood glucose regulation, bone density, sleep, mood and mortality that no other single behaviour matches. It is a surprisingly weak tool for weight loss on its own, and understanding why prevents a lot of frustration.</p>
<h3>The numbers are smaller than they feel</h3>
<p>A demanding 45-minute session might cost 350 to 450 kcal gross for an average adult. That is real, but it is also one large coffee and a pastry. Diet changes move more calories per unit of effort; exercise wins decisively on everything else.</p>
<h3>It is a small share of your daily total</h3>
<p>Even for people who train regularly, deliberate exercise is usually a modest slice of daily energy use next to resting metabolism. The <a href="../bmr/index.html">BMR calculator</a> shows how the rest of it breaks down.</p>
<h3>Compensation is common</h3>
<p>People often eat somewhat more after exercise, and move somewhat less for the rest of the day, without noticing either. Both effects are well documented and both reduce the net energy deficit produced by a session.</p>
<h3>Estimates run optimistic</h3>
<p>Between population-average MET values, over-reported session duration and under-reported food intake, the gap between calculated and actual balance usually runs in the same direction. A common practical suggestion is to eat back at most half of an estimated burn, then judge by what your weight actually does over two to three weeks.</p>
''' + callout('<p><strong>A better frame.</strong> Treat exercise as the thing that makes you healthier, stronger and more resilient, and treat diet as the main lever for body weight. The two work well together and poorly as substitutes.</p>')),
    ],
    limits='''
<ul>
  <li><strong>MET values are laboratory population averages</strong>, not measurements of your session. Expect roughly 15 to 25% error for an individual.</li>
  <li><strong>Fitness, terrain, temperature, altitude, technique and equipment</strong> all move the true cost and none of them is an input here.</li>
  <li><strong>The figure is gross, not net</strong>, so it includes the energy you would have spent at rest during the same period.</li>
  <li><strong>One MET value has to cover a broad activity.</strong> &ldquo;Weight training&rdquo; or &ldquo;swimming&rdquo; spans a wide range of real intensities.</li>
  <li><strong>The compendium was compiled from healthy adults</strong> and is less applicable to children, to older adults with limited mobility, and to people with conditions affecting movement efficiency.</li>
  <li><strong>Burning calories is not the same as losing weight.</strong> Appetite and spontaneous activity both respond to training, and both affect the outcome.</li>
</ul>
''',
    seek_title='When to talk to a healthcare professional',
    seek='''
<p>It is worth speaking with a doctor, physiotherapist or qualified exercise professional if:</p>
<ul>
  <li>You are starting to exercise after a long period of inactivity, particularly if you are over 40 or have cardiovascular risk factors.</li>
  <li>You have a heart, lung, joint or metabolic condition, or you are recovering from surgery or injury.</li>
  <li>You experience chest pain, unusual breathlessness, dizziness or fainting during or after exercise. Symptoms like these need prompt medical attention rather than a calculator.</li>
  <li>You are pregnant or recently postpartum and want to know what activity is appropriate for your situation.</li>
  <li>You are combining a large calorie deficit with heavy training, where supervision genuinely helps.</li>
  <li>Exercise has started to feel compulsory, or you find it difficult to take rest days. That pattern is worth talking through with someone.</li>
</ul>
''',
    disclaimer='''
<p><strong>This calculator is for general information and education.</strong> It estimates energy expenditure from published MET values and does not provide medical advice, diagnosis or treatment. The figures are population averages and can differ substantially from your own energy cost. Before starting or significantly changing an exercise programme &mdash; especially alongside a health condition, injury, pregnancy or medication &mdash; speak with a qualified healthcare professional.</p>
''',
    faqs=[
        ('What is a MET value?',
         'A Metabolic Equivalent of Task expresses an activity&rsquo;s energy cost as a multiple of sitting quietly, which is defined as roughly 3.5 millilitres of oxygen per kilogram of body weight per minute. An activity at 7 METs costs about seven times your resting rate. The values used here come from the Compendium of Physical Activities, the standard reference dataset in exercise science.'),
        ('Why does my smartwatch show a different number?',
         'Wearables mostly estimate from heart rate, motion sensors and your profile rather than from MET tables, using proprietary algorithms. Heart-rate methods pick up some individual variation that MET values miss, but they carry their own error &mdash; often 10 to 20% or worse for activities that are not steady-state. Neither figure is authoritative; both are estimates built on different assumptions.'),
        ('Do I burn calories after the workout ends?',
         'Yes, a little. Energy expenditure stays elevated while your body restores oxygen stores and repairs tissue, an effect called EPOC. It is larger after intense or long sessions but generally modest &mdash; typically a few per cent up to around 15% of the session&rsquo;s own energy cost, rather than the large bonus it is sometimes claimed to be.'),
        ('Is walking or running better for burning calories?',
         'Running costs more per minute; walking costs more per unit of effort you are likely to sustain. Over a fixed distance the gap narrows considerably, since covering a kilometre costs broadly similar energy either way. The better question is which one you will do consistently &mdash; frequency beats intensity over any horizon longer than a few weeks.'),
        ('Can I lose weight through exercise alone?',
         'It is possible but inefficient, and the research is fairly consistent on this. Exercise alone produces modest weight loss compared with diet change or the two combined, partly because sessions cost fewer calories than people expect and partly because appetite and spontaneous movement adjust. Exercise is extremely worthwhile for health and for preserving muscle while losing weight &mdash; it is just not the strongest single lever on the scale.'),
    ],
)

# ==========================================================================
# Pace
# ==========================================================================
GUIDES_ENERGY['pace'] = guide(
    intro='''
<p>Pace is the language runners actually think in. Nobody plans a session around metres per second, but almost everyone knows what five minutes per kilometre feels like in their legs. It is the number that turns an abstract distance into a plan you can execute.</p>
<p>This guide covers how pace relates to speed, how to read the pace numbers you are given, how training paces differ and why that matters, how pace naturally changes as distance grows, and what actually makes people faster over time.</p>
''',
    sections=[
        ('reading-pace-numbers', 'Pace, speed and how to convert between them', '''
<p>Pace and speed describe the same thing from opposite directions. <strong>Pace</strong> is time per unit distance &mdash; minutes per kilometre or per mile &mdash; so lower is faster. <strong>Speed</strong> is distance per unit time, so higher is faster. To convert, divide 60 by the other one: 5:00/km is 12 km/h, and 12 km/h is 5:00/km.</p>
<p>The only trap is that pace is written in minutes and seconds while the arithmetic wants decimals &mdash; 5:30/km is 5.5, not 5.3. Runners favour pace because races are fixed distances: if you know your target pace, you know what each kilometre marker should read.</p>
<p>A reference for the paces most people work around. A mile is 1.609344 km exactly, so pace per mile is always pace per kilometre multiplied by that number.</p>
''' + ref_table(
    'Pace and speed equivalents',
    [('Per km', True), ('Per mile', True), ('Speed', True), ('Typical context', False)],
    [
        ('4:00', '6:26', '15.0 km/h', 'Competitive club running'),
        ('4:30', '7:15', '13.3 km/h', 'Strong recreational racing pace'),
        ('5:00', '8:03', '12.0 km/h', 'A common target for experienced runners'),
        ('5:30', '8:51', '10.9 km/h', 'Steady running for many regulars'),
        ('6:00', '9:39', '10.0 km/h', 'Comfortable aerobic pace'),
        ('7:00', '11:16', '8.6 km/h', 'Easy running, early training'),
        ('8:00', '12:52', '7.5 km/h', 'Very easy running or a fast walk'),
    ]) + '''
<p>Worth remembering when you compare yourself to anything online: a pace quoted per mile always looks slower than the same pace quoted per kilometre, because the distance is longer. Check which unit a figure is in before drawing conclusions from it.</p>
'''),
        ('training-paces', 'Why runners train at several different paces', '''
<p>Running every session at the same moderately hard effort is the most common training mistake, and it produces the least return. Different paces drive different physiological adaptations, and a programme that includes several of them outperforms one that does not.</p>
''' + ref_table(
    'Common training intensities',
    [('Session type', False), ('Effort', False), ('What it develops', False)],
    [
        ('Recovery', 'Very easy, conversational throughout', 'Blood flow and recovery without added fatigue'),
        ('Easy / base', 'Comfortable, full sentences possible', 'Aerobic capacity, capillaries, mitochondria, durability'),
        ('Long run', 'Easy pace, extended duration', 'Endurance, fat utilisation, mental resilience'),
        ('Tempo / threshold', 'Comfortably hard, short phrases only', 'Ability to hold a faster pace before fatigue accumulates'),
        ('Intervals', 'Hard, spoken words at best', 'Maximal aerobic capacity and running economy'),
        ('Strides', 'Fast but relaxed, 15&ndash;20 seconds', 'Mechanics, turnover and leg speed'),
    ]) + '''
<h3>The 80/20 idea</h3>
<p>A consistent finding in research on trained endurance athletes is that they spend the large majority of their training time at low intensity &mdash; often cited as roughly 80% easy, 20% hard. The trap for recreational runners is the middle ground: sessions run too fast to recover from and too slow to drive adaptation. Easy days should feel genuinely easy.</p>
<h3>The talk test</h3>
<p>The most reliable tool you already own. If you can hold a conversation in full sentences, you are in the easy zone. If you can manage short phrases, you are around threshold. If you can only get single words out, you are running hard. It self-adjusts for heat, hills, fatigue and how you slept, which no fixed pace target does.</p>
'''),
        ('pace-by-distance', 'How pace changes with distance', '''
<p>Nobody holds their 5K pace through a marathon. The relationship between distance and sustainable pace is predictable enough that it has been formalised.</p>
<p>The best-known version is <strong>Riegel&rsquo;s formula</strong>, published in 1981: predicted time equals your known time multiplied by the ratio of distances raised to the power 1.06. In everyday terms that works out at roughly <strong>4 to 5% slower each time the distance doubles</strong>, and higher exponents used by some variants push it nearer 6%.</p>
''' + worked(
    'A runner who covers <b>10 km in 50:00</b> (5:00/km) projects under Riegel to about <b>1:50</b> for a '
    'half marathon (5:14/km) and about <b>3:50</b> for a marathon (5:27/km). Those are ceilings for a '
    'runner who has trained for the distance, not promises.', tag='Worked prediction') + '''
<p>Two conditions sit behind every prediction of this kind, and both are routinely ignored. It assumes you have trained specifically for the longer distance &mdash; a marathon projection from a 10K time means little without long runs behind it. And it assumes similar conditions: heat, wind, hills and a crowded start all cost time that no formula accounts for.</p>
<p>The <a href="../calories-burned/index.html">calories burned calculator</a> covers the energy side of these distances, if that is what you are planning around.</p>
'''),
        ('pacing-a-race', 'Pacing a race', '''
<h3>Even splits and negative splits</h3>
<p>The split table on this page assumes perfectly even pacing. Real races rarely go that way &mdash; most runners start faster than planned and fade in the second half. Running the second half slightly faster than the first, a <strong>negative split</strong>, is how a large share of distance records and personal bests are set, because starting conservatively preserves glycogen and delays the point where fatigue forces a slowdown.</p>
<p>A practical version: run the first few kilometres 5 to 10 seconds per kilometre slower than target, then settle in. It feels far too easy at the time, and it repays that restraint several times over in the closing kilometres.</p>
<h3>What shifts your realistic pace on the day</h3>
<ul>
  <li><strong>Heat and humidity.</strong> The most significant environmental factor by a distance. Pace expectations should drop noticeably in warm conditions, more so for longer races.</li>
  <li><strong>Hills.</strong> Time lost on an ascent is generally not fully recovered on the descent, so a hilly course is slower than its flat equivalent even when the net elevation is zero.</li>
  <li><strong>Wind.</strong> A headwind costs more than an equivalent tailwind returns.</li>
  <li><strong>Altitude.</strong> Aerobic performance is reduced at altitude until you have adapted, which takes weeks.</li>
  <li><strong>Surface.</strong> Trail, sand and deep grass all cost time against road or track.</li>
  <li><strong>Crowding.</strong> Congested starts and narrow sections cost seconds that never come back.</li>
</ul>
'''),
        ('improving-pace', 'What actually makes you faster', '''
<p>General training principles, not a personalised plan. A coach can adapt them to your history, goals and the time you have.</p>
<h3>Consistency beats individual sessions</h3>
<p>Aerobic fitness is built through accumulated, repeated work. Three steady runs a week for six months does more than one heroic session a fortnight. The single most useful habit is showing up regularly at an easy effort.</p>
<h3>Build volume gradually</h3>
<p>The commonly quoted guidance is to increase weekly distance by no more than about 10% at a time. The exact figure is a rule of thumb rather than a validated threshold, but the principle behind it &mdash; that tendons, bone and connective tissue adapt more slowly than the cardiovascular system &mdash; is well supported.</p>
<h3>Include some faster running</h3>
<p>Once a consistent easy base exists, a weekly tempo or interval session improves the pace you can hold before fatigue accumulates. One hard session a week is plenty for most recreational runners; two is the upper end.</p>
<h3>Strength training supports running</h3>
<p>Resistance work is associated with improved running economy and is widely used to reduce injury risk. It does not make you slower or bulky at the volumes runners typically use.</p>
<h3>Recovery is where adaptation happens</h3>
<p>Training provides the stimulus; sleep and rest days produce the improvement. Persistently poor sleep undermines everything upstream of it.</p>
<h3>Cadence and form, cautiously</h3>
<p>Very low cadence combined with overstriding is associated with higher impact loading, and small increases in step rate are sometimes used to address it. Form changes are best made gradually and ideally with someone watching you run.</p>
'''),
    ],
    limits='''
<ul>
  <li><strong>Split times assume perfectly even pacing</strong>, which almost no real race follows.</li>
  <li><strong>Race predictions assume specific training</strong> for the target distance. Without it, the real result is usually considerably slower than the projection.</li>
  <li><strong>No environmental factors are modelled.</strong> Heat, humidity, wind, hills, altitude and surface all cost time that the arithmetic does not see.</li>
  <li><strong>GPS distance carries its own error</strong>, typically a per cent or two, and more under tree cover, between tall buildings or on twisting courses. Two watches on the same run routinely disagree.</li>
  <li><strong>The calculator knows nothing about your fitness, history or injury status</strong> &mdash; it solves an equation, it does not assess whether a target is appropriate for you.</li>
  <li><strong>Prediction formulas are population fits.</strong> Individual runners vary in how well they hold pace as distance increases, and specialists at either end of the range deviate the most.</li>
</ul>
''',
    seek_title='When to get professional input',
    seek='''
<p>A doctor, physiotherapist or qualified running coach is worth involving if:</p>
<ul>
  <li>You are returning to running after injury, illness, surgery or a long break.</li>
  <li>You have pain that persists during or after runs, or that changes how you move. Pain that alters your gait is worth assessing early rather than training through.</li>
  <li>You experience chest pain, unusual breathlessness, palpitations, dizziness or fainting while running. Seek prompt medical attention for symptoms like these.</li>
  <li>You have a cardiovascular, respiratory or metabolic condition and are increasing training load.</li>
  <li>You are pregnant or recently postpartum and want guidance on appropriate activity.</li>
  <li>You are training for a first marathon or ultra, where structured planning materially reduces the chance of injury.</li>
  <li>Training has started to feel compulsory, or you are struggling to take rest days.</li>
</ul>
''',
    disclaimer='''
<p><strong>This calculator is for general information and education.</strong> It performs arithmetic on the values you enter and does not assess your fitness, health or readiness for any distance. The training information on this page is general and is not a personalised plan. Before starting or significantly increasing a running programme &mdash; particularly with a health condition, an injury, or during and after pregnancy &mdash; speak with a qualified healthcare professional.</p>
''',
    faqs=[
        ('How do I work out my pace from a run?',
         'Divide your total time by the distance covered. A 42-minute 7 km run is 42 &divide; 7 = 6 minutes per kilometre. If the result is a decimal, multiply the part after the point by 60 to get seconds &mdash; 6.5 minutes is 6:30, not 6:50. The calculator above does the conversion for you either way.'),
        ('What is a good 5K time?',
         'It depends so heavily on age, training history and starting point that a single figure is not very useful. Many recreational runners finish somewhere between 25 and 35 minutes, plenty of newer runners are above that, and club runners are well below it. A more meaningful benchmark is your own previous time on a comparable course.'),
        ('Should I run by pace or by heart rate?',
         'Both have uses. Pace is precise, immediate and unaffected by caffeine, sleep or stress, which makes it good for intervals and race execution. Heart rate reflects internal effort and adjusts for heat, fatigue and illness, which makes it good for keeping easy days genuinely easy. Many runners use pace for hard sessions and effort or heart rate for easy ones.'),
        ('Why is my GPS distance different from the official race distance?',
         'Courses are measured along the shortest legal route, and almost nobody runs exactly that line &mdash; weaving around other runners and taking wide corners adds real distance. GPS also carries its own error of a per cent or two, more in cities or under trees. A watch reading slightly long on a certified course is normal and usually correct.'),
        ('How much can I realistically improve my pace?',
         'New runners often improve quickly in the first year, sometimes by minutes per kilometre, because so much of the early gain comes from basic aerobic adaptation. Improvement slows considerably after that, and experienced runners may work a full season for a few seconds per kilometre. Consistency over months and years is what separates the two curves.'),
    ],
)
