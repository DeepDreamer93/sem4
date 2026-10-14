# HANDOVER: MBA thesis "AI-Driven Transformation in Banking GRC: Implications for Workforce Management in UK and EU Banks"
Student: Narentheran S (Online MBA BAGM, CDOE Anna University; Roll 2406OBA0034, Reg 69124100089). Course is Business Analytics, so the thesis needs basic hypothesis testing.

## 1. Non-negotiable user rules
1. **Never name individual banks** in any thesis text, table, chart or slide. Use "Bank A, B…" or "large UK/EU banks". Bank names exist ONLY in `stats/data/PRIVATE_bank_key.csv` and the raw PDFs (internal use).
2. **Never state how many interviews/questionnaires/responses were collected.** Report questionnaire results as means/SD only, never respondent percentages (they reveal n). (Internal fact for you only: interview sheet has 4 rows, questionnaire 3 rows. The questionnaire is fixed and will not grow.)
3. Cited public-source figures (percentages, growth rates) ARE allowed, with source.
4. Review 1 report is the controlling baseline (objectives unchanged).
5. When filling a university template, paste content into the user's template preserving its fonts/layout exactly.
6. User likes: a Markdown draft first for review, then the final Word/PPT. Short, plain-English messages.
7. Do not update the Second Review report; the stats work is an add-on for the final thesis.

## 2. What is done (files under `thesis/`)
| File | What |
|---|---|
| `out/Second_Review_Report_Narentheran_S.docx` | Filled Second Review template (submitted version) |
| `out/Second_Review_Report_Draft.md` | Approved Markdown source of the above |
| `out/Second_Review_Presentation_Narentheran_S.pptx` | 9-slide deck, 5–6 min, speaker notes |
| `out/Presentation_Prep_Guide.md`, `out/Slide_Talking_Points.md` | Viva prep: 30 Q&A, talking points |
| `out/GRC_Workforce_Analysis_Narentheran_S.docx` | Earlier analysis chapter (themes T1–T10, role map, framework) |
| `out/Web_Research_Reference_Compendium.md` | Unfiltered web research (20 sources) |
| `research/` | Downloaded source PDFs/text (PRA SS1/23, TR 2025, IIA Vision 2035, GSDC 2026, FCA, ECB) + NOTES.md |
| `txt/` | Text extracts of the user's Review 1 report, annexures, interview questions, Review 1 deck |
| `../attachments/` | All original user files (Review 1 docx/pdf/pptx, annexures, proposals, response spreadsheets, Review 2 template) |

Known open fix: in `Second_Review_Report_Draft.md` / docx Section 5, the paragraph "Conditional trust (H4)" compares item 17 with item 16 (4.33) and says it supports H4; H4 is defined vs item 15 (both 3.67 → not supported). User was told; awaiting a decision. Do not change the Second Review unless asked.

Framework: P1–P4 propositions (qualitative, all supported), H1–H4 questionnaire hypotheses (directional only; H4 not supported). Questionnaire constructs A 7–10, B 11–13, C 14–18, D 19–21, E 22–25, F 26–27, G 28–31; reverse-code 19, 20, 21, 30. Composite means: A 3.58, B 4.00, C 3.87, D 3.89, E 3.75, F 3.83, G 3.58.

## 3. Statistical add-on (IN PROGRESS), in `stats/`
Spec (authoritative coding rules, regexes, frame of 29 banks): `stats/DATA_SPEC.md`. Collectors: `stats/scripts/collect_d*.py` (+ `scripts/README.md`). Analysis: `stats/scripts/analysis.py` → `stats/out/results.md`, `test_results.csv`, `fig_D1.png`, `fig_D3.png`.
Python deps: `pip install --user scipy statsmodels matplotlib tabulate pandas`.

| Dataset | Status | Notes |
|---|---|---|
| D1 Eurostat (`data/D1_eurostat.csv`) | DONE: 27 EU countries + EU27 aggregate × 2021/23/24/25 | isoc_eb_ai (E_AI_TANY, PC_ENT, GE10 & GE250) + isoc_sks_itspt (PC_EMP). **Survey excludes the financial sector**: present as economy-wide context only. |
| D2 Bank annual reports (`data/D2_bank_reports.csv`) | **INCOMPLETE: 6 of 58 bank-years coded; paired n = 1** | See section 4. |
| D3 Reed UK job ads (`data/D3_job_ads.csv`) | DONE: 163 financial-services ads (19 AI-titled, 144 traditional; 72 mention AI/ML; 83 with annual salary) | No employer names. Reed salaryType: 5 = annual, 2 = daily, 1 = hourly (only annual used). LinkedIn/Indeed block automation; EURES public search reachable but not collected (EU ads missing). |
| D4 survey proportions (`data/D4_survey_props.csv`) | DONE: 12 rows, 9 with n | BoE/FCA 2024 n=118, 2022 n=71; IIA n=6,506; TR n=2,275. 46%/34%/84% rows have no item n: don't test them. |

Results so far (`stats/out/results.md`), already shared with the user:
- H5a: AI adoption rose 2021/2023→2025 in all 27 countries (paired t, Wilcoxon, Friedman; p<0.001; 250+ firms ~30%→54%).
- H5b: ICT-specialist share vs AI adoption, 2025: r=0.75, OLS R²=0.57.
- H6: AI-exposed ads (description mentions AI/ML) vs others: data 51% vs 25%, automation, cyber higher; regulatory 40% vs 78% lower (chi-square, Holm-adjusted, all significant); governance and cert not significant. Interpretation: AI roles written as technical roles; regulatory knowledge sits in traditional roles → hybrid-profile gap (supports P3).
- H7: pay premium significant only for AI-titled ads (median £90k vs £60k, p=0.009, but only n=8 with salary); not for AI-exposed ads.
- H8: UK FS firms using AI 58%→75% (2022→2024, two-proportion z, p=0.008; different firm samples).
- H9: talent constraint large+medium 57% vs 50%: p=0.069 (NOT significant); IIA 96% and TR 80% significantly > 50%.
- Questionnaire: descriptive only (no tests, n too small).
Minor: `fig_D1.png` x-axis shows decimal years; set integer ticks.

## 4. D2: next steps (main remaining data task)
- Frame: 29 banks in `DATA_SPEC.md` (7 UK, 22 EU), FY2022 vs FY2025, English annual report from the bank's own IR site; codes A..AC from a seed-42 shuffle (key in PRIVATE_bank_key.csv).
- Coded: A-2025, E-2025, J-2025, Q-2025, V-2022, V-2025. **Q-2025 is suspect** (19,449 words, all counts 0): probably a summary doc, not the full annual report. Re-source it.
- `raw/d2/` (in the separate raw zip) holds 6 more unkeyed PDFs (A/E/H/M FY2022, H/M FY2025): verify bank and year from the first pages, record URL/title in the key, then code them.
- Bank IR sites are reachable with a browser UA (HSBC, Barclays, Lloyds, Deutsche Bank tested HTTP 200); some (ING) return 403 to curl, so use a real browser.
- Collector gaps: doesn't validate bank/year itself, swallows download errors, trusts existing local PDFs.
- Target: >= 20 banks with both years. Then add to analysis.py:
  - H10: paired t-test + Wilcoxon on ai_d, reskill_d, aigov_d, reg_d (FY2022 vs FY2025).
  - McNemar on aigov_body.
  - Spearman ai_d vs reskill_d (FY2025).
  - Mann-Whitney UK vs EU on FY2025 densities.
  Report only Bank A/B… codes.

## 5. After D2: deliverable the user expects
A thesis-ready "Statistical Analysis & Hypothesis Testing" chapter (Markdown first for review, then Word):
- data sources and sampling;
- variables and coding (from the spec);
- hypotheses H5–H10 with H0/H1;
- tests and why (non-parametric where appropriate);
- results tables and charts;
- interpretation linked to objectives and P1–P4;
- limitations (D1 excludes finance; D3 single UK board, convenience sample, few AI titles; D4 secondary; questionnaire descriptive only).
Then possibly the final thesis and viva deck.

## 6. Environment gotchas
- LibreOffice cannot render docx/pptx on this VM (Writer/Impress missing, no sudo). Ask the user to check layout in Office.
- Use polite collection (>= 3 s per host, respect robots.txt, no login walls).
