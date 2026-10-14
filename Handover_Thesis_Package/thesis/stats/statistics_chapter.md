# Statistical Analysis and Hypothesis Testing

## 1. Purpose

This chapter adds simple quantitative evidence to the qualitative findings. It tests whether public data support the study's main claims: AI use in banking is rising, bank disclosures increasingly cover AI, reskilling and AI regulation, AI-related roles need a different skill mix, and skills are a recognised constraint. The tests are hypotheses H5–H10. They complement propositions P1–P4 and questionnaire hypotheses H1–H4; they do not replace them.

All analysis is reproducible with `stats/scripts/analysis.py`. Full output is in `stats/out/results.md` and `stats/out/test_results.csv`. The significance level is α = 0.05.

## 2. Data sources

| Dataset | Source | Unit and coverage | Role |
|---|---|---|---|
| D1 | Eurostat (`isoc_eb_ai`, `isoc_sks_itspt`) | 27 EU countries; 2021, 2023, 2024, 2025 | Economy-wide AI adoption and ICT-skills context |
| D2 | Bank annual reports from official investor-relations sites | 29 large UK/EU banks (7 UK, 22 EU); FY2022 and FY2025. 42 of 58 report-years coded; 19 banks have both years | Change in AI, reskilling, AI-governance and regulation disclosure |
| D3 | Reed.co.uk job adverts | 163 UK financial-services GRC adverts; 83 with an annual salary | Skills and pay in AI-exposed roles |
| D4 | Published surveys (Bank of England/FCA 2022 and 2024, IIA, Thomson Reuters) | Published proportions with sample sizes | Industry adoption and skills-constraint evidence |

**D2 sampling.** The frame is fixed in `DATA_SPEC.md`. Each bank's full English annual report (or universal registration document) was taken from its own investor-relations site. Each file was checked against its title page for the right bank and fiscal year. Report-years that were not used are listed with a reason in the private bank key. Reasons include: no full English report found, site blocks automated access, or only a summary or extract available. Banks appear as codes (Bank A … Bank AC) in tables.

## 3. Variables

| Variable | Definition |
|---|---|
| `ai_ge10`, `ai_ge250` (D1) | % of enterprises (10+ / 250+ employees) using at least one AI technology |
| `ict_spec_pc_emp` (D1) | ICT specialists as % of total employment |
| `ai_d` (D2) | Mentions of AI terms (artificial intelligence, machine learning, generative AI, LLM, "AI") per 10,000 words |
| `reskill_d` (D2) | Mentions of reskilling/upskilling/retraining, digital skills, AI/data literacy, skills gap/development per 10,000 words |
| `aigov_d` (D2) | Mentions of AI governance, responsible/ethical AI, human oversight / human-in-the-loop, explainability, model risk per 10,000 words |
| `reg_d` (D2) | Mentions of the EU AI Act, DORA / digital operational resilience, PRA SS1/23 per 10,000 words |
| `aigov_body` (D2) | 1 if the report names a dedicated AI governance body or role (e.g. chief data/AI officer, AI council or committee, responsible-AI office), else 0 |
| `ai_ml` (D3) | 1 if the advert text mentions AI/ML ("AI-exposed") |
| Skill flags (D3) | 1 if the advert asks for data, regulatory, cyber, automation, certification or governance skills |
| `salary_annual_mid` (D3) | Midpoint of the advertised annual salary (£) |

D2 counts come from fixed regular expressions run over the full extracted text, divided by total word count, so long and short reports can be compared fairly.

## 4. Hypotheses

| | H0 (null) | H1 (alternative) | Data |
|---|---|---|---|
| H5a | AI adoption did not increase between 2021/2023 and 2025 | AI adoption increased | D1 |
| H5b | ICT-specialist share is not associated with AI adoption | Positive association | D1 |
| H6 | Skill demand is the same in AI-exposed and other adverts | Skill demand differs | D3 |
| H7 | AI-related adverts do not offer higher pay | AI-related adverts offer higher pay | D3 |
| H8 | The share of UK financial firms using AI did not rise 2022→2024 | The share rose | D4 |
| H9 | At most half of firms/professionals see skills/talent as a constraint | More than half do | D4 |
| H10a | AI / reskilling / AI-governance / regulation term density did not rise FY2022→FY2025 | Density rose | D2 |
| H10b | The share of banks naming an AI governance body did not change | The share changed | D2 |
| H10c | FY2025 AI density is not correlated with reskilling density | They are correlated | D2 |
| H10d | UK and EU banks do not differ in FY2025 densities | They differ | D2 |

## 5. Choice of tests

- **Paired t-test with Wilcoxon signed-rank (H5a, H10a).** The same countries or banks are measured twice, so the comparison is paired. The t-test compares mean change. The Wilcoxon test checks the result without assuming normality, which matters for small, skewed samples such as D2 densities. Both are one-sided because the hypotheses predict an increase.
- **Friedman test (H5a).** A non-parametric repeated-measures test across all four Eurostat years.
- **Pearson, Spearman and simple OLS (H5b).** These measure the strength of the ICT-skills/AI link. Spearman is the rank-based check.
- **Chi-square / Fisher exact with Holm correction (H6).** Skill flags are yes/no. Fisher is used when expected cell counts are small. Holm controls for testing six skills at once.
- **Mann–Whitney U with Welch t (H7, H10d).** These compare two independent groups. Salaries and densities are skewed, and groups are small (6 UK vs 16 EU banks), so the rank test is the main test. Holm correction is applied across the four D2 densities.
- **Two-proportion and one-sample z-tests (H8, H9).** Only published proportions and sample sizes are available.
- **McNemar exact test (H10b).** A paired yes/no outcome for the same banks in two years.
- **Spearman rho (H10c).** A rank correlation that is robust to outliers in a small sample.

## 6. Results

### 6.1 D1 – AI adoption across EU economies (H5)

| Year | Mean AI adoption, 10+ staff (%) | Mean AI adoption, 250+ staff (%) | Mean ICT specialists (% employment) |
|---|---|---|---|
| 2021 | 7.7 | 27.5 | 4.8 |
| 2023 | 8.2 | 30.2 | 5.1 |
| 2024 | 14.3 | 41.2 | 5.3 |
| 2025 | 20.7 | 53.6 | 5.4 |

| Test | Statistic | p | Effect | n |
|---|---|---|---|---|
| H5a paired t, 250+ staff, 2021→2025 | t = 18.99 | <0.0001 | +26.1 pp; dz = 3.66 | 27 |
| H5a Wilcoxon, 250+ staff, 2021→2025 | W = 378 | <0.0001 | 27/27 countries up | 27 |
| H5a paired t, 10+ staff, 2021→2025 | t = 10.35 | <0.0001 | +13.0 pp; dz = 1.99 | 27 |
| H5a Friedman, 250+ staff, four years | χ² = 73.31 | <0.0001 | | 27 |
| H5b Pearson, ICT share vs AI (10+), 2025 | r = 0.75 | <0.0001 | | 27 |
| H5b OLS, AI(10+) on ICT share, 2025 | t = 5.70 | <0.0001 | b = 5.09 pp per 1 pp; R² = 0.57 | 27 |

H5a and H5b are supported. Adoption rose in every country, and countries with more ICT specialists adopt more AI (Figure 1, `out/fig_D1.png`).

### 6.2 D2 – Bank annual reports (H10)

Mean (median) density per 10,000 words, 19 banks with both years:

| Measure | FY2022 | FY2025 |
|---|---|---|
| AI terms (`ai_d`) | 0.27 (0.15) | 2.87 (2.58) |
| Reskilling terms (`reskill_d`) | 0.21 (0.12) | 0.37 (0.30) |
| AI governance terms (`aigov_d`) | 0.88 (0.82) | 1.03 (0.75) |
| Regulation terms (`reg_d`) | 0.03 (0.00) | 0.22 (0.15) |
| Banks naming an AI governance body | 5% | 42% |

| Test | Statistic | p | Effect | n |
|---|---|---|---|---|
| H10a AI density, paired t | t = 6.61 | <0.0001 | +2.61; dz = 1.52 | 19 |
| H10a AI density, Wilcoxon | W = 190 | <0.0001 | 19/19 banks up | 19 |
| H10a reskilling density, paired t | t = 2.09 | 0.026 | +0.16; dz = 0.48 | 19 |
| H10a reskilling density, Wilcoxon | W = 142 | 0.030 | 13/19 banks up | 19 |
| H10a AI governance density, paired t | t = 1.56 | 0.068 | +0.15; dz = 0.36 | 19 |
| H10a AI governance density, Wilcoxon | W = 132 | 0.072 | 13/19 banks up | 19 |
| H10a regulation density, paired t | t = 5.42 | <0.0001 | +0.20; dz = 1.24 | 19 |
| H10a regulation density, Wilcoxon | W = 171 | <0.0001 | 18/19 banks up | 19 |
| H10b AI governance body, McNemar exact | — | 0.016 | 7 banks 0→1, 0 banks 1→0 | 19 |
| H10c AI vs reskilling density, FY2025, Spearman | ρ = −0.16 | 0.487 | | 22 |
| H10d AI density UK vs EU, FY2025, Mann–Whitney | U = 87 | 0.002 (Holm 0.007) | median 3.96 vs 2.00 | 6 + 16 |
| H10d reskilling density UK vs EU | U = 23 | 0.070 (Holm 0.140) | median 0.22 vs 0.42 | 6 + 16 |
| H10d AI governance density UK vs EU | U = 94 | 0.0001 (Holm 0.0004) | median 2.01 vs 0.50 | 6 + 16 |
| H10d regulation density UK vs EU | U = 45 | 0.858 (Holm 0.858) | median 0.21 vs 0.15 | 6 + 16 |

- **Supported:** H10a for AI, reskilling and regulation terms. AI mentions rose about tenfold, in every bank. AI Act/DORA/SS1/23 mentions went from near zero to routine. H10b is also supported: banks naming a dedicated AI governance body rose from 1 in 19 to 8 in 19.
- **Not supported:** H10a for AI-governance terms (p ≈ 0.07). Model-risk and oversight language was already common in FY2022 and did not grow much.
- **H10c is not supported.** Banks that talk most about AI do not talk most about reskilling. AI disclosure has grown much faster than reskilling disclosure.
- **H10d is partly supported.** UK banks mention AI and AI governance more than EU banks. Reskilling and regulation show no significant regional difference.

See Figure 2 (`out/fig_D2.png`).

### 6.3 D3 – Job adverts (H6, H7)

Of the 163 adverts, 44.2% mention AI/ML (95% CI 36.8–51.8%).

| Skill | AI-exposed (%) | Other (%) | Test | p (Holm) | Odds ratio |
|---|---|---|---|---|---|
| Data | 51.4 | 25.3 | χ² = 11.79 | 0.002 | 3.13 |
| Regulatory | 40.3 | 78.0 | χ² = 24.15 | <0.0001 | 0.19 |
| Cyber | 19.4 | 5.5 | χ² = 7.60 | 0.018 | 4.15 |
| Automation | 48.6 | 13.2 | χ² = 24.58 | <0.0001 | 6.23 |
| Certification | 15.3 | 12.1 | χ² = 0.35 | 1.000 | 1.31 |
| Governance | 52.8 | 48.4 | χ² = 0.32 | 1.000 | 1.19 |

| Pay comparison | Test | Statistic | p | Medians | n |
|---|---|---|---|---|---|
| AI-exposed vs other | Mann–Whitney | U = 898.5 | 0.193 | £70,000 vs £59,250 | 31 vs 52 |
| AI-titled vs traditional | Mann–Whitney | U = 453.5 | 0.009 | £90,000 vs £60,000 | 8 vs 75 |

H6 is supported for data, regulatory, cyber and automation skills. AI-exposed adverts want more technical skills and fewer regulatory skills. H7 is supported only for AI-titled roles, and that group is very small. See Figure 3 (`out/fig_D3.png`).

### 6.4 D4 – Published surveys (H8, H9)

| Test | Statistic | p | Effect | n |
|---|---|---|---|---|
| H8 UK FS firms using AI, 2022→2024 | z = 2.41 | 0.008 | 58% → 75% | 71 / 118 |
| H9 Talent/skills a large or medium constraint | z = 1.49 | 0.069 | 57% vs 50% | 118 |
| H9 Experienced auditors need more tech skills (IIA) | z = 189.4 | <0.0001 | 96% | 6,506 |
| H9 High/transformative AI impact expected (TR) | z = 35.8 | <0.0001 | 80% | 2,275 |

H8 is supported. H9 is supported for the professional surveys, but not for the Bank of England/FCA firm-level item, which is just short of significance.

### 6.5 Questionnaire (descriptive only)

The questionnaire is reported descriptively, as construct means on a 5-point scale. No inferential tests are run. Means: A 3.58, B 4.00, C 3.87, D 3.89, E 3.75, F 3.83, G 3.58.

## 7. Interpretation against objectives and propositions

| Proposition / objective | Statistical evidence | Verdict |
|---|---|---|
| Objective (i), P1: routine GRC work is automated and AI use is spreading | H5a, H8, H10a (AI): adoption and AI disclosure rose strongly and consistently | Supported |
| Objective (ii), P2: regulation makes oversight and competence obligations | H10a (regulation) and H10b: AI Act/DORA/SS1/23 mentions and named AI governance bodies rose significantly; H10d shows UK banks discuss AI governance more | Supported |
| Objective (iii), P3: a hybrid technical + regulatory skill profile is needed | H6: AI roles are technical-heavy and regulatory-light (the hybrid gap); H5b: ICT skills track AI adoption; H9: skills are a recognised constraint; H10a: reskilling disclosure rose | Supported |
| Objective (iii), management response to skill gaps | H10c: reskilling disclosure is not linked to AI intensity and grew far less than AI disclosure | Gap between AI ambition and stated reskilling effort |
| P4: knowledge-loss risk | Not directly measurable in public data; indirect support from slower growth in reskilling than in AI disclosure | Qualitative evidence only |
| Objective (iv): employee responses | Questionnaire construct means (descriptive) | Descriptive only |

**Overall:** the numbers support the qualitative story. AI adoption and AI disclosure in banks have risen sharply since 2022, and so have regulatory and governance structures. Skills and reskilling responses are growing more slowly and are not matched to AI intensity. This supports the case for the workforce framework in objective (v).

## 8. Limitations

- **D1** covers the whole economy and excludes the financial sector. It is context only.
- **D2** counts words, not actions. A mention of AI or reskilling does not show what a bank actually does. Results also depend on report length, language and PDF text extraction. Only 19 of 29 banks had both years available, and UK banks are few (6 in FY2025), so the regional tests have low power. One bank's fiscal year ends in April and is mapped to the nearest year.
- **D3** comes from one UK job board on one collection date (a convenience sample). It has no EU adverts and very few AI-titled adverts (19; 8 with salary), so the H7 pay result is indicative only.
- **D4** is secondary published data. The survey waves use different firm samples.
- **Questionnaire** results are descriptive only and are not generalised.
- Multiple tests are run. Holm corrections are applied within families (H6, H10d), but other p-values are unadjusted.
