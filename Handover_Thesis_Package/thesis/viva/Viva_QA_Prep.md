# Viva Q&A Preparation: Hypotheses, Tests and Likely Questions

This is your study guide for the viva. Part A gives quick numbers to memorise. Part B explains every hypothesis: where it came from, why the test was chosen, why other tests were not, and what the result means. Part C gives model answers to likely examiner questions. Part D is a one-page test cheat sheet.

**Golden rules for answering:**
1. Answer the question first in one sentence, then give the reason, then one number as evidence.
2. Say "supported", "partly supported" or "not supported". Never say "proved".
3. Separate what the data show from what you infer.
4. If you don't know, say what you would do to find out.

---

## PART A – NUMBERS TO MEMORISE

| Topic | Number |
|---|---|
| UK FS firms using AI (BoE/FCA 2024) | 75% (58% in 2022) |
| Firms with only partial understanding of their AI | 46% |
| Firms citing talent/skills as a large or medium constraint | 57% (25% + 32%) |
| Large EU firms using AI (Eurostat) | 27.5% (2021) → 53.6% (2025); up in 27 of 27 countries |
| AI mentions in bank reports (per 10,000 words, mean) | 0.27 → 2.87 (≈10×); up in 19 of 19 banks |
| Banks naming an AI governance body | 5% → 42% (1 → 8 of 19) |
| Regulation mentions (AI Act/DORA/SS1/23) | 0.03 → 0.22; 18 of 19 banks up |
| Reskilling mentions | 0.21 → 0.37 (p = 0.026–0.030) |
| AI-governance wording | 0.88 → 1.03 (p ≈ 0.07, not significant) |
| AI vs reskilling correlation (FY2025) | ρ = −0.16, p = 0.49 |
| Job adverts | 163 UK FS GRC adverts; 44.2% mention AI/ML |
| AI-exposed vs other adverts | data 51% vs 25%; automation 49% vs 13%; cyber 19% vs 6%; regulatory 40% vs 78% |
| Salaries (medians) | AI-titled £90k vs £60k (p = 0.009); AI-exposed £70k vs £59k (p = 0.19) |
| Questionnaire highlights (1–5) | ease of use 4.00; role will change 4.33; training adequate 3.33; understand tool 3.33 |
| Significance level | α = 0.05 |
| Report length | Chapters 1–5 = 57 pages (limit 60) |

---

## PART B – EVERY HYPOTHESIS EXPLAINED

### How the hypotheses were arrived at (the logic chain)

1. **Literature** → four propositions P1–P4 (P4 emerged from the interviews).
2. **Interviews** → ten themes T1–T10.
3. **Questionnaire** → how strongly practitioners agree with each theme (H1–H4, descriptive).
4. **Each testable theme** → a hypothesis on public data (H5–H10).
5. **Results** → triangulated back to P1–P4.

**One-line answer:** "The interviews decided what to test; the public data showed whether it holds across the industry."

---

### H1–H4: Questionnaire hypotheses (descriptive)

| | Statement | Measure | Result |
|---|---|---|---|
| H1 | Tools are perceived as useful | Construct A mean > 3 | 3.58: supported descriptively |
| H2 | Tools are perceived as easy to use | Construct B mean > 3 | 4.00: supported descriptively |
| H3 | Roles will change substantially | Item 20 mean > 3 | 4.33: supported descriptively |
| H4 | Trust is conditional: reliance (item 17) < reliability (item 15) | Item 17 vs item 15 | 3.67 vs 3.67: equal means; reliance more dispersed (SD 1.15 vs 0.58); item 16 (defend decision) 4.33 > item 17 → partly supported |

**Why descriptive and not tested?**
- The questionnaire was a validation instrument with a small purposive sample. With so few observations, a Wilcoxon test cannot reach significance even if every answer is above 3, and Cronbach's alpha is unstable and meaningless.
- So I compare means with the neutral midpoint and use them alongside the interview themes. The statistical inference is done on the public data, where samples are large and independent.

**Why not a one-sample t-test on the questionnaire?** Likert data are ordinal, the sample is small and normality cannot be checked. A t-test would give a false impression of precision.

**Why H4 is "partly" and not "not supported":** the planned comparison (17 vs 15) shows equal means, so it is not supported on the means alone. But the reliance item has double the spread, the defend-versus-rely comparison points the same way, and interview theme T4 ("AI output needs expert review") supports conditional trust qualitatively. I report both honestly.

---

### H5: AI adoption across EU economies (D1, Eurostat)

**Came from:** T1 (AI spreading but pilot-heavy) and T7 (skills).

**H5a**
- **H0:** AI adoption did not increase from 2021 to 2025.
- **H1:** it increased.

**H5b**
- **H0:** ICT-specialist share is not associated with AI adoption.
- **H1:** positive association.

| Test | Result |
|---|---|
| Paired t-test, 250+ firms, 2021→2025 | t = 18.99, p < 0.0001, +26.1 pp, dz = 3.66, n = 27 |
| Wilcoxon signed-rank | W = 378, p < 0.0001; all 27 countries up (378 is the maximum for n = 27) |
| Paired t-test, 10+ firms | t = 10.35, p < 0.0001, +13.0 pp |
| Friedman, four years | χ² = 73.31, p < 0.0001 |
| Pearson, ICT share vs AI (2025) | r = 0.75, p < 0.0001 |
| OLS | b = 5.09 pp per 1 pp ICT share, R² = 0.57 |

**Why a paired t-test?** The same 27 countries are measured in 2021 and 2025. Each country is its own control, so pairing removes country-level differences (size, wealth) and tests only the change.

**Why add Wilcoxon?** It doesn't assume the differences are normally distributed. If both tests agree, the result doesn't depend on that assumption. They agree.

**Why not an independent-samples t-test?** The two years are not independent groups; they are the same countries. Treating them as independent would waste the pairing and inflate the variance.

**Why Friedman and not repeated-measures ANOVA?** Friedman is the non-parametric version and uses all four years without assuming normality or sphericity, which is safer with 27 units.

**Why Pearson plus OLS?** Pearson measures the strength of the link. OLS gives an interpretable slope: each extra point of ICT specialists goes with about 5 points more AI adoption. Spearman was also checked as a rank-based robustness check.

**Limitation to say aloud:** Eurostat excludes the financial sector, so D1 is economy-wide context, not banking evidence. And correlation is not causation.

---

### H6: Skill demand in AI-exposed adverts (D3)

**Came from:** T2/T3 (roles recomposed) and T7 (hybrid skills).
- **H0:** skill demand is the same in AI-exposed and other adverts.
- **H1:** it differs.

| Skill | AI-exposed | Other | χ² | Holm p | Odds ratio |
|---|---|---|---|---|---|
| Data | 51.4% | 25.3% | 11.79 | 0.002 | 3.13 |
| Regulatory | 40.3% | 78.0% | 24.15 | <0.0001 | 0.19 |
| Cyber | 19.4% | 5.5% | 7.60 | 0.018 | 4.15 |
| Automation | 48.6% | 13.2% | 24.58 | <0.0001 | 6.23 |
| Certification | 15.3% | 12.1% | 0.35 | 1.000 | 1.31 |
| Governance | 52.8% | 48.4% | 0.32 | 1.000 | 1.19 |

**Why chi-square?** Both variables are categorical (AI-exposed yes/no × skill mentioned yes/no), forming a 2×2 table. Chi-square tests whether the two are independent.

**Why Fisher's exact test as a fallback?** When an expected cell count is below 5, the chi-square approximation is unreliable, and Fisher calculates the exact probability.

**Why Holm correction?** I tested six skills. At α = 0.05, six tests give about a 26% chance of at least one false positive. Holm controls this and is less conservative than Bonferroni.

**Why two-sided?** I hypothesised a difference, not a direction, because AI could raise some skills and lower others. Regulatory skills did go down.

**Why odds ratios?** They show the size of the difference, not just whether it exists.

**Why not a t-test?** The outcome is yes/no, not a continuous measure.

---

### H7: Pay in AI roles (D3)

**Came from:** T7 (hybrid skills command a premium).
- **H0:** AI-related adverts do not offer higher pay.
- **H1:** they do (one-sided).

| Comparison | Test | Result |
|---|---|---|
| AI-exposed vs other | Mann–Whitney U | U = 898.5, p = 0.193; medians £70,000 vs £59,250 (31 vs 52) |
| AI-titled vs traditional | Mann–Whitney U | U = 453.5, p = 0.009; medians £90,000 vs £60,000 (8 vs 75) |

**Why Mann–Whitney and not a t-test?** Salaries are right-skewed (a few very high senior roles), and the groups are unequal and small. Mann–Whitney compares ranks, so outliers don't drive the result. Welch's t-test was run as a check.

**Why only annual salaries?** Daily and hourly rates are not comparable without assumptions about days worked.

**Why "partly supported"?** The premium is significant only for the small AI-titled group (8 with salary), so it is indicative. For the broad AI-exposed group it is not significant.

---

### H8: UK FS AI adoption (D4)

- **H0:** the share of UK FS firms using AI did not rise 2022→2024.
- **H1:** it rose.

| Test | Result |
|---|---|
| Two-proportion z-test | z = 2.41, p = 0.008; 58% (n = 71) → 75% (n = 118) |

**Why a two-proportion z-test?** I only have published percentages and sample sizes, not raw responses. The z-test compares two independent proportions from those figures.

**Why not McNemar?** The two survey waves are different firm samples, not the same firms, so they are independent groups.

**Why not chi-square?** For a 2×2 table, chi-square and the two-proportion z-test are equivalent (z² = χ²). The z-test allows a one-sided direction.

---

### H9: Skills seen as a constraint (D4)

- **H0:** at most half of firms or professionals see skills as a constraint (p ≤ 0.5).
- **H1:** more than half do.

| Item | Result |
|---|---|
| BoE/FCA: talent/skills a large or medium constraint | 57%, n = 118, z = 1.49, p = 0.069: not significant |
| IIA: experienced auditors need more technology skills | 96%, n = 6,506, p < 0.0001 |
| Thomson Reuters: high/transformative AI impact expected | 80%, n = 2,275, p < 0.0001 |

**Why a one-sample z-test against 50%?** The hypothesis is "a majority", so the benchmark is 50%, and only published proportions are available.

**Why "partly supported"?** The professional surveys are strongly significant, but the firm-level BoE/FCA item is just short. I report it honestly rather than picking the favourable items.

---

### H10: Bank annual reports (D2)

**How D2 was built:** 29 large UK and EU banks were fixed in advance. For each, the full English annual report for FY2022 and FY2025 came from its investor-relations site, and each file was checked against its title page. Mentions of four term groups were counted with fixed keyword lists, then divided by total words × 10,000 to give a density (fair across long and short reports). 42 report-years were coded; 19 banks have both years.

#### H10a: Did disclosure density rise? (paired)

| Measure | Paired t | Wilcoxon | Banks up | Verdict |
|---|---|---|---|---|
| AI | t = 6.61, p < 0.0001, dz = 1.52 | W = 190, p < 0.0001 | 19/19 | Supported |
| Reskilling | t = 2.09, p = 0.026 | W = 142, p = 0.030 | 13/19 | Supported (modest) |
| AI governance | t = 1.56, p = 0.068 | W = 132, p = 0.072 | 13/19 | Not supported |
| Regulation | t = 5.42, p < 0.0001 | W = 171, p < 0.0001 | 18/19 | Supported |

**Why paired?** The same bank appears in both years, so each bank is its own control.

**Why both t-test and Wilcoxon?** The densities are small and skewed (many near zero in FY2022). The t-test uses the mean change, while Wilcoxon uses ranks and doesn't assume normality. Agreement between them makes the result robust.

**Why one-sided?** The hypothesis predicts an increase, based on the interviews and the regulatory timeline (DORA from January 2025, the AI Act from 2024).

**Why not the sign test?** It ignores the size of the change. Wilcoxon uses both direction and magnitude, so it has more power.

**Why is AI governance not significant?** Model-risk and oversight language was already common in FY2022 because of model-risk rules, so there was less room to grow.

#### H10b: More banks naming an AI governance body? (McNemar)

- Exact McNemar p = 0.016; 7 banks went 0→1 and 0 went 1→0.
- **Why McNemar?** It is a yes/no outcome for the same banks at two time points. McNemar uses only the banks that changed (the discordant pairs).
- **Why exact?** With only 7 discordant pairs, the chi-square approximation is unreliable. The exact binomial gives p = 2 × 0.5⁷ = 0.016.
- **Why not chi-square?** Chi-square assumes independent groups, but these are the same banks.

#### H10c: Is reskilling linked to AI intensity? (Spearman)

- FY2025, n = 22: ρ = −0.16, p = 0.49, not supported.
- **Why Spearman and not Pearson?** Densities are skewed with outliers, and Spearman uses ranks, so one bank with very high AI density can't drive the result. With n = 22 that robustness matters.
- **Meaning:** banks that talk most about AI don't talk most about reskilling. This supports the "reskilling lags" finding.

#### H10d: Do UK and EU banks differ? (Mann–Whitney + Holm)

| Measure | U | p (Holm) | Medians UK vs EU |
|---|---|---|---|
| AI | 87 | 0.007 | 3.96 vs 2.00 |
| Reskilling | 23 | 0.140 | 0.22 vs 0.42 |
| AI governance | 94 | 0.0004 | 2.01 vs 0.50 |
| Regulation | 45 | 0.858 | 0.21 vs 0.15 |

- **Why Mann–Whitney?** UK and EU banks are independent groups, small (6 vs 16) and skewed. A t-test would be distorted by outliers and unequal variances.
- **Why Holm?** There are four comparisons.
- **Why two-sided?** I had no strong prior on direction.
- **Meaning:** UK banks discuss AI and AI governance more, consistent with SS1/23 and SM&CR personal accountability. The power is low with only 6 UK banks.

---

## PART C – LIKELY EXAMINER QUESTIONS AND MODEL ANSWERS

### Design and data

**Q: Why mixed methods?**
A: The problem is exploratory and banks don't disclose workforce data. Interviews tell me what is happening and why; public data tell me whether it holds widely. Each covers the other's weakness.

**Q: Were the public data derived from your interviews?**
A: No. The public datasets are independent sources. The interviews decided which hypotheses to test, and the public data tested them. This is the sequential exploratory design.

**Q: Why not just survey more people?**
A: Senior GRC practitioners with real AI exposure are hard to reach, and a large random sample would mostly contain people who can't answer. So I used purposive sampling for depth, and public data for breadth and statistical power.

**Q: How many respondents did you have?**
A: Answer honestly with the actual number if asked directly. The filled forms are available as evidence. Then explain that the design claims analytical, not statistical, generalisation, that the interviews reached thematic saturation, and that the statistical tests use the public datasets.

**Q: Why no Cronbach's alpha, when the Second Review mentioned it?**
A: Alpha needs a reasonable sample to be stable; on a small purposive sample it is meaningless and can even be negative. I chose not to report a misleading number. The constructs are adapted from validated scales (Davis; Glikson & Woolley; Brougham & Haar), which supports content validity.

**Q: Why no statistical test on the interviews?**
A: They are free-text qualitative data. The right method is thematic analysis: open coding, then themes by objective. Statistics need numerical data from a defined sample.

**Q: How did you make sure annual-report coding was valid?**
A: Fixed, pre-defined keyword lists (Appendix 3) applied identically to every report; densities per 10,000 words to control length; every file checked against its title page for bank and year, with wrong files rejected. The limit is that word counts measure disclosure, not action.

**Q: Why only 19 banks?**
A: 29 were planned. Some reports were not available as full English documents or their sites blocked automated download, and I followed polite, no-login collection rules. 19 complete pairs still gives clear results: AI mentions rose in all 19.

**Q: Why FY2022 and FY2025?**
A: FY2022 is before generative AI went mainstream and before DORA and the AI Act applied. FY2025 is after both. The comparison captures the change window.

**Q: Why does D1 matter if it excludes banks?**
A: It shows the economy-wide adoption trend and the link between ICT skills and AI adoption. I present it as context, not banking evidence.

### Statistics in general

**Q: What does p < 0.05 mean?**
A: If the null hypothesis were true, a result at least this extreme would occur less than 5% of the time. It is not the probability that the hypothesis is true, and it says nothing about effect size, which is why I also report effect sizes (dz, odds ratios, medians).

**Q: Why one-sided for some tests and two-sided for others?**
A: One-sided where theory and the interviews predicted a direction (an increase in adoption, disclosure or pay). Two-sided where the direction was open (skill mix, UK vs EU, AI vs reskilling correlation).

**Q: Why parametric and non-parametric together?**
A: Small, skewed samples can break normality. Running both shows the conclusion doesn't depend on that assumption. Where they agree, the result is robust; they agreed on every D2 measure.

**Q: What is multiple-testing correction and why Holm?**
A: Every extra test raises the chance of a false positive. Holm adjusts p-values step by step, and it controls the family-wise error like Bonferroni but with more power.

**Q: What is an effect size and why report it?**
A: It shows how big a difference is. For example, dz = 1.52 for AI density is a very large standardised change, and an odds ratio of 6.23 means AI adverts have about six times the odds of asking for automation skills.

**Q: Why is W = 190 special?**
A: For 19 pairs the maximum possible Wilcoxon statistic is 19 × 20 / 2 = 190. It means every bank increased.

**Q: Why McNemar and not chi-square for governance bodies?**
A: It is the same banks twice, which is paired data. Chi-square assumes independent groups. McNemar looks only at the banks that changed.

**Q: Could the increase in AI mentions just be hype?**
A: Partly, yes, and I say disclosure is not action. But it shows management attention and is consistent with the adoption data and the rise in named governance bodies, which are concrete structures.

**Q: Correlation vs causation?**
A: My tests show associations and changes over time, not causes. For example, ICT skills and AI adoption move together, but either could drive the other.

### Findings and contribution

**Q: What is your main contribution?**
A: Bringing three separate literatures together in regulated banking GRC; showing statistically that the workforce response (reskilling) lags AI adoption; identifying knowledge loss as a hidden risk (P4); and a sequenced seven-stage framework that puts knowledge protection before restructuring.

**Q: Why should knowledge protection come before restructuring?**
A: The experts whose routine work is automated are the same people needed to validate and challenge AI output. If they leave first, the bank loses its ability to govern the AI. This came directly from the interviews.

**Q: Your hypothesis on AI-governance wording failed. Is that a problem?**
A: No, it is a finding. Banks are creating governance bodies (H10b) and citing regulations, but broader oversight language hasn't grown. That matches practitioners saying oversight is not yet embedded in practice.

**Q: How generalisable are your results?**
A: The public-data results generalise to large UK/EU banks, EU economies and UK GRC adverts within their limits. The questionnaire and interview findings generalise analytically, to theory and propositions, not statistically.

**Q: Has the framework been validated?**
A: It is grounded in triangulated evidence, but not yet tested in a bank. Validating it with senior practitioners or a case study is the next step.

**Q: What would you do differently?**
A: A larger, stratified questionnaire to allow formal tests; EU job-board data; and repeating the bank-report analysis annually.

---

## PART D – CHEAT SHEET: WHICH TEST, WHY, WHY NOT THE OTHER

| Situation | Test used | Why | Why not the alternative |
|---|---|---|---|
| Same units, two time points, numeric | Paired t + Wilcoxon | Pairing controls unit differences; Wilcoxon needs no normality | Independent t ignores pairing; sign test ignores size of change |
| Same units, 4 time points | Friedman | Non-parametric repeated measures | Repeated-measures ANOVA assumes normality and sphericity |
| Same units, yes/no, two time points | Exact McNemar | Uses discordant pairs; exact for small counts | Chi-square assumes independent groups |
| Two independent groups, skewed numeric | Mann–Whitney U | Rank-based, robust to outliers and unequal sizes | t-test distorted by skew and outliers |
| Two categorical variables (2×2) | Chi-square / Fisher | Tests independence; Fisher exact for small cells | t-test needs a continuous outcome |
| Many tests at once | Holm correction | Controls false positives with good power | Bonferroni is too conservative; no correction inflates errors |
| Published % only, two groups | Two-proportion z | Works from percentages and n | McNemar needs the same respondents |
| Published % vs a benchmark | One-sample z | Tests "majority" against 50% | Needs raw data for exact binomial on items without n |
| Strength of a link, skewed, small n | Spearman | Rank-based, robust | Pearson sensitive to outliers |
| Link plus slope | Pearson + OLS | Strength plus an interpretable effect | Correlation alone gives no slope |
| Small purposive Likert sample | Descriptive means/SD vs 3 | Honest, given the sample | Wilcoxon/t-test/alpha not meaningful at this size |
| Free-text interviews | Thematic analysis | Fits qualitative data | Statistical tests need numerical, sampled data |
