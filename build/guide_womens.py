# -*- coding: utf-8 -*-
"""Educational articles for the period, pregnancy and bra size calculators.

These three carry the most sensitive subject matter on the site. The copy
stays general and educational throughout: no diagnosis, no symptom checking,
no personalised medical advice, and an explicit route to a clinician.
"""

from guide import callout, guide
from parts import ref_table, worked

GUIDES_WOMENS = {}

# ==========================================================================
# Period
# ==========================================================================
GUIDES_WOMENS['period'] = guide(
    intro='''
<p>A menstrual cycle is a monthly sequence of hormonal changes, and the period itself is only the visible part of it. Understanding the rest &mdash; what happens between periods, why ovulation timing moves, and how much variation is ordinary &mdash; makes the dates this calculator produces much easier to interpret.</p>
<p>This guide covers the phases of the cycle, what the research describes as typical, how ovulation and the fertile window are estimated, why cycles shift from month to month, and what is worth tracking if you want better information than a calendar can give you.</p>
''',
    sections=[
        ('understanding-the-cycle', 'Understanding the menstrual cycle', '''
<p>By convention the cycle is counted from the first day of bleeding. It runs in four phases, driven by four hormones working in sequence.</p>
''' + ref_table(
    'Phases of a typical 28-day cycle',
    [('Phase', False), ('Typical days', True), ('What happens', False)],
    [
        ('Menstrual', '1&ndash;5', 'The uterine lining is shed; this is the period itself'),
        ('Follicular', '1&ndash;13', 'FSH matures ovarian follicles; rising oestrogen rebuilds the lining'),
        ('Ovulation', 'Around 14', 'An LH surge triggers release of a mature egg'),
        ('Luteal', '15&ndash;28', 'The corpus luteum produces progesterone; the lining is maintained'),
    ]) + '''
<p>If the egg is not fertilised, the corpus luteum breaks down, progesterone and oestrogen fall, and the lining is shed &mdash; which is day one of the next cycle. The follicular phase overlaps the menstrual phase, which is why the day ranges above are not sequential blocks.</p>
<h3>The two halves behave very differently</h3>
<p>This is the single most useful thing to understand about cycle timing. The <strong>luteal phase</strong>, from ovulation to the next period, is relatively consistent &mdash; usually 12 to 16 days, averaging around 14. The <strong>follicular phase</strong>, from the period to ovulation, is the variable one, and it is what makes one person&rsquo;s cycle 25 days and another&rsquo;s 34.</p>
<p>The practical consequence: ovulation is better estimated by counting <em>backwards</em> from the next expected period than forwards from the last one. On a 32-day cycle, ovulation lands nearer day 18 than day 14 &mdash; a four-day difference that matters if you are using the dates for anything.</p>
'''),
        ('what-is-typical', 'What counts as typical', '''
<p>Descriptive ranges from clinical and epidemiological literature. They describe how populations distribute, not a standard anyone is expected to meet.</p>
''' + ref_table(
    'Commonly described ranges for adults',
    [('Measure', False), ('Typical range', False)],
    [
        ('Cycle length', '21 to 35 days'),
        ('Days of bleeding', '2 to 7 days'),
        ('Variation between your own cycles', 'Within about 7 to 9 days'),
        ('Luteal phase length', '12 to 16 days'),
        ('Fertile window', 'About 6 days ending on the day of ovulation'),
    ]) + '''
<p>Adolescents in the first few years after their first period commonly have longer and more variable cycles, sometimes up to around 45 days, as the hormonal system settles. Cycles often become irregular again in the years approaching menopause.</p>
<p>How much <em>your own</em> cycles vary tends to be more informative than where the average sits. Consistent 33-day cycles are ordinary; cycles swinging between 24 and 38 days are worth mentioning to a clinician even though both numbers fall inside the typical range.</p>
'''),
        ('ovulation-and-fertility', 'Ovulation and the fertile window', '''
<p>Ovulation is the release of a mature egg, usually one per cycle. The egg remains viable for roughly 12 to 24 hours afterwards.</p>
<p>The fertile window is longer than that because sperm survive. In fertile cervical mucus, sperm can remain viable in the reproductive tract for up to about five days. So the window opens roughly five days before ovulation and closes about a day after it &mdash; six days in total &mdash; with the highest probability of conception in the two days immediately before ovulation.</p>
<h3>Signs that ovulation is approaching</h3>
<p>These are the indicators commonly used in fertility awareness, described here for general understanding rather than as instructions:</p>
<ul>
  <li><strong>Cervical mucus changes.</strong> Mucus typically becomes clearer, more slippery and stretchier in the days before ovulation, often compared to raw egg white.</li>
  <li><strong>Basal body temperature.</strong> Resting temperature rises slightly after ovulation, driven by progesterone. Because the rise comes <em>after</em> the event, charting confirms ovulation retrospectively rather than predicting it.</li>
  <li><strong>Ovulation predictor kits.</strong> These detect the LH surge in urine, which typically precedes ovulation by around 24 to 36 hours.</li>
  <li><strong>Mid-cycle discomfort.</strong> Some people notice one-sided lower abdominal sensation around ovulation, sometimes called mittelschmerz. Many people notice nothing at all, and its absence means nothing.</li>
</ul>
''' + callout('<p><strong>Calendar prediction is not contraception.</strong> Ovulation timing shifts between cycles even in regular ones, and sperm survive for days. Typical-use failure rates for calendar-based methods are high. If you are preventing pregnancy, use a method designed for that purpose and discuss the options with a healthcare provider. Formal fertility awareness methods require training and daily observation, not a calendar alone.</p>', warn=True)),
        ('why-cycles-vary', 'Why cycles vary', '''
<p>A cycle is not a clock. Ovulation is the outcome of a hormonal cascade that responds to a great deal of what is going on in the rest of your life, and delaying ovulation delays the period that follows it. Factors commonly associated with shifts in cycle timing include:</p>
<ul>
  <li><strong>Psychological stress</strong> and periods of high demand.</li>
  <li><strong>Sleep disruption</strong>, including shift work and travel across time zones.</li>
  <li><strong>Illness</strong>, including short infections and fevers.</li>
  <li><strong>Substantial weight change</strong> in either direction, and low energy availability.</li>
  <li><strong>Intense or sharply increased exercise</strong>, particularly alongside inadequate fuelling.</li>
  <li><strong>Pregnancy and breastfeeding.</strong> Breastfeeding commonly suppresses ovulation for a period after birth. If a period is late and pregnancy is possible, the <a href="../pregnancy/index.html">pregnancy calculator</a> covers how dating works.</li>
  <li><strong>Starting, stopping or switching hormonal contraception.</strong> Bleeding on combined pills is a withdrawal bleed rather than a true period.</li>
  <li><strong>Perimenopause</strong>, when cycles typically become less predictable over several years.</li>
  <li><strong>Underlying conditions</strong> such as polycystic ovary syndrome, thyroid disorders, endometriosis and uterine fibroids, all of which can affect cycle length, bleeding or both.</li>
  <li><strong>Some medications.</strong> If you are unsure whether something you take is relevant, a pharmacist or doctor can tell you.</li>
</ul>
<p>Research on large numbers of cycle-tracking app users has found that even people who describe their cycles as regular ovulate across a spread of several days from month to month. Variation is the normal case, not the exception.</p>
'''),
        ('tracking-your-cycle', 'Tracking your cycle', '''
<p>A calendar projection is only as good as the average behind it. A few cycles of real data make the estimates noticeably better, and they give a clinician something concrete to work from if you ever need one.</p>
<h3>What is worth recording</h3>
<ul>
  <li><strong>The first day of bleeding</strong> every cycle. This one entry drives everything else.</li>
  <li><strong>How many days bleeding lasts</strong>, and a rough sense of flow.</li>
  <li><strong>Any mid-cycle observations</strong> you choose to track &mdash; mucus changes, temperature, LH test results.</li>
  <li><strong>Notable context</strong>: illness, travel, unusual stress, a change in training or medication. These explain outliers that would otherwise look alarming.</li>
</ul>
<h3>How much data before the average means anything</h3>
<p>Three cycles gives a rough sense; six or more gives a usable average and, more importantly, shows how much your cycles vary. That variation figure is often the more useful output &mdash; someone with a range of two days and someone with a range of twelve should read the same projected date very differently.</p>
''' + worked(
    'Six recorded cycles of <b>27, 29, 28, 31, 28 and 30 days</b> average <b>28.8 days</b> and range across '
    '<b>4 days</b>. A projected date from that data is reasonably firm. The same average built from cycles of '
    '22, 35, 26, 33, 27 and 30 days would not be.', tag='Why the spread matters')),
    ],
    limits='''
<ul>
  <li><strong>This is a calendar projection, not a measurement.</strong> It assumes your next cycles will resemble the average you entered.</li>
  <li><strong>Ovulation dates are the least certain output.</strong> Ovulation timing shifts between cycles even when cycle length looks stable.</li>
  <li><strong>It is not a contraceptive method</strong> and must not be used as one.</li>
  <li><strong>It does not apply on hormonal contraception</strong>, during pregnancy or breastfeeding, or through perimenopause, where the underlying assumptions break down.</li>
  <li><strong>It cannot detect or rule out anything.</strong> It has no information about your health, and an unexpected date means nothing clinically on its own.</li>
  <li><strong>Irregular cycles make projections much weaker.</strong> If your cycles vary by more than about a week, treat every date as a rough indication.</li>
</ul>
''',
    seek_title='When to speak with a healthcare professional',
    seek='''
<p>General guidance about when professional input is usually appropriate. It is not a diagnostic checklist, and anything that concerns you is reason enough to ask.</p>
<ul>
  <li>Periods stop for three months or more and pregnancy is not the explanation.</li>
  <li>Cycles are consistently shorter than 21 days or longer than 35, or the variation between them is more than about seven to nine days.</li>
  <li>Bleeding is unusually heavy, lasts longer than seven days, or requires changing protection very frequently.</li>
  <li>There is bleeding between periods, after sex, or after menopause.</li>
  <li>Period pain regularly interferes with work, study, sleep or daily activities.</li>
  <li>Premenstrual symptoms significantly affect your mood, relationships or ability to function.</li>
  <li>You have been trying to conceive for twelve months without success, or six months if you are over 35.</li>
  <li>Your cycle pattern changes noticeably and stays changed without an obvious explanation.</li>
</ul>
''',
    disclaimer='''
<p><strong>This calculator is for general information and education.</strong> It projects dates arithmetically from what you enter and does not provide medical advice, diagnosis or treatment. It cannot detect pregnancy, confirm ovulation, assess fertility or identify any medical condition, and it must not be relied on as a method of contraception. For anything concerning your cycle, fertility or reproductive health, speak with a doctor, gynaecologist or another qualified healthcare professional. Your dates are calculated in your browser and are never sent to a server.</p>
''',
    faqs=[
        ('Why do the calculator dates not match what actually happened?',
         'Because a projection assumes your next cycle will match your average, and cycles genuinely vary. Ovulation can be delayed by stress, illness, travel, disrupted sleep, a change in training or weight, and a delayed ovulation pushes the period back with it. A gap of a few days between projection and reality is ordinary rather than a sign that something is wrong.'),
        ('How many cycles should I track before the estimates get better?',
         'Three gives a rough average; six or more gives something reasonably stable and, more usefully, shows how much your cycles vary. That spread matters as much as the average &mdash; a projection built on cycles ranging across three days is far firmer than one built on cycles ranging across twelve.'),
        ('Can I ovulate without having a period, or have a period without ovulating?',
         'Both happen. Ovulation can return before the first period after childbirth or after coming off hormonal contraception, which is why the first cycle is often only visible in hindsight. Cycles without ovulation also occur &mdash; commonly in the years after a first period and in the years approaching menopause &mdash; and can still involve bleeding.'),
        ('Does the calculator work if I am on the pill or have an IUD?',
         'Generally no. Most hormonal methods suppress or override the natural cycle, and bleeding on combined pills is a withdrawal bleed during the hormone-free interval rather than a period that follows ovulation. The ovulation and fertile window estimates are not meaningful while you are using these methods.'),
        ('What does it mean if my cycle length changes?',
         'Usually very little on its own. Cycle length responds to stress, sleep, illness, travel, training load and weight change, and a one-off shift is common. A change that persists across several cycles without an obvious explanation, or one accompanied by other changes, is worth raising with a clinician &mdash; not because it is likely to be serious, but because it is the kind of thing that is easy to assess and reassuring to have checked.'),
        ('Is my cycle data private?',
         'Yes. Every calculation on this site runs in your browser in JavaScript. The dates you enter are never transmitted to a server, never stored in an account and never logged. Close the tab and nothing remains beyond an optional unit preference on your own device.'),
    ],
)

# ==========================================================================
# Pregnancy
# ==========================================================================
GUIDES_WOMENS['pregnancy'] = guide(
    intro='''
<p>A due date is one of the first pieces of information anyone receives in pregnancy, and it is almost always treated as more precise than it is. It is an estimate: the centre of a range of likely birth dates, calculated from a convention that starts counting about two weeks before conception.</p>
<p>This guide explains what pregnancy term means, how the different dating methods compare, what the standard timeline looks like, and the general considerations around managing a pregnancy &mdash; medication, weight, activity and nutrition. Throughout, it stays general: your own care belongs with the midwife, obstetrician or doctor who knows your history.</p>
''',
    sections=[
        ('term-and-due-date', 'Pregnancy term and the due date', '''
<p>Human pregnancy is conventionally counted as <strong>280 days, or 40 weeks, from the first day of the last menstrual period</strong>. Because ovulation typically follows about two weeks later, actual gestation from conception averages nearer 38 weeks. Both numbers describe the same pregnancy; they simply start counting at different points.</p>
<p>The estimated due date is the midpoint of a distribution, not an appointment. Only a small minority of babies &mdash; commonly cited as around 4% &mdash; arrive on the estimated date itself, while the large majority arrive within roughly two weeks either side of it.</p>
<h3>The term bands</h3>
<p>Obstetric practice divides the end of pregnancy into bands, introduced because outcomes at 37 weeks are measurably different from those at 39.</p>
''' + ref_table(
    'Gestational age bands at the end of pregnancy',
    [('Band', False), ('Gestational age', False)],
    [
        ('Preterm', 'Before 37 weeks 0 days'),
        ('Early term', '37 weeks 0 days to 38 weeks 6 days'),
        ('Full term', '39 weeks 0 days to 40 weeks 6 days'),
        ('Late term', '41 weeks 0 days to 41 weeks 6 days'),
        ('Post-term', '42 weeks 0 days and beyond'),
    ]) + '''
<h3>Why the date of birth varies</h3>
<p>Factors associated in research with variation in pregnancy length include the accuracy of the dating method itself, the length and regularity of your cycles, whether this is a first pregnancy, your own previous pregnancy lengths, carrying more than one baby, and a range of individual and clinical factors. Some of this variation is simply biological and is not explained by anything identifiable.</p>
'''),
        ('dating-methods', 'How due dates are calculated', '''
<p>Four methods are in common use, and they do not always agree.</p>
''' + ref_table(
    'Comparison of pregnancy dating methods',
    [('Method', False), ('How it works', False), ('Typical precision', False)],
    [
        ('Last menstrual period', 'Naegele&rsquo;s rule: 280 days from the first day of the LMP',
         'Weakest; depends on recall and on ovulation timing'),
        ('Conception date', '266 days from conception, where that date is known',
         'Good when the date is genuinely known'),
        ('IVF transfer date', 'Counted from a precisely known embryo age',
         'The most precise of the four'),
        ('First-trimester ultrasound', 'Crown-rump length measurement',
         'Within about five days when performed early'),
    ]) + '''
<h3>Why LMP dating is the default but not the best</h3>
<p>Naegele&rsquo;s rule works from a date most people can actually recall, which is its whole advantage. Its weakness is that it assumes a 28-day cycle with ovulation on day 14. On a 35-day cycle, ovulation happens closer to day 21, so the pregnancy is about a week younger than the LMP implies and the due date moves later &mdash; which is what the cycle-length adjustment in this calculator corrects for.</p>
<h3>Ultrasound dating takes precedence</h3>
<p>A first-trimester scan measuring crown-rump length dates a pregnancy to within about five days, because early embryonic growth is highly consistent between pregnancies. Standard practice is to re-date the pregnancy if the scan differs from the LMP estimate by more than roughly five to seven days in the first trimester. Later scans are less precise for dating, because growth diverges more between babies as pregnancy progresses.</p>
''' + callout('<p><strong>Your clinician&rsquo;s date is the one that counts.</strong> If a midwife or doctor has given you a due date, use theirs. It is based on measurements this calculator does not have, and it is the date your whole care plan &mdash; screening windows, scan timing, monitoring &mdash; will be built around.</p>')),
        ('pregnancy-detection', 'How pregnancy is detected', '''
<p>General information about how pregnancy is identified. This page cannot tell you whether you are pregnant, and no symptom list can.</p>
<h3>Home pregnancy tests</h3>
<p>Home tests detect human chorionic gonadotropin (hCG) in urine, a hormone produced after a fertilised egg implants in the uterine lining. Implantation typically occurs somewhere around six to twelve days after ovulation, and hCG then rises quickly in early pregnancy.</p>
<p>Because of that timing, tests taken very early can return a negative result even in an established pregnancy. Most manufacturers advise testing from the day of a missed period, and testing again a few days later if the result is negative but a period has not arrived. First-morning urine is more concentrated and generally gives the clearest result. Follow the instructions supplied with your own test, including its stated reading window.</p>
<h3>Blood tests</h3>
<p>A blood test performed by a healthcare provider can detect hCG earlier than a urine test, and a quantitative test measures the actual concentration. Repeated measurements are sometimes used clinically to observe how the level is changing.</p>
<h3>Ultrasound</h3>
<p>An early scan can confirm a pregnancy, establish its location and, from around six weeks, detect cardiac activity. It is also the most accurate way to date the pregnancy.</p>
<h3>Early signs</h3>
<p>Commonly reported early experiences include a missed period, breast tenderness, fatigue, nausea, changes in appetite or smell, and more frequent urination. These are reported often enough to be worth knowing about and are far too non-specific to confirm anything &mdash; each of them has many other explanations, and plenty of pregnancies involve none of them early on. A test, and then a clinician, is how pregnancy is confirmed.</p>
'''),
        ('pregnancy-timeline', 'The pregnancy timeline', '''
<p>A general outline of how pregnancy is usually structured. Exact timing of appointments and screening varies by country and by local service.</p>
''' + ref_table(
    'Typical milestones by gestational age',
    [('Gestational age', False), ('What typically happens', False)],
    [
        ('4&ndash;5 weeks', 'A missed period; home tests usually become reliable'),
        ('6&ndash;8 weeks', 'First contact with maternity care in many systems; early scan in some'),
        ('8&ndash;13 weeks', 'Booking appointment; dating scan and first-trimester screening'),
        ('13 weeks', 'End of the first trimester'),
        ('18&ndash;22 weeks', 'Detailed anatomy scan'),
        ('20&ndash;24 weeks', 'Movements usually become noticeable'),
        ('27&ndash;28 weeks', 'Start of the third trimester; further blood tests in many systems'),
        ('36&ndash;40 weeks', 'More frequent appointments; position and growth monitored'),
        ('37 weeks onward', 'Considered early term; birth may occur at any point from here'),
    ]) + '''
<p>The calculator above shows these milestones against your own estimated dates. Treat them as a general map: your care team sets the actual schedule, and it varies with your history and with local guidelines.</p>
'''),
        ('pregnancy-management', 'General considerations during pregnancy', '''
<p>The four areas below come up in almost every pregnancy. Everything here is general educational information. None of it is advice for your pregnancy, and all of it should be discussed with your own midwife, obstetrician or doctor.</p>
<h3>Medication</h3>
<p>Medicines, supplements and herbal products can behave differently in pregnancy, and the evidence about their use varies from well established to very limited. Two points are worth carrying:</p>
<ul>
  <li><strong>Check before starting anything new</strong>, including over-the-counter medicines and supplements. A pharmacist, midwife or doctor can tell you what is known about a specific product.</li>
  <li><strong>Do not stop a prescribed medication on your own.</strong> Untreated conditions carry their own risks, and stopping abruptly can be worse than continuing. Many long-term medications are continued in pregnancy, sometimes with adjustments. That decision belongs with the prescriber.</li>
</ul>
<h3>Weight gain</h3>
<p>Weight gain in pregnancy is expected and healthy. It reflects the baby, placenta, amniotic fluid, increased blood volume, breast tissue and maternal stores &mdash; not simply body fat.</p>
<p>How much gain is appropriate differs between individuals, and the most widely used guidance bases it on pre-pregnancy BMI. The ranges below come from the 2009 Institute of Medicine guidelines for singleton pregnancies, which are referenced internationally:</p>
''' + ref_table(
    'IOM 2009 total weight-gain ranges, singleton pregnancy',
    [('Pre-pregnancy BMI', False), ('Recommended total gain', True)],
    [
        ('Under 18.5', '12.5&ndash;18 kg (28&ndash;40 lb)'),
        ('18.5&ndash;24.9', '11.5&ndash;16 kg (25&ndash;35 lb)'),
        ('25.0&ndash;29.9', '7&ndash;11.5 kg (15&ndash;25 lb)'),
        ('30.0 and over', '5&ndash;9 kg (11&ndash;20 lb)'),
    ]) + '''
<p>Pre-pregnancy BMI is what these bands are read against &mdash; the <a href="../bmi/index.html">BMI calculator</a> covers how that figure is worked out and what it does not capture. A BMI calculated during pregnancy is not meaningful.</p>
<p>These are population-level recommendations, not targets to manage yourself against. Ranges differ for twins and multiples, and your care team may advise something different for good reason. Weight loss dieting is generally not recommended during pregnancy.</p>
<h3>Exercise</h3>
<p>For most people with an uncomplicated pregnancy, staying physically active is encouraged. Guidance from bodies including the American College of Obstetricians and Gynecologists supports around 150 minutes of moderate-intensity activity per week during pregnancy in the absence of contraindications.</p>
<p>What differs is the individual picture. Some medical and obstetric conditions change what is appropriate, and activities carrying a risk of falls, abdominal impact, overheating or scuba diving are generally advised against. Comfort, balance and breathlessness all change as pregnancy progresses, so what works in the first trimester may need adapting later. Confirm with your care team what suits your situation, particularly if you are starting something new or training at a high level.</p>
<h3>Nutrition</h3>
<p>Nutritional needs rise modestly in pregnancy &mdash; much less than the &ldquo;eating for two&rdquo; phrase suggests &mdash; while requirements for certain micronutrients rise sharply. General considerations that appear consistently in national guidance:</p>
<ul>
  <li><strong>Folic acid</strong> before conception and through early pregnancy, to reduce the risk of neural tube defects. A commonly recommended dose is 400 micrograms daily, with higher doses advised for some people. Your clinician will tell you which applies.</li>
  <li><strong>Iron</strong>, since requirements rise substantially and iron deficiency is common in pregnancy.</li>
  <li><strong>Calcium and vitamin D</strong>, with supplementation recommended in many countries.</li>
  <li><strong>Iodine and omega-3 fatty acids</strong>, both associated with fetal development.</li>
  <li><strong>Food safety.</strong> National guidance commonly advises avoiding unpasteurised dairy, undercooked meat and eggs, certain soft cheeses and pat&eacute;s, and high-mercury fish, and advises limiting caffeine.</li>
  <li><strong>Alcohol.</strong> Guidance in most countries is that no amount is known to be safe in pregnancy.</li>
</ul>
<p>Specific recommendations vary between countries and between individuals. Ask your midwife, doctor or a registered dietitian what applies to you, rather than assembling a plan from general information.</p>
'''),
        ('factors-affecting-dates', 'Factors that affect pregnancy dates', '''
<p>Why your estimated date may move, or may not match what actually happens:</p>
<ul>
  <li><strong>Cycle length.</strong> The 280-day rule assumes ovulation on day 14. Longer or shorter cycles shift the true date by up to a week in either direction.</li>
  <li><strong>Irregular cycles.</strong> If ovulation timing varies substantially, LMP dating carries correspondingly more uncertainty.</li>
  <li><strong>Recall.</strong> LMP dating depends entirely on remembering a date accurately, which is a larger source of error than most people expect.</li>
  <li><strong>Recent hormonal contraception.</strong> Cycles immediately after stopping can be atypical, which weakens LMP-based dating.</li>
  <li><strong>Ultrasound re-dating.</strong> If an early scan differs from the LMP estimate by more than roughly five to seven days, the scan date is normally adopted.</li>
  <li><strong>Previous pregnancies.</strong> First pregnancies tend on average to run slightly longer, and your own previous pregnancy lengths carry some information about later ones.</li>
  <li><strong>Multiple pregnancy.</strong> Twins and higher-order pregnancies are typically born earlier, and are dated and monitored differently.</li>
  <li><strong>Clinical factors.</strong> A range of maternal and pregnancy-related conditions influence timing, which is part of why individual care matters more than any calculation.</li>
</ul>
'''),
    ],
    limits='''
<ul>
  <li><strong>The due date is an estimate, not a prediction.</strong> Only around 4% of births occur on the estimated date, and most fall within about two weeks either side.</li>
  <li><strong>Different methods give different answers.</strong> LMP, conception date and ultrasound dating can disagree by a week or more, and ultrasound is the more reliable of them in the first trimester.</li>
  <li><strong>LMP dating assumes a 28-day cycle</strong> with ovulation on day 14, which is not true for many people even with the cycle-length adjustment applied.</li>
  <li><strong>The calculator cannot confirm or detect a pregnancy</strong>, assess how it is progressing, or identify any complication.</li>
  <li><strong>It does not account for multiple pregnancies</strong> or for any medical or obstetric factor affecting timing.</li>
  <li><strong>It is no substitute for clinical assessment.</strong> Scans, examinations and your medical history all carry information no calculator has access to.</li>
</ul>
''',
    seek_title='When to speak with a healthcare professional',
    seek='''
<p>Pregnancy care is built around regular professional contact, and the sections below are general orientation rather than a substitute for it.</p>
<p><strong>Arrange care early.</strong> If you have a positive pregnancy test, contact a midwife, GP or maternity service. Early contact is how dating scans, screening and any needed support get organised in good time.</p>
<p><strong>Ask sooner rather than later if:</strong></p>
<ul>
  <li>You are unsure of your dates, or the dates you have been given do not match what you expected.</li>
  <li>You take regular medication, or are considering starting or stopping anything.</li>
  <li>You have an existing health condition, or a history of pregnancy complications.</li>
  <li>You have questions about activity, work, travel or nutrition in your particular situation.</li>
  <li>You are pregnant with more than one baby.</li>
</ul>
<p><strong>Seek prompt medical attention for anything acute.</strong> Bleeding, abdominal pain, severe or persistent headache, visual changes, sudden swelling, fever, fluid loss, or a change in your baby&rsquo;s movements are all reasons to contact your maternity service straight away rather than waiting for a scheduled appointment. Trust your own sense that something is different &mdash; maternity services expect and want these calls.</p>
''',
    disclaimer='''
<p><strong>This calculator is for general information and education.</strong> It estimates dates arithmetically and does not provide medical advice, diagnosis or treatment. It cannot confirm a pregnancy, assess how one is progressing, or replace clinical assessment, and the information on this page is general rather than advice about your pregnancy. Always follow the guidance of your midwife, obstetrician or doctor, and use the due date they give you in preference to this one. If you have any urgent concern, contact your maternity service or local emergency number without delay.</p>
''',
    faqs=[
        ('How accurate is a due date calculator?',
         'As an estimate of a range, quite useful; as a prediction of a day, not at all. Around 4% of babies arrive on the estimated date and roughly 80% within two weeks either side. An early ultrasound narrows the range considerably, while dating from the last menstrual period alone is the least precise of the common methods.'),
        ('Which is more accurate, my dates or the ultrasound?',
         'The ultrasound, if it was performed in the first trimester. Early embryonic growth is highly consistent between pregnancies, so a crown-rump length measurement dates a pregnancy to within about five days. Standard practice is to re-date the pregnancy if a first-trimester scan differs from the LMP estimate by more than roughly five to seven days.'),
        ('Can I work out my due date without knowing my last period?',
         'Yes, in two ways. If you know roughly when conception occurred, switch the calculator to conception dating. Otherwise an ultrasound is the reliable route &mdash; a first-trimester scan can date a pregnancy from measurements alone, without needing any remembered dates.'),
        ('Why am I counted as pregnant before conception happened?',
         'Because gestational age is counted from the first day of your last period rather than from conception, which places roughly two weeks of the count before you conceived. It is a convention rather than an error, and it is the same convention your clinician and every scan report will use &mdash; keeping to it avoids a great deal of confusion later.'),
        ('What does full term actually mean?',
         'Obstetric practice divides the end of pregnancy into bands: early term is 37 weeks 0 days to 38 weeks 6 days, full term is 39 weeks 0 days to 40 weeks 6 days, late term is 41 weeks, and post-term is 42 weeks and beyond. The distinction was introduced because outcomes at 37 weeks differ measurably from those at 39.'),
        ('How much weight should I gain during pregnancy?',
         'It depends on your pre-pregnancy BMI and your individual circumstances, and it is genuinely a question for your care team rather than a calculator. The widely referenced 2009 Institute of Medicine ranges run from about 5 to 9 kg for a pre-pregnancy BMI of 30 or over, up to about 12.5 to 18 kg for a BMI under 18.5, for a single baby. Ranges differ for twins.'),
        ('Is it safe to exercise while pregnant?',
         'For most people with an uncomplicated pregnancy, staying active is encouraged, and guidance from bodies including ACOG supports around 150 minutes of moderate activity per week in the absence of contraindications. What differs is the individual picture: some conditions change what is appropriate, and activities with a risk of falls, abdominal impact or overheating are generally advised against. Confirm with your own care team.'),
        ('Can a due date change during pregnancy?',
         'Yes, most often after an early scan re-dates the pregnancy. Once a due date has been established in the first trimester it is not usually revised again, because later scans estimate size rather than age and babies grow at increasingly different rates as pregnancy progresses.'),
    ],
)

# ==========================================================================
# Bra size
# ==========================================================================
GUIDES_WOMENS['bra-size'] = guide(
    intro='''
<p>Bra sizing has a reputation for being mysterious, and most of that reputation is earned. The labels combine two independent measurements, the letters mean different things in different countries, and no standard governs how any brand cuts a given size.</p>
<p>The underlying system, though, is simpler than it looks. This guide explains what the band and cup actually represent, how to measure yourself properly, how the international systems line up, why the same size fits differently between brands, and how to judge fit once a bra is on.</p>
''',
    sections=[
        ('how-sizing-works', 'How bra sizing works', '''
<p>A bra size such as 34D is two separate pieces of information.</p>
<ul>
  <li><strong>The number is the band</strong> &mdash; derived from your underbust measurement, the ribcage circumference directly beneath the bust.</li>
  <li><strong>The letter is the cup</strong> &mdash; derived from the <em>difference</em> between your bust measurement and your band.</li>
</ul>
<p>The consequence that surprises most people is that a cup letter is not an absolute volume. It is a difference, so it only means something relative to the band it sits on. A 30D and a 40D are both &ldquo;a D cup&rdquo; and hold noticeably different volumes, because the same four-inch difference is measured around very different ribcages.</p>
''' + callout('<p><strong>This is why cup letters travel badly.</strong> Saying &ldquo;I am a D cup&rdquo; conveys much less than it appears to. The band it sits on, and the country whose lettering is being used, both change what it means.</p>')),
        ('band-size', 'The band', '''
<p>The band does the work. It should carry roughly <strong>80% of the support</strong>, with the straps contributing the remainder. This is the single most useful fact in bra fitting, and it explains most common fit complaints.</p>
<p>A band that is too loose cannot support anything, so the load transfers to the straps &mdash; which is why shoulder grooves and neck ache are usually a band problem rather than a strap problem. A loose band also rides up at the back, which tilts the cups and changes how everything sits at the front.</p>
<h3>The &ldquo;add four inches&rdquo; problem</h3>
<p>Older fitting practice added four or five inches to the underbust measurement to arrive at a band size. That convention dates from an era of far less elastic fabrics, and modern materials do not need it. It is still widely repeated, and it reliably produces bands that are too large &mdash; which then pushes people into cups that are too small, since a larger band with the same bust measurement yields a smaller cup difference. Someone measuring 33 inches under the bust and 40 inches around it lands on a 38B under the old rule and a 34E under the modern one &mdash; same body, four band sizes and three cup letters apart.</p>
<h3>How a band should feel</h3>
<p>Snug and level all the way around, sitting horizontally rather than riding up at the back. On a new bra it should fit on the loosest hook, so there is room to tighten as the elastic relaxes over months of wear. You should be able to slide a couple of fingers under it, no more.</p>
'''),
        ('cup-size', 'The cup', '''
<p>The cup letter comes from the difference between your bust and band measurements. Working in inches, each full inch of difference is roughly one cup letter; working in centimetres, each 2 to 3 cm step is roughly one letter depending on the system.</p>
''' + ref_table(
    'Difference between bust and band, in inches, to UK / India cup letter',
    [('Difference', True), ('Cup', False), ('Difference', True), ('Cup', False)],
    [
        ('1&Prime;', 'A', '7&Prime;', 'F'),
        ('2&Prime;', 'B', '8&Prime;', 'FF'),
        ('3&Prime;', 'C', '9&Prime;', 'G'),
        ('4&Prime;', 'D', '10&Prime;', 'GG'),
        ('5&Prime;', 'DD', '11&Prime;', 'H'),
        ('6&Prime;', 'E', '12&Prime;', 'HH'),
    ]) + '''
<h3>Sister sizes</h3>
<p>Because cup volume depends on the band, you can hold volume roughly constant while changing the band &mdash; going down a band and up a cup letter, or the reverse. These are sister sizes: 36C, 34D and 32DD hold broadly similar cup volume on progressively tighter bands.</p>
<p>This is the first adjustment to try when a bra is close but not right:</p>
<ul>
  <li><strong>Cup fits, band rides up or feels loose:</strong> go down one band, up one cup. A 36C becomes a 34D.</li>
  <li><strong>Band fits, cup is tight or overflowing:</strong> stay on the band, go up one or two cups.</li>
  <li><strong>Band fits, cup gapes:</strong> stay on the band, go down a cup &mdash; or try a different style, since gaping is often a shape mismatch rather than a size error.</li>
</ul>
'''),
        ('measuring-yourself', 'Measuring yourself properly', '''
<p>Two measurements, taken carefully. The care matters more than the tape.</p>
<ol>
  <li><strong>Wear an unpadded bra, or nothing.</strong> A padded or moulded bra adds volume and will inflate the bust measurement.</li>
  <li><strong>Stand upright in front of a mirror.</strong> The mirror is for checking the tape is level at the back, which is where most errors happen.</li>
  <li><strong>Measure the underbust.</strong> Wrap the tape around your ribcage directly beneath the bust, snug and parallel to the floor. It should be firm &mdash; this measurement is taken tight, because the band is meant to be tight.</li>
  <li><strong>Measure the bust.</strong> Around the fullest part, with the tape level and loose enough not to compress the tissue at all.</li>
  <li><strong>Breathe normally.</strong> Take both readings at the end of a normal exhale, not while holding a deep breath.</li>
  <li><strong>Repeat each measurement</strong> and take the average. If two readings differ by more than about a centimetre, take a third.</li>
</ol>
''' + worked(
    'An underbust of <b>78 cm</b> is 30.7 inches, which rounds to a <b>band of 30</b>. A bust of '
    '<b>92 cm</b> is 36.2 inches, so the difference is just over <b>6 inches</b> &mdash; a UK <b>30E</b>. '
    'Its sister sizes, 28F and 32DD, are the next two worth trying if the first is close but not quite right.') + '''
<h3>Common measuring errors</h3>
<ul>
  <li><strong>The tape sloping down at the back</strong>, which inflates the measurement. This is by far the most common one.</li>
  <li><strong>Measuring the bust over a padded bra</strong>, which adds volume that is not yours.</li>
  <li><strong>Pulling the bust tape tight</strong>, which compresses tissue and understates the cup.</li>
  <li><strong>Measuring the underbust too loosely</strong>, which produces a band that will not support.</li>
  <li><strong>Measuring while leaning forward</strong>, which changes where the tissue sits.</li>
</ul>
<h3>When to measure</h3>
<p>Size changes more often than most people re-measure. Weight change, pregnancy and breastfeeding, hormonal cycles, ageing and hormonal contraception all affect band or cup or both. Re-measuring every six to twelve months, and after any significant change, is reasonable. Many people also find their measurements shift slightly across the menstrual cycle, so measuring at a consistent point gives more comparable readings &mdash; the <a href="../period/index.html">period calculator</a> is one way to keep track of where you are in yours. During and after a pregnancy, expect to re-measure several times; the <a href="../pregnancy/index.html">pregnancy calculator</a> covers that timeline.</p>
'''),
        ('sizing-systems', 'International sizing systems', '''
<p>Bands and cups are labelled differently by country, which is the second major source of sizing confusion after the band myth.</p>
<h3>Bands</h3>
''' + ref_table(
    'Approximate band size equivalents',
    [('UK / India / US', True), ('EU / JP (cm)', True), ('France / Spain', True), ('Australia / NZ', True)],
    [
        ('30', '65', '80', '8'),
        ('32', '70', '85', '10'),
        ('34', '75', '90', '12'),
        ('36', '80', '95', '14'),
        ('38', '85', '100', '16'),
        ('40', '90', '105', '18'),
    ]) + '''
<h3>Cups</h3>
<p>Up to a D cup, the systems broadly agree. Above it they diverge, and this is where a size that fits in one country becomes unfindable in another.</p>
''' + ref_table(
    'Approximate cup equivalents from a D cup upward',
    [('UK / India', False), ('United States', False), ('EU', False)],
    [
        ('D', 'D', 'D'),
        ('DD', 'DD', 'E'),
        ('E', 'DDD', 'F'),
        ('F', 'G', 'G'),
        ('FF', 'H', 'H'),
        ('G', 'I', 'I'),
        ('GG', 'J', 'J'),
        ('H', 'K', 'K'),
    ]) + '''
<p>So a UK 34F sits close to a US 34G and an EU 75G. US lettering is the least consistent of the three &mdash; some brands print F where this chart shows DDD, and some skip letters altogether &mdash; which is why the calculator shows all four systems side by side rather than picking one.</p>
'''),
        ('why-brands-differ', 'Why the same size fits differently between brands', '''
<p>There is no enforced standard for how much volume a cup holds or how tight a band runs. Each brand works from its own blocks and fit models, and the result is genuine variation between labels bearing the same number and letter.</p>
<p>What drives the differences:</p>
<ul>
  <li><strong>Different fit models.</strong> Brands develop patterns on a specific body, and yours is not that body.</li>
  <li><strong>Different shapes at the same volume.</strong> Cups vary in projection and in where the volume sits &mdash; fuller at the top, fuller at the bottom, more central. Two cups of identical volume can fit completely differently.</li>
  <li><strong>Materials and construction.</strong> Moulded, seamed, stretch lace and rigid fabrics behave differently at the same nominal size.</li>
  <li><strong>Style.</strong> Balconette, plunge, full-cup and sports constructions each suit different shapes, and a style mismatch reads as a size problem.</li>
  <li><strong>Drift over time.</strong> Brands revise patterns between seasons, so even the same style can change.</li>
</ul>
<p>The practical response is to treat a calculated size as a shortlist rather than an answer. Take the calculated size plus its two sister sizes into a fitting room and judge by how they actually sit.</p>
'''),
        ('fit-checklist', 'Judging the fit', '''
<p>Measurements narrow the search; fit is decided in front of a mirror. Put a bra on properly first &mdash; lean forward, settle the tissue fully into each cup, then stand and adjust. A surprising share of fit problems disappear at this step alone.</p>
<h3>What a good fit looks like</h3>
<ul>
  <li><strong>The band</strong> is level all the way around, firm, and fastens on the loosest hook when new.</li>
  <li><strong>The centre gore</strong> &mdash; the panel between the cups &mdash; sits flat against the breastbone rather than standing away from it.</li>
  <li><strong>Underwires</strong> sit on the ribcage, following the natural crease, not resting on breast tissue.</li>
  <li><strong>The cups</strong> contain everything smoothly, with no spilling at the top or sides and no gaping or wrinkling.</li>
  <li><strong>The straps</strong> stay put without digging in, and you can slide a finger beneath them.</li>
</ul>
<h3>What each common problem usually means</h3>
''' + ref_table(
    'Reading a poor fit',
    [('What you notice', False), ('Usual cause', False), ('What to try', False)],
    [
        ('Band rides up at the back', 'Band too loose', 'Down a band, up a cup'),
        ('Straps dig into the shoulders', 'Band not carrying the support', 'Down a band, up a cup'),
        ('Tissue spills over the top or sides', 'Cup too small', 'Up one or two cups, same band'),
        ('Cup gapes or wrinkles', 'Cup too large, or wrong shape', 'Down a cup, or a different style'),
        ('Centre gore stands away from the chest', 'Cup too small, or wrong wire width', 'Up a cup, or a different style'),
        ('Wire sits on breast tissue', 'Cup too small, or wire too narrow', 'Up a cup, or a different style'),
        ('Band digs in uncomfortably', 'Band too tight, or worn out and stiff', 'Up a band, down a cup'),
    ]) + '''
<h3>Care and replacement</h3>
<p>Elastic degrades with wear, and a band that no longer holds stops supporting long before the bra looks worn. Rotating between several bras rather than wearing one repeatedly lets the elastic recover between wears, and washing gently &mdash; by hand, or in a mesh bag on a cool cycle &mdash; extends their life considerably. Tumble drying is what kills elastic fastest. When a bra only fits on the tightest hook and still rides up, it has reached the end of its useful life.</p>
'''),
    ],
    limits='''
<ul>
  <li><strong>The result is a starting size, not a final answer.</strong> No calculation can account for breast shape, tissue firmness or how a particular style is cut.</li>
  <li><strong>There is no enforced sizing standard.</strong> The same labelled size varies between brands, between styles within a brand, and between seasons.</li>
  <li><strong>Measurement technique dominates the result.</strong> A tape that slopes at the back or a bust measured over padding changes the answer by a full size or more.</li>
  <li><strong>Cross-system conversions are approximate</strong>, particularly in US lettering, which is the least consistent of the common systems.</li>
  <li><strong>Sizing changes with your body.</strong> Weight change, pregnancy, breastfeeding, hormonal cycles and ageing all shift band or cup or both.</li>
  <li><strong>It does not cover specialist needs</strong> such as post-surgery, mastectomy, nursing or sports bras with their own sizing conventions, where a specialist fitter is genuinely worth seeking out.</li>
</ul>
''',
    seek_title='When to see a fitter or a doctor',
    seek='''
<h3>A professional fitting is worth it if</h3>
<ul>
  <li>Nothing you try fits well, or your measurements fall at the edges of standard size ranges.</li>
  <li>You are shopping for a specialist purpose &mdash; nursing, post-surgery, mastectomy or high-impact sports.</li>
  <li>Your size has changed substantially, for example after pregnancy or significant weight change.</li>
  <li>You want to work out which cup shapes suit you, which is difficult to judge from measurements alone.</li>
</ul>
<h3>Speak with a doctor if</h3>
<p>Fit is a clothing question; the following are not, and a calculator cannot assess any of them. It is worth contacting a healthcare professional if you notice:</p>
<ul>
  <li>Persistent breast pain, or pain that is not related to your cycle.</li>
  <li>A new lump, thickening or change in texture.</li>
  <li>Changes to the skin or nipple, including dimpling, puckering, rash or inversion.</li>
  <li>Discharge from the nipple, particularly if it is bloodstained or from one side only.</li>
  <li>A noticeable change in the size or shape of one breast.</li>
  <li>Neck, shoulder or back pain that persists despite a well-fitting bra.</li>
</ul>
<p>These are reasons to get checked rather than reasons to worry &mdash; most such changes turn out to be benign, and having them assessed is straightforward.</p>
''',
    disclaimer='''
<p><strong>This calculator is for general information and education.</strong> It converts tape measurements into a starting bra size and does not provide medical advice, diagnosis or treatment. Sizing varies between brands and styles, so treat the result as a shortlist to try rather than a definitive size. For any concern about breast health &mdash; including pain, lumps, skin or nipple changes, or discharge &mdash; contact a doctor or another qualified healthcare professional.</p>
''',
    faqs=[
        ('Why is my calculated size so different from what I usually wear?',
         'Most often because the old rule of adding four or five inches to the underbust measurement is still widely used, and it produces bands that are far too loose. A loose band shifts support to the straps and, because the cup is a difference from the band, simultaneously produces a cup that is too small. Moving from something like a 38B to a 34E is one of the most common corrections in professional fitting.'),
        ('Is a D cup the same size in every country?',
         'Up to a D cup the systems broadly agree. Above it they diverge: UK and Indian sizing uses doubled letters (DD, E, FF, GG), US sizing often runs DD then DDD before continuing with single letters, and EU sizing uses single letters throughout. A UK 34F is close to a US 34G and an EU 75G, which is why the calculator shows all four systems together.'),
        ('How tight should the band be?',
         'Firm. It should sit level all the way around, stay horizontal when you raise your arms, and fasten on the loosest hook when the bra is new, leaving room to tighten as the elastic relaxes. Two fingers should slide underneath without much slack. The band is meant to carry around 80% of the support, which it cannot do if it is loose.'),
        ('How often should bras be replaced?',
         'When the band no longer holds, which is usually the first thing to go. A practical test: if a bra only works on the tightest hook and still rides up at the back, its elastic is finished regardless of how it looks. Rotating between several bras and avoiding the tumble dryer both extend their working life considerably.'),
        ('Does bra size change during pregnancy or breastfeeding?',
         'Commonly and substantially, in both band and cup. The ribcage expands during pregnancy and breast volume changes through pregnancy and lactation, often more than once. Many people re-measure at several points and choose styles with more adjustment, and specialist maternity and nursing fitters are genuinely useful during this period.'),
        ('What if I am between two sizes?',
         'Try both, plus the sister sizes on either side. Because band and cup interact, being between sizes often means one combination works in a particular style while the other works elsewhere. Cup shape and construction matter as much as the number at this point, so judging by how each one actually sits beats reasoning it out on paper.'),
    ],
)
