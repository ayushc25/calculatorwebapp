# -*- coding: utf-8 -*-
"""Educational articles for the body-composition calculators.

bmi, ideal-weight, body-fat. Rendered below the calculator by build.py.
"""

from guide import callout, guide
from parts import ref_table, worked

GUIDES_BODY = {}

# ==========================================================================
# BMI
# ==========================================================================
GUIDES_BODY['bmi'] = guide(
    intro='''
<p>Body Mass Index is the number you are most likely to meet first in any conversation about weight. It appears on health checks, insurance forms, clinical notes and fitness apps, usually with a one-word verdict attached to it. That makes it worth understanding properly &mdash; both what it is genuinely good at and where it quietly misleads.</p>
<p>The short version: BMI is a screening tool. It was built to describe populations, it costs nothing to calculate, and it correlates well enough with body fat across large groups to be useful in public health. What it is not is a measurement of your body, your health or your fitness. The sections below cover how to read your figure, what it cannot see, and which measurements are worth pairing it with.</p>
''',
    sections=[
        ('what-is-bmi', 'What BMI is, and where it came from', '''
<p>BMI expresses your weight relative to your height as a single number. Because taller people are heavier at the same build, dividing weight by height squared removes most of that effect and lets you compare bodies of different sizes on one scale.</p>
<p>The ratio was described in the 1830s by the Belgian statistician Adolphe Quetelet, who was studying the distribution of human measurements rather than anything clinical. It stayed a statistician&rsquo;s curiosity until 1972, when the American physiologist Ancel Keys tested several weight-for-height indices against measured body fat, found Quetelet&rsquo;s ratio performed best of the simple options, and gave it the name we use now.</p>
<p>That origin explains a lot. BMI was selected because it was the best <em>cheap</em> proxy available, in an era before body scanners, for comparing groups of people. It was never designed to say something precise about an individual, and Keys said as much at the time.</p>
'''),
        ('reading-your-number', 'Reading your number', '''
<p>The World Health Organization classification for adults aged 20 and over runs as follows. The sub-classes matter mainly in clinical settings, but they show how wide each headline band actually is.</p>
''' + ref_table(
    'WHO adult BMI classification',
    [('BMI', True), ('Classification', False), ('What it indicates', False)],
    [
        ('Under 16.0', 'Severe thinness', 'Substantially below the expected weight for height'),
        ('16.0 &ndash; 16.9', 'Moderate thinness', 'Below expected; worth clinical review'),
        ('17.0 &ndash; 18.4', 'Mild thinness', 'Slightly below the healthy band'),
        ('18.5 &ndash; 24.9', 'Healthy weight', 'The reference range for most adults'),
        ('25.0 &ndash; 29.9', 'Overweight (pre-obesity)', 'Above the reference range'),
        ('30.0 &ndash; 34.9', 'Obesity class I', 'Raised risk for several conditions at population level'),
        ('35.0 &ndash; 39.9', 'Obesity class II', 'Higher population-level risk'),
        ('40.0 and above', 'Obesity class III', 'Highest population-level risk band'),
    ]) + '''
<p>Two things are worth holding onto when you read your band. First, the boundaries are administrative lines drawn through a continuous distribution &mdash; nothing physiological changes between a BMI of 24.9 and 25.1. Second, these are risk associations observed across large groups, and a population-level association does not predict what will happen to any particular person in it.</p>
''' + callout('<p><strong>Reading a borderline figure.</strong> If your BMI sits within about a point of a category boundary, the category is not telling you much. Measurement error in height alone can move BMI by half a point. Look at the trend across several months rather than the label attached to one reading.</p>')),
        ('what-bmi-misses', 'What BMI cannot see', '''
<p>BMI takes in two numbers and gives back one. Everything else about your body is invisible to it.</p>
<ul>
  <li><strong>What your weight is made of.</strong> Muscle, bone, organs, water and fat all weigh the same on a scale. Two people at the same BMI can have very different body composition.</li>
  <li><strong>Where fat is stored.</strong> Visceral fat around the abdominal organs behaves differently from fat under the skin of the hips and thighs. BMI cannot distinguish them, though the difference matters more to metabolic health than the total does.</li>
  <li><strong>Bone density and frame.</strong> A broad, densely built skeleton adds weight that has nothing to do with fat.</li>
  <li><strong>Age-related changes.</strong> Adults tend to lose muscle and gain fat from middle age onward. An unchanged BMI across twenty years can hide a real shift in composition.</li>
  <li><strong>Fluid balance.</strong> Oedema, pregnancy and some medical conditions add weight that is water, not tissue.</li>
  <li><strong>Everything about how you live.</strong> Fitness, diet quality, sleep, blood pressure, blood lipids and blood glucose all carry independent information that BMI has no access to.</li>
</ul>
'''),
        ('other-measures', 'Measurements worth taking alongside it', '''
<p>BMI works best as one line in a short list rather than as a verdict on its own. These three are cheap, quick and add information BMI does not carry.</p>
<h3>Waist circumference</h3>
<p>Measured around the abdomen, this is a rough proxy for visceral fat, which is the deposit most consistently linked with metabolic risk in research. It is the single most useful companion measurement, partly because it can change noticeably while body weight barely moves.</p>
<h3>Waist-to-height ratio</h3>
<p>Divide your waist by your height in the same units. The commonly cited guidance, used in UK NICE guidance among others, is to keep the ratio below 0.5 &mdash; easy to remember as &ldquo;keep your waist under half your height&rdquo;. It needs no charts and applies reasonably across adult heights.</p>
<h3>Body-fat percentage</h3>
<p>The measure that answers what BMI cannot: how much of your weight is actually fat. The <a href="../body-fat/index.html">body fat calculator</a> estimates it from a few tape measurements, and pairing the two covers the main blind spot in each.</p>
<h3>How your clothes fit and how your training feels</h3>
<p>Less quantitative, but genuinely informative. Body composition can shift substantially with no movement on the scale at all, and people who train consistently often notice it in fit and performance long before any number reflects it.</p>
'''),
        ('different-populations', 'BMI across different groups', '''
<h3>Children and teenagers</h3>
<p>The adult categories do not apply below age 20. Children&rsquo;s BMI is plotted on age- and sex-specific growth charts and read as a percentile, because healthy body composition changes continuously through growth and puberty. A paediatrician or GP interprets those charts in the context of growth history.</p>
<h3>Asian populations</h3>
<p>A WHO expert consultation noted that many Asian populations show raised risk of type 2 diabetes and cardiovascular disease at a lower BMI than European populations, and proposed lower action points. Several national guidelines &mdash; including in India and China &mdash; use figures around 23 for overweight and 27.5 for obesity. If that applies to you, read your number against local guidance as well as the WHO default.</p>
<h3>Athletes and heavily trained people</h3>
<p>BMI misclassifies this group routinely. Muscle is denser than fat, so a lean, well-trained body can land squarely in the overweight band. Body-fat estimates and performance measures are far more useful here.</p>
<h3>Older adults</h3>
<p>Muscle mass declines with age, and low weight in later life carries its own risks. Some research suggests a slightly higher BMI is associated with better outcomes in older adults than in younger ones. Unintentional weight loss in an older adult is worth raising with a doctor regardless of which band it falls in.</p>
<h3>Pregnancy</h3>
<p>BMI calculated during pregnancy is not meaningful. What clinicians use is <em>pre-pregnancy</em> BMI, which guides expected weight-gain ranges. The <a href="../pregnancy/index.html">pregnancy calculator</a> covers that in more detail.</p>
'''),
    ],
    limits='''
<ul>
  <li><strong>BMI is not a measure of body fat.</strong> It cannot distinguish muscle from fat, or one fat distribution from another.</li>
  <li><strong>The categories are population screening bands.</strong> They describe average risk across large groups, not your individual health.</li>
  <li><strong>The cut-offs are not universal.</strong> Several countries use lower thresholds for people of Asian descent, and the adult bands do not apply to under-20s at all.</li>
  <li><strong>It does not apply during pregnancy</strong>, or to people with significant fluid retention, limb loss, or some muscle-wasting conditions.</li>
  <li><strong>Small input errors move the result.</strong> Rounding your height to the nearest centimetre can shift BMI by a few tenths, which is enough to cross a category line.</li>
  <li><strong>It says nothing about causes.</strong> Two people at the same BMI may have arrived there by entirely different routes, with entirely different health profiles.</li>
</ul>
''',
    seek_title='When to talk to a healthcare professional',
    seek='''
<p>General guidance, not a checklist for self-assessment. It may be worth speaking with a doctor or another qualified professional if:</p>
<ul>
  <li>Your BMI sits well outside the healthy band and you would like to understand what, if anything, it means for you.</li>
  <li>You have lost or gained weight without intending to.</li>
  <li>You are planning a significant change to how you eat or train, particularly alongside an existing health condition or medication.</li>
  <li>You have a family or personal history of diabetes, heart disease or high blood pressure, which changes how weight measures should be interpreted.</li>
  <li>Thoughts about weight, food or body image are causing you distress or affecting daily life. Support for this is available and effective.</li>
</ul>
''',
    disclaimer='''
<p><strong>This calculator is for general information and education.</strong> It does not provide medical advice, diagnosis or treatment, and a BMI figure on its own cannot tell you whether you are healthy. Decisions about your weight, diet, exercise or medical care should be made with a qualified healthcare professional who knows your history. If you have a medical concern, contact your doctor or local health service.</p>
''',
    faqs=[
        ('Who invented BMI and what was it designed for?',
         'The ratio was described by Adolphe Quetelet in the 1830s as part of statistical work on human measurements, and was named Body Mass Index by Ancel Keys in 1972 after he compared several weight-for-height indices against measured body fat. It was chosen as a cheap, reliable proxy for comparing populations &mdash; not as a way of assessing individuals, a distinction Keys himself made explicitly.'),
        ('Is waist circumference better than BMI?',
         'It is better at one specific thing: flagging abdominal fat, which carries more metabolic risk than fat stored elsewhere. Neither replaces the other. Using both, plus a waist-to-height ratio under roughly 0.5, gives a more complete picture than either alone.'),
        ('Can BMI be used during pregnancy?',
         'No. Weight gained in pregnancy reflects the baby, placenta, amniotic fluid and increased blood volume, so a BMI calculated while pregnant is not interpretable. Clinicians use pre-pregnancy BMI to set expected weight-gain ranges instead.'),
        ('Does BMI apply to people with a large frame?',
         'Only loosely. A broad, densely built skeleton adds weight that has nothing to do with fat, which nudges BMI upward. There is no validated way to adjust BMI for frame size, so the practical answer is to read the number alongside a waist measurement and a body-fat estimate rather than trying to correct it.'),
        ('How often should I recalculate my BMI?',
         'Monthly is more than enough for most purposes, measured under similar conditions &mdash; same time of day, similar hydration, similar clothing. Daily weight fluctuates by a kilogram or more from food, salt and fluid, so frequent readings mostly measure noise.'),
    ],
)

# ==========================================================================
# Ideal weight
# ==========================================================================
GUIDES_BODY['ideal-weight'] = guide(
    intro='''
<p>&ldquo;Ideal weight&rdquo; sounds like a fact waiting to be looked up. In practice it is a small family of estimates, written decades apart for purposes that had little to do with personal health goals, that disagree with each other by several kilograms at the same height.</p>
<p>That disagreement is the most useful thing about them. Four formulas, four answers, none of them wrong &mdash; which tells you there is no single correct weight for a given height. What each one really returns is a <strong>reference weight</strong>: roughly the weight of an average-build adult of that height in the population the formula was built from. Clinicians increasingly use that term, or <em>predicted body weight</em>, precisely because &ldquo;ideal&rdquo; implies a health judgement these equations were never able to make.</p>
<p>This guide covers how far apart the formulas are, where they are genuinely used, and how to set a weight target worth having.</p>
''',
    sections=[
        ('comparing-formulas', 'How far apart the formulas are', '''
<p>All four share the same structure: a base weight at five feet, plus a fixed increment for every inch above that. The constants differ, and the gaps widen as height increases. Here is what they produce at six common heights.</p>
''' + ref_table(
    'Reference weight in kg by formula and height',
    [('Height', False), ('Devine', True), ('Robinson', True), ('Miller', True), ('Hamwi', True)],
    [
        ('Men, 168 cm (about 5&prime;6&Prime;)', '64.1', '63.7', '64.9', '64.6'),
        ('Men, 178 cm (about 5&prime;10&Prime;)', '73.2', '71.1', '70.4', '75.2'),
        ('Men, 188 cm (about 6&prime;2&Prime;)', '82.2', '78.6', '76.0', '85.8'),
        ('Women, 158 cm (about 5&prime;2&Prime;)', '50.6', '52.7', '56.1', '50.4'),
        ('Women, 168 cm (about 5&prime;6&Prime;)', '59.6', '59.4', '61.5', '59.0'),
        ('Women, 178 cm (about 5&prime;10&Prime;)', '68.7', '66.1', '66.8', '67.7'),
    ]) + '''
<p>At 188 cm the spread between the highest and lowest answer is close to ten kilograms. No formula is more &ldquo;right&rdquo; than the others; they simply encode different assumptions. When four reasonable methods disagree by that much, the range &mdash; not any single figure inside it &mdash; is the honest answer.</p>
'''),
        ('ideal-vs-healthy', 'Reference weight versus healthy weight range', '''
<p>These are different ideas, and mixing them up causes most of the confusion around this calculator.</p>
<ul>
  <li>A <strong>reference weight</strong> is a single number produced by a formula from your height and sex. It is precise and arbitrary.</li>
  <li>A <strong>healthy weight range</strong> is the span of weights that put you between a BMI of 18.5 and 24.9 at your height. It is imprecise and grounded in population health data.</li>
</ul>
<p>The range is almost always the more useful of the two. At 175 cm it runs from roughly 57 to 76 kg &mdash; a span of nearly twenty kilograms, all of it inside the healthy screening band. A single &ldquo;ideal&rdquo; figure sitting somewhere in there implies a precision that does not exist.</p>
<p>The <a href="../bmi/index.html">BMI calculator</a> shows this range directly, and explains what it does and does not cover.</p>
'''),
        ('what-is-left-out', 'What the formulas leave out', '''
<p>Only two inputs go in: height and sex. Everything below is invisible to the calculation, and every one of them affects what a healthy weight looks like for a real person.</p>
<ul>
  <li><strong>Body composition.</strong> A muscular 85 kg and a sedentary 85 kg at the same height are not comparable, but the formula treats them identically.</li>
  <li><strong>Frame size.</strong> Bone structure varies substantially between people of the same height. Older clinical practice adjusted results by roughly 10% for small or large frames, but that adjustment has weak evidence behind it.</li>
  <li><strong>Age.</strong> Body composition shifts across adulthood; the formulas return the same answer at 25 and at 75.</li>
  <li><strong>Ancestry and reference population.</strong> All four were derived from mid-twentieth-century North American data.</li>
  <li><strong>Health history.</strong> Existing conditions, medications, pregnancy and recovery from illness all change what weight is appropriate.</li>
  <li><strong>Everything behavioural.</strong> Fitness, diet quality, sleep and strength carry information about health that weight alone does not.</li>
</ul>
'''),
        ('clinical-uses', 'Where these formulas are genuinely used', '''
<p>Reference body weight remains a working clinical tool &mdash; just not for telling people what to weigh. Its real uses share a common logic: some physiological quantity scales with lean body size rather than with total weight, and a height-based reference weight is a usable stand-in.</p>
<ul>
  <li><strong>Medication dosing.</strong> The Devine formula was published in 1974 specifically to scale aminoglycoside doses. Several drug classes are still dosed on reference or adjusted body weight, because fat tissue takes up some drugs very differently from lean tissue.</li>
  <li><strong>Ventilator settings.</strong> Lung volume tracks height, not weight, so lung-protective ventilation sets tidal volume per kilogram of <em>predicted</em> body weight. Using actual weight in a larger patient would over-inflate the lungs.</li>
  <li><strong>Nutrition support.</strong> Calculating energy and protein targets for tube or intravenous feeding often starts from a reference or adjusted weight.</li>
  <li><strong>Kidney function estimates.</strong> Some creatinine clearance equations take reference body weight as an input.</li>
</ul>
<p>In all of these the formula is a practical approximation inside a wider clinical judgement &mdash; which is a good spirit in which to read your own result too.</p>
'''),
        ('setting-a-target', 'Setting a weight target that is actually useful', '''
<p>If you want a number to work toward, a few principles make it more likely to be worth having.</p>
<h3>Aim at a range, not a point</h3>
<p>Body weight moves by one to two kilograms across a normal week from food volume, salt, fluid and hormonal cycles. A target range of three or four kilograms absorbs that noise; a single number turns ordinary fluctuation into apparent failure.</p>
<h3>Modest changes carry most of the benefit</h3>
<p>Research on weight loss and metabolic health consistently finds that a reduction of around 5 to 10% of starting weight is associated with meaningful improvements in blood pressure, blood glucose and blood lipids. That is a far more reachable target than any formula weight, and it is defined relative to where you actually are.</p>
<h3>Judge the process, not only the outcome</h3>
<p>Weight is a lagging, noisy indicator of things you control more directly: what you eat, how you train, how you sleep. Targets set on those tend to survive longer than targets set on the scale. Waist circumference and a <a href="../body-fat/index.html">body-fat estimate</a> both respond to change sooner than the scale does, which makes them better things to watch week to week.</p>
''' + worked(
    'Someone at <b>92 kg</b> aiming for a formula weight of <b>72 kg</b> is looking at a 20 kg gap. '
    'A first target of <b>5 to 10%</b> &mdash; roughly 87 to 83 kg &mdash; is the range most associated '
    'with measurable health improvement, and it is reachable in months rather than years.',
    tag='A more useful target')),
    ],
    limits='''
<ul>
  <li><strong>No ideal weight formula was validated against health outcomes.</strong> They describe population averages, not the weight at which a person is healthiest.</li>
  <li><strong>Only height and sex are used.</strong> Frame, muscle mass, age, ancestry and medical history are absent from every one of them.</li>
  <li><strong>The four formulas disagree</strong> by up to roughly ten kilograms at taller heights, which puts a ceiling on how precisely any of them can be read.</li>
  <li><strong>They were built from mid-twentieth-century North American data</strong> and were not designed for global use.</li>
  <li><strong>They do not apply to children or adolescents</strong>, who are assessed on growth charts instead.</li>
  <li><strong>They are a poor fit for athletes</strong>, for whom body composition and performance are far more informative than total weight.</li>
</ul>
''',
    seek_title='When to talk to a healthcare professional',
    seek='''
<p>Speaking with a doctor or registered dietitian is worth considering if:</p>
<ul>
  <li>You want a weight target tailored to your health history rather than to a formula.</li>
  <li>You are planning a substantial change in weight, in either direction.</li>
  <li>You have a condition or take a medication that affects weight, appetite or metabolism.</li>
  <li>Your weight has changed noticeably without you intending it to.</li>
  <li>You are underweight, or weight loss has become difficult to stop.</li>
  <li>Thoughts about weight or food are taking up more space than you would like. Disordered eating is common, treatable, and not something to work through alone.</li>
</ul>
''',
    disclaimer='''
<p><strong>This calculator is for general information and education.</strong> The formulas shown are historical clinical reference equations, not personal health targets, and this page does not provide medical advice, diagnosis or treatment. Any decision about changing your weight, diet or exercise &mdash; particularly alongside an existing condition or medication &mdash; should involve a qualified healthcare professional who knows your circumstances.</p>
''',
    faqs=[
        ('Is there really no single ideal weight for my height?',
         'No, and the four formulas disagreeing by several kilograms is the clearest evidence of it. Healthy weight is a range rather than a point, it depends on body composition and health history as much as on height, and it shifts across a lifetime. A range you can live inside is a more realistic and more useful target than any single figure.'),
        ('Why are the formulas different for men and women?',
         'They were derived from population data in which average body composition differed by sex &mdash; broadly, higher average lean mass in men and higher essential fat in women. The formulas encode that average difference as a different base weight. Like everything else in them, it is a population average and says nothing about an individual.'),
        ('Can I adjust the result for my frame size?',
         'Some older clinical practice adjusted by roughly 10% up or down for large or small frames, judged by wrist circumference or elbow breadth. The evidence behind that adjustment is weak and it is not part of the published formulas, so this calculator does not apply it. Treat frame size as a reason to read the result loosely rather than to compute a new one.'),
        ('What weight should I aim for if the formulas disagree?',
         'A practical approach is to use the healthy BMI range for your height as the outer boundary, then set a nearer target relative to where you are now &mdash; a 5 to 10% change is the amount most consistently associated with measurable health improvement. A dietitian or doctor can help set something specific to you.'),
        ('Do these formulas work for older adults?',
         'Less well. Muscle mass declines with age while the formula output stays fixed, so an older adult can meet the reference weight while carrying proportionally more fat and less lean tissue. In later life, unintentional weight loss and loss of muscle strength are generally more important signals than weight relative to a formula.'),
    ],
)

# ==========================================================================
# Body fat
# ==========================================================================
GUIDES_BODY['body-fat'] = guide(
    intro='''
<p>Body-fat percentage answers the question weight alone cannot: what is your body actually made of? Two people at the same height and weight can carry very different amounts of fat and muscle, and that difference matters more to health and performance than the number on the scale.</p>
<p>Measuring it precisely takes a laboratory. Estimating it usefully takes a tape measure and some care. This article covers what the percentage represents, what counts as a typical range, how the various measurement methods compare, and why your reading moves around from day to day even when your body has not changed.</p>
''',
    sections=[
        ('what-is-body-fat', 'What body-fat percentage represents', '''
<p>Body-fat percentage is the share of your total body mass made up of fat tissue. Everything else &mdash; muscle, bone, organs, blood, water, connective tissue &mdash; is grouped together as <strong>lean body mass</strong>, also called fat-free mass.</p>
<p>So someone weighing 80 kg at 20% body fat carries 16 kg of fat and 64 kg of everything else. Both halves of that split are informative. Fat mass is what most people are trying to change; lean mass is what most people are trying to protect while they change it.</p>
<p>This is why body-fat percentage can move in ways that look strange next to body weight. Gaining two kilograms of muscle while losing two kilograms of fat leaves your weight identical and your body composition meaningfully different.</p>
'''),
        ('essential-vs-storage', 'Essential fat and storage fat', '''
<p>Not all body fat is spare. It divides into two functional categories.</p>
<h3>Essential fat</h3>
<p>Fat that is structurally necessary &mdash; in bone marrow, the brain and nervous system, cell membranes, and the tissue surrounding organs. Commonly cited estimates put this at roughly 2 to 5% of body mass in men and 10 to 13% in women, the difference reflecting fat associated with reproductive and hormonal function. Below these levels the body cannot operate normally.</p>
<h3>Storage fat</h3>
<p>Energy reserve, held in adipose tissue. It splits again by location:</p>
<ul>
  <li><strong>Subcutaneous fat</strong> sits under the skin. It is what you can pinch, and it is the less metabolically active of the two.</li>
  <li><strong>Visceral fat</strong> sits deeper, around the abdominal organs. It is more metabolically active and is the deposit most consistently associated with cardiometabolic risk in research.</li>
</ul>
<p>Circumference methods, including the one this calculator uses, pick up some of this distribution indirectly through the waist measurement &mdash; part of why waist size carries information that weight does not.</p>
'''),
        ('reference-ranges', 'Typical reference ranges', '''
<p>These are commonly published descriptive bands, widely used in fitness and exercise settings. They describe how populations distribute; they are not targets anyone needs to reach.</p>
''' + ref_table(
    'Commonly cited body-fat ranges for adults',
    [('Category', False), ('Men', True), ('Women', True)],
    [
        ('Essential fat', '2&ndash;5%', '10&ndash;13%'),
        ('Athletes', '6&ndash;13%', '14&ndash;20%'),
        ('Fitness', '14&ndash;17%', '21&ndash;24%'),
        ('Acceptable', '18&ndash;24%', '25&ndash;31%'),
        ('Above the typical range', '25% and over', '32% and over'),
    ]) + '''
<p>These bands say what BMI cannot, which is why the two are usually read together &mdash; the <a href="../bmi/index.html">BMI calculator</a> explains where that measure works and where it misleads.</p>
<p>Two caveats before you compare yourself to the table. Women carry more essential fat than men for physiological reasons, so the two columns are not interchangeable and a woman at a &ldquo;male athlete&rdquo; percentage is not healthier for it. And these bands do not adjust for age, although body composition shifts steadily across adulthood.</p>
''' + callout('<p><strong>Lower is not automatically better.</strong> Very low body fat is associated with hormonal disruption, reduced bone density, impaired immune function, poor recovery and mood disturbance. Competitive athletes who reach very low percentages generally do so briefly and with professional support.</p>', warn=True)),
        ('measurement-methods', 'How body fat is measured', '''
<p>Every method is an estimate; they differ in what they measure directly and how much error they carry. None measures fat tissue itself &mdash; they infer it from density, electrical resistance, X-ray absorption or body dimensions.</p>
''' + ref_table(
    'Comparison of body-composition methods',
    [('Method', False), ('How it works', False), ('Typical error', False), ('Practicality', False)],
    [
        ('DEXA scan', 'X-ray absorption at two energies', 'About 1&ndash;2 points', 'Clinic only, costly'),
        ('Hydrostatic weighing', 'Underwater weight gives body density', 'About 2 points', 'Lab only, uncomfortable'),
        ('Air displacement (Bod Pod)', 'Body volume from air pressure', 'About 2&ndash;3 points', 'Lab only'),
        ('Skinfold callipers', 'Subcutaneous fat at set sites', '3&ndash;5 points', 'Cheap, needs a trained tester'),
        ('Circumference (US Navy)', 'Ratios between tape measurements', '3&ndash;4 points', 'Free, do it at home'),
        ('Bioelectrical impedance', 'Resistance to a small current', '3&ndash;8 points', 'Smart scales, handheld devices'),
    ]) + '''
<p>DEXA is the practical reference standard outside research settings, which is why other methods are usually validated against it. Bioelectrical impedance &mdash; the technology in most smart scales &mdash; is the most convenient and the most variable, because body water strongly affects conductivity. It tends to read differently before and after meals, exercise or a night&rsquo;s sleep.</p>
<p>For home use the honest ranking is: consistency beats precision. A method with a three-point offset that you apply identically every month will track your real change better than an occasional scan taken under different conditions each time.</p>
'''),
        ('what-moves-the-reading', 'Why your reading moves when your body has not', '''
<p>Short-term swings in any body-fat estimate are mostly measurement conditions, not tissue. The usual causes:</p>
<ul>
  <li><strong>Hydration.</strong> A dehydrated body reads differently on impedance devices and measures slightly differently with a tape. This is the single largest source of day-to-day variation.</li>
  <li><strong>Food and digestion.</strong> Abdominal circumference changes noticeably across a day, especially after large or high-fibre meals.</li>
  <li><strong>Time of day.</strong> Fluid redistributes overnight, so morning readings differ systematically from evening ones.</li>
  <li><strong>Tape placement and tension.</strong> A centimetre of difference at the waist can move the result by more than a percentage point. Consistent landmarks matter more than perfect ones.</li>
  <li><strong>The menstrual cycle.</strong> Fluid retention varies across the cycle, which affects both circumference and impedance readings.</li>
  <li><strong>Recent training.</strong> Hard exercise causes temporary fluid shifts and muscle swelling.</li>
</ul>
<p>The practical response is to standardise: same time of day, same conditions, same tape, same landmarks, ideally the same person taking the measurement. Then read the trend over months rather than the difference between two Tuesdays.</p>
'''),
    ],
    limits='''
<ul>
  <li><strong>The US Navy method is an estimate from a population equation</strong>, typically within about 3 to 4 percentage points of a DEXA scan &mdash; not a measurement of your tissue.</li>
  <li><strong>Accuracy falls at the extremes.</strong> Very lean and very heavy bodies, and anyone whose fat distribution is unusual, are estimated less reliably.</li>
  <li><strong>Tape technique dominates the error.</strong> Inconsistent placement or tension moves the result more than most real short-term changes do.</li>
  <li><strong>The reference ranges are descriptive.</strong> They are not clinical thresholds, are not adjusted for age, and are not treatment targets.</li>
  <li><strong>It is not valid during pregnancy</strong>, or where there is significant fluid retention or oedema.</li>
  <li><strong>A single reading tells you little.</strong> The method is built for tracking direction over months, not for producing one authoritative figure.</li>
</ul>
''',
    seek_title='When to talk to a healthcare professional',
    seek='''
<p>It may be worth speaking with a doctor, registered dietitian or qualified coach if:</p>
<ul>
  <li>You are aiming for a very low body-fat percentage, particularly for a competition or a physique goal.</li>
  <li>You have noticed changes that can accompany very low body fat &mdash; persistent fatigue, frequent illness, loss of menstrual periods, poor recovery, or stress fractures.</li>
  <li>Your body composition has changed substantially without you intending it.</li>
  <li>You have a condition or medication that affects weight, appetite, fluid balance or metabolism.</li>
  <li>Measuring and tracking has started to feel compulsive, or thoughts about body composition are causing distress. Support for this exists and works.</li>
</ul>
''',
    disclaimer='''
<p><strong>This calculator is for general information and education.</strong> It estimates body-fat percentage from a published population equation and does not provide medical advice, diagnosis or treatment. It cannot assess your health and should not be used to guide medical decisions. For advice about body composition, nutrition or training that accounts for your own circumstances, speak with a qualified healthcare professional.</p>
''',
    faqs=[
        ('What is the difference between body fat and BMI?',
         'BMI compares weight to height and cannot tell muscle from fat. Body-fat percentage estimates what proportion of your weight is fat tissue. They agree reasonably for people in the middle of the distribution and disagree at the edges &mdash; muscular people and people with low muscle mass are exactly where BMI misleads and a body-fat estimate clarifies.'),
        ('Why do smart scales give a different number?',
         'Most smart scales use bioelectrical impedance, which infers composition from how easily a small current passes through the body. Because that depends heavily on body water, readings shift with hydration, meals, exercise and time of day, and different devices use different proprietary equations. A gap of several percentage points between a scale and a tape estimate is normal.'),
        ('Can I lose fat from one specific area?',
         'Controlled studies have not supported spot reduction. Training a muscle strengthens that muscle, but the fat used for energy is drawn from the body as a whole, in a pattern that largely follows genetics and hormones. Overall fat loss eventually reaches the areas you care about, just not in the order you would choose.'),
        ('Does body-fat percentage change with age?',
         'Typically yes. Muscle mass tends to decline gradually from middle age unless it is actively maintained, so body-fat percentage often rises even when body weight is unchanged. Resistance training and adequate protein are the two factors most consistently associated with slowing that shift.'),
        ('Is a waist measurement enough on its own?',
         'It is a genuinely useful measurement, particularly as a proxy for abdominal fat, and it responds to change quickly. But it cannot give you a percentage and it does not account for height or overall size. Waist plus a body-fat estimate plus weight covers more ground than any of the three alone.'),
    ],
)
