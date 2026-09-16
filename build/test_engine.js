/* Reference-value tests for the VitaCalc calculation engine.
   Run:  node build/test_engine.js                                        */
'use strict';
const E = require('../assets/js/engine.js');

let pass = 0, fail = 0;
const results = [];

function ok(name, cond, detail) {
  if (cond) { pass++; results.push('  PASS  ' + name); }
  else { fail++; results.push('  FAIL  ' + name + (detail ? '  -> ' + detail : '')); }
}
function near(name, actual, expected, tol) {
  const d = Math.abs(actual - expected);
  ok(name, d <= tol, 'got ' + actual + ', expected ' + expected + ' +/- ' + tol);
}
function eq(name, actual, expected) {
  ok(name, actual === expected, 'got ' + JSON.stringify(actual) + ', expected ' + JSON.stringify(expected));
}

/* ----------------------------- conversions ----------------------------- */
near('lb -> kg (150 lb)', E.convert.lbToKg(150), 68.0389, 0.001);
near('kg -> lb (70 kg)', E.convert.kgToLb(70), 154.3236, 0.001);
near('ft/in -> cm (5 ft 9 in)', E.convert.ftInToCm(5, 9), 175.26, 0.001);
near('in -> cm (33 in)', E.convert.inToCm(33), 83.82, 0.001);
near('mi -> km (26.2188 mi)', E.convert.miToKm(26.2188), 42.1949, 0.001);
near('km -> mi (5 km)', E.convert.kmToMi(5), 3.10686, 0.0001);
eq('cm -> ft/in (175.26 cm) feet', E.convert.cmToFtIn(175.26).ft, 5);
near('cm -> ft/in (175.26 cm) inches', E.convert.cmToFtIn(175.26).inches, 9, 0.0001);

/* -------------------------------- BMI ---------------------------------- */
let r = E.calculateBmi({ weightKg: 70, heightCm: 175 });
near('BMI 70kg/175cm', r.bmi, 22.9, 0.05);
eq('BMI 70kg/175cm category', r.category.key, 'normal');
near('BMI healthy min at 175cm', r.healthyMinKg, 56.7, 0.1);
near('BMI healthy max at 175cm', r.healthyMaxKg, 76.3, 0.1);

r = E.calculateBmi({ weightKg: 100, heightCm: 175 });
near('BMI 100kg/175cm', r.bmi, 32.7, 0.05);
eq('BMI 100kg/175cm category', r.category.key, 'obese-1');

r = E.calculateBmi({ weightKg: 50, heightCm: 175 });
eq('BMI 50kg/175cm is underweight', r.category.key, 'underweight-mod');

/* boundary: exactly 25.0 must be "overweight", not "normal" */
r = E.calculateBmi({ weightKg: 25 * Math.pow(1.75, 2), heightCm: 175 });
eq('BMI boundary 25.0 -> overweight', r.category.key, 'overweight');
/* boundary: exactly 18.5 must be "normal" */
r = E.calculateBmi({ weightKg: 18.5 * Math.pow(1.75, 2), heightCm: 175 });
eq('BMI boundary 18.5 -> normal', r.category.key, 'normal');

/* imperial reference: 703 * lb / in^2 */
const lbIn = 703 * 150 / (69 * 69);
r = E.calculateBmi({ weightKg: E.convert.lbToKg(150), heightCm: E.convert.ftInToCm(5, 9) });
near('BMI imperial matches 703 formula', r.bmiRaw, lbIn, 0.01);

/* -------------------------------- BMR ---------------------------------- */
/* Mifflin-St Jeor, male 80kg/180cm/30y = 10*80+6.25*180-5*30+5 = 1780 */
r = E.calculateBmr({ sex: 'male', age: 30, heightCm: 180, weightKg: 80, formula: 'mifflin', activityKey: 'sedentary' });
eq('BMR Mifflin male 80/180/30', r.bmr, 1780);
eq('BMR TDEE sedentary x1.2', r.tdee, Math.round(1780 * 1.2));

/* Mifflin female 60kg/165cm/25y = 600+1031.25-125-161 = 1345.25 */
r = E.calculateBmr({ sex: 'female', age: 25, heightCm: 165, weightKg: 60, formula: 'mifflin', activityKey: 'moderate' });
eq('BMR Mifflin female 60/165/25', r.bmr, 1345);
eq('BMR TDEE moderate x1.55', r.tdee, Math.round(1345.25 * 1.55));
eq('BMR deficit 500 below TDEE', r.weightLoss, Math.round(1345.25 * 1.55) - 500);

/* Harris-Benedict male 80/180/30 = 88.362+1071.76+863.82-170.31 = 1853.632 */
r = E.calculateBmr({ sex: 'male', age: 30, heightCm: 180, weightKg: 80, formula: 'harris', activityKey: 'sedentary' });
eq('BMR Harris male 80/180/30', r.bmr, 1854);

/* Katch-McArdle: 80kg at 20% fat -> lean 64 -> 370 + 21.6*64 = 1752.4 */
r = E.calculateBmr({ sex: 'male', age: 30, heightCm: 180, weightKg: 80, formula: 'katch', bodyFatPct: 20, activityKey: 'sedentary' });
eq('BMR Katch 80kg @20% fat', r.bmr, 1752);
ok('BMR Katch without body fat returns null',
   E.calculateBmr({ sex: 'male', age: 30, heightCm: 180, weightKg: 80, formula: 'katch' }) === null);

/* ---------------------------- Ideal weight ----------------------------- */
/* Devine male at 5'10" = 50 + 2.3*10 = 73 kg */
r = E.calculateIdealWeight({ heightCm: E.convert.ftInToCm(5, 10), sex: 'male', formula: 'devine' });
near('Devine male 5ft10', r.idealKg, 73.0, 0.05);
/* Devine female at 5'4" = 45.5 + 2.3*4 = 54.7 kg */
r = E.calculateIdealWeight({ heightCm: E.convert.ftInToCm(5, 4), sex: 'female', formula: 'devine' });
near('Devine female 5ft4', r.idealKg, 54.7, 0.05);
/* Robinson male 5'10" = 52 + 1.9*10 = 71 */
r = E.calculateIdealWeight({ heightCm: E.convert.ftInToCm(5, 10), sex: 'male', formula: 'robinson' });
near('Robinson male 5ft10', r.idealKg, 71.0, 0.05);
/* Miller female 5'4" = 53.1 + 1.36*4 = 58.54 */
r = E.calculateIdealWeight({ heightCm: E.convert.ftInToCm(5, 4), sex: 'female', formula: 'miller' });
near('Miller female 5ft4', r.idealKg, 58.5, 0.05);
/* Hamwi male 5'10" = 48 + 2.7*10 = 75 */
r = E.calculateIdealWeight({ heightCm: E.convert.ftInToCm(5, 10), sex: 'male', formula: 'hamwi' });
near('Hamwi male 5ft10', r.idealKg, 75.0, 0.05);
eq('Ideal weight returns all four formulas', r.allFormulas.length, 4);
/* below 5 ft must not go negative */
r = E.calculateIdealWeight({ heightCm: 140, sex: 'female', formula: 'devine' });
ok('Ideal weight under 5ft stays at base', r.idealKg === 45.5, 'got ' + r.idealKg);

/* ------------------------------ Body fat -------------------------------- */
/* US Navy male: height 180, neck 38, waist 85 */
r = E.calculateBodyFat({ sex: 'male', heightCm: 180, neckCm: 38, waistCm: 85, weightKg: 80 });
ok('Navy male in plausible range', r.bodyFatPct > 14 && r.bodyFatPct < 20, 'got ' + r.bodyFatPct);
near('Navy male fat+lean = weight', r.fatMassKg + r.leanMassKg, 80, 0.15);
/* verify against the published equation directly */
const log10 = (v) => Math.log(v) / Math.LN10;
const expectMale = 495 / (1.0324 - 0.19077 * log10(85 - 38) + 0.15456 * log10(180)) - 450;
near('Navy male matches published formula', r.bodyFatPct, Math.round(expectMale * 10) / 10, 0.05);

/* US Navy female: height 165, neck 32, waist 72, hip 96 */
r = E.calculateBodyFat({ sex: 'female', heightCm: 165, neckCm: 32, waistCm: 72, hipCm: 96, weightKg: 60 });
const expectFemale = 495 / (1.29579 - 0.35004 * log10(72 + 96 - 32) + 0.22100 * log10(165)) - 450;
near('Navy female matches published formula', r.bodyFatPct, Math.round(expectFemale * 10) / 10, 0.05);
ok('Navy female category assigned', !!r.category.key);

/* impossible input must be rejected, not returned as a number */
r = E.calculateBodyFat({ sex: 'male', heightCm: 180, neckCm: 40, waistCm: 38 });
ok('Navy rejects waist <= neck', !!r.error, JSON.stringify(r));

/* --------------------------- Calories burned ---------------------------- */
/* 8 MET, 70 kg, 30 min -> 8*3.5*70/200 = 9.8 kcal/min -> 294 kcal */
r = E.calculateCaloriesBurned({ met: 8, weightKg: 70, minutes: 30 });
eq('MET 8 / 70kg / 30min total', r.total, 294);
near('MET 8 / 70kg per minute', r.perMinute, 9.8, 0.01);
eq('MET 8 / 70kg per hour', r.perHour, 588);
eq('MET-minutes 8x30', r.metMinutes, 240);
/* scales linearly with weight */
const light = E.calculateCaloriesBurned({ met: 8, weightKg: 35, minutes: 30 });
near('Calorie burn scales with weight', light.total * 2, r.total, 1);

/* ------------------------------- Pace ----------------------------------- */
/* 10 km in 50:00 -> 5:00 /km */
r = E.calculatePace({ solveFor: 'pace', distanceKm: 10, timeSeconds: 50 * 60 });
eq('Pace 10km/50min', E.formatDuration(r.paceSecPerKm), '5:00');
eq('Speed 10km/50min', r.speedKmh, 12);
eq('Pace per mile at 5:00/km', E.formatDuration(r.paceSecPerMi), '8:03');
/* marathon split at 5:00/km = 42.195 * 300 s = 12658.5 s = 3:30:59 (rounded) */
const marathon = r.splits.filter((s) => s.label === 'Marathon')[0];
eq('Marathon split at 5:00/km', E.formatDuration(marathon.seconds), '3:30:59');

/* solve for time: 21.0975 km at 5:30/km */
r = E.calculatePace({ solveFor: 'time', distanceKm: 21.0975, paceSecPerKm: 330 });
eq('Half marathon at 5:30/km', E.formatDuration(r.timeSeconds), '1:56:02');

/* solve for distance: 1 hour at 6:00/km = 10 km */
r = E.calculatePace({ solveFor: 'distance', timeSeconds: 3600, paceSecPerKm: 360 });
near('Distance in 1h at 6:00/km', r.distanceKm, 10, 0.0001);

eq('hmsToSeconds 1:02:03', E.hmsToSeconds(1, 2, 3), 3723);
eq('formatDuration 3723', E.formatDuration(3723), '1:02:03');
eq('formatDuration 59', E.formatDuration(59), '0:59');

/* ------------------------------- Dates ---------------------------------- */
ok('parseISODate rejects 2025-02-30', E.parseISODate('2025-02-30') === null);
ok('parseISODate accepts leap day 2024-02-29', E.parseISODate('2024-02-29') !== null);
ok('parseISODate rejects non-leap 2025-02-29', E.parseISODate('2025-02-29') === null);
ok('parseISODate rejects junk', E.parseISODate('not-a-date') === null);
eq('addDays crosses leap day', E.toISO(E.addDays(E.parseISODate('2024-02-28'), 2)), '2024-03-01');
eq('addDays crosses non-leap Feb', E.toISO(E.addDays(E.parseISODate('2025-02-28'), 2)), '2025-03-02');
eq('addDays crosses year boundary', E.toISO(E.addDays(E.parseISODate('2025-12-30'), 5)), '2026-01-04');
eq('daysBetween across leap year', E.daysBetween(E.parseISODate('2024-01-01'), E.parseISODate('2025-01-01')), 366);
eq('daysBetween across normal year', E.daysBetween(E.parseISODate('2025-01-01'), E.parseISODate('2026-01-01')), 365);

/* ------------------------------- Period --------------------------------- */
r = E.calculatePeriod({ lmp: E.parseISODate('2026-09-01'), cycleLength: 28, periodLength: 5, cycles: 6 });
eq('Next period after 2026-09-01 + 28d', E.toISO(r.next.periodStart), '2026-09-29');
eq('Period window end (5 days)', E.toISO(r.next.periodEnd), '2026-10-03');
eq('Ovulation = next period - 14', E.toISO(r.next.ovulation), '2026-09-15');
eq('Fertile window opens 5 days before ovulation', E.toISO(r.next.fertileStart), '2026-09-10');
eq('Fertile window closes 1 day after ovulation', E.toISO(r.next.fertileEnd), '2026-09-16');
eq('Six cycles projected', r.cycles.length, 6);
eq('Sixth cycle start (LMP + 6 x 28d)', E.toISO(r.cycles[5].periodStart), '2027-02-16');

/* long cycle moves ovulation later, not to day 14 */
r = E.calculatePeriod({ lmp: E.parseISODate('2026-09-01'), cycleLength: 35, periodLength: 5, cycles: 2 });
eq('35-day cycle next period', E.toISO(r.next.periodStart), '2026-10-06');
eq('35-day cycle ovulation is day 21', E.toISO(r.next.ovulation), '2026-09-22');

/* ------------------------------ Pregnancy -------------------------------- */
r = E.calculatePregnancy({ method: 'lmp', date: E.parseISODate('2026-01-01'), cycleLength: 28 });
eq('EDD = LMP + 280 days', E.toISO(r.edd), '2026-10-08');
eq('Conception estimate = LMP + 14', E.toISO(r.conception), '2026-01-15');
eq('Full term begins at day 259', E.toISO(r.termStart), '2026-09-17');

/* 35-day cycle pushes the due date 7 days later */
r = E.calculatePregnancy({ method: 'lmp', date: E.parseISODate('2026-01-01'), cycleLength: 35 });
eq('EDD with 35-day cycle', E.toISO(r.edd), '2026-10-15');

/* from a known due date, the LMP works backwards */
r = E.calculatePregnancy({ method: 'dueDate', date: E.parseISODate('2026-10-08') });
eq('Due date mode recovers LMP', E.toISO(r.lmp), '2026-01-01');
eq('Due date mode keeps the EDD', E.toISO(r.edd), '2026-10-08');

/* from conception on a 28-day cycle: LMP = conception - 14 */
r = E.calculatePregnancy({ method: 'conception', date: E.parseISODate('2026-01-15'), cycleLength: 28 });
eq('Conception mode recovers LMP', E.toISO(r.lmp), '2026-01-01');
eq('Conception mode EDD', E.toISO(r.edd), '2026-10-08');

/* leap-year pregnancy spanning 29 Feb */
r = E.calculatePregnancy({ method: 'lmp', date: E.parseISODate('2023-08-01'), cycleLength: 28 });
eq('EDD across leap day 2024', E.toISO(r.edd), '2024-05-07');

/* milestone count and ordering */
ok('Milestones are in ascending date order',
   r.milestones.every((m, i, a) => i === 0 || a[i - 1].date <= m.date));

/* ------------------------------ Bra size --------------------------------- */
/* underbust 78 cm (30.7 in -> band 30), bust 92 cm (36.2 in) -> diff 6.2 -> ~6 steps */
r = E.calculateBraSize({ underbustCm: 78, bustCm: 92, region: 'uk' });
eq('UK band from 78 cm underbust', r.band, '30');
ok('UK cup letter assigned', typeof r.cup === 'string' && r.cup.length > 0);
eq('All four systems returned', r.allRegions.length, 4);
eq('Two sister sizes returned', r.sisterSizes.length, 2);

/* one-inch difference = A cup */
r = E.calculateBraSize({ underbustCm: E.convert.inToCm(34), bustCm: E.convert.inToCm(35), region: 'uk' });
eq('34 in band / 1 in difference = 34A', r.size, '34A');
r = E.calculateBraSize({ underbustCm: E.convert.inToCm(34), bustCm: E.convert.inToCm(38), region: 'uk' });
eq('34 in band / 4 in difference = 34D', r.size, '34D');
r = E.calculateBraSize({ underbustCm: E.convert.inToCm(34), bustCm: E.convert.inToCm(39), region: 'uk' });
eq('UK 5 in difference = DD', r.size, '34DD');
r = E.calculateBraSize({ underbustCm: E.convert.inToCm(34), bustCm: E.convert.inToCm(40), region: 'us' });
eq('US 6 in difference = DDD', r.size, '34DDD');
r = E.calculateBraSize({ underbustCm: E.convert.inToCm(34), bustCm: E.convert.inToCm(40), region: 'eu' });
eq('EU 6 in difference = F', r.cup, 'F');
/* EU band follows the standard conversion: UK 34 in -> EU 75 */
r = E.calculateBraSize({ underbustCm: E.convert.inToCm(34), bustCm: E.convert.inToCm(40), region: 'eu' });
eq('EU band for a 34 in underbust', r.band, '75');
/* every system must report the same cup step, only different letters */
r = E.calculateBraSize({ underbustCm: E.convert.inToCm(32), bustCm: E.convert.inToCm(38), region: 'uk' });
eq('UK 6 in difference = E', r.size, '32E');
eq('Same step in US letters', r.allRegions.filter((x) => x.key === 'us')[0].size, '32DDD');
eq('Same step in EU letters', r.allRegions.filter((x) => x.key === 'eu')[0].size, '70F');
eq('Sister size down a band, up a cup', r.sisterSizes[0].size, '30F');
eq('Sister size up a band, down a cup', r.sisterSizes[1].size, '34DD');
/* bust smaller than underbust must error */
r = E.calculateBraSize({ underbustCm: 90, bustCm: 85, region: 'uk' });
ok('Bra size rejects bust <= underbust', !!r.error);

/* ------------------------------- Report ---------------------------------- */
console.log(results.join('\n'));
console.log('\n' + pass + ' passed, ' + fail + ' failed, ' + (pass + fail) + ' total');
process.exit(fail ? 1 : 0);
