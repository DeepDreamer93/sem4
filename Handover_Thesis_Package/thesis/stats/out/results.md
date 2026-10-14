# Statistical results

## Hypothesis tests

| hypothesis                                                                  | data   | test                              |   statistic | p_value   | effect                                   |    n | note                             |
|:----------------------------------------------------------------------------|:-------|:----------------------------------|------------:|:----------|:-----------------------------------------|-----:|:---------------------------------|
| H5a: AI adoption rose 2023->2025 (enterprises 10+ staff)                    | D1     | Paired t-test (one-sided)         |       9.487 | <0.0001   | mean diff 12.49 pp; Cohen dz 1.83        |   27 |                                  |
| H5a: AI adoption rose 2023->2025 (enterprises 10+ staff)                    | D1     | Wilcoxon signed-rank (one-sided)  |     378     | <0.0001   | median diff 11.35 pp; 27/27 countries up |   27 |                                  |
| H5a: AI adoption rose 2021->2025 (enterprises 10+ staff)                    | D1     | Paired t-test (one-sided)         |      10.348 | <0.0001   | mean diff 13.03 pp; Cohen dz 1.99        |   27 |                                  |
| H5a: AI adoption rose 2021->2025 (enterprises 10+ staff)                    | D1     | Wilcoxon signed-rank (one-sided)  |     378     | <0.0001   | median diff 11.76 pp; 27/27 countries up |   27 |                                  |
| H5a: AI adoption rose 2023->2025 (enterprises 250+ staff)                   | D1     | Paired t-test (one-sided)         |      19.001 | <0.0001   | mean diff 23.37 pp; Cohen dz 3.66        |   27 |                                  |
| H5a: AI adoption rose 2023->2025 (enterprises 250+ staff)                   | D1     | Wilcoxon signed-rank (one-sided)  |     378     | <0.0001   | median diff 22.56 pp; 27/27 countries up |   27 |                                  |
| H5a: AI adoption rose 2021->2025 (enterprises 250+ staff)                   | D1     | Paired t-test (one-sided)         |      18.993 | <0.0001   | mean diff 26.09 pp; Cohen dz 3.66        |   27 |                                  |
| H5a: AI adoption rose 2021->2025 (enterprises 250+ staff)                   | D1     | Wilcoxon signed-rank (one-sided)  |     378     | <0.0001   | median diff 27.08 pp; 27/27 countries up |   27 |                                  |
| H5a: AI adoption differs across 2021/23/24/25 (250+)                        | D1     | Friedman test                     |      73.311 | <0.0001   |                                          |   27 |                                  |
| H5b: ICT-specialist share correlates with AI adoption (10+, 2025)           | D1     | Pearson r                         |       0.752 | <0.0001   | r=0.75                                   |   27 |                                  |
| H5b: ICT-specialist share correlates with AI adoption (10+, 2025)           | D1     | Spearman rho                      |       0.753 | <0.0001   | rho=0.75                                 |   27 |                                  |
| H5b: ICT-specialist share correlates with AI adoption (250+, 2025)          | D1     | Pearson r                         |       0.623 | 0.0005    | r=0.62                                   |   27 |                                  |
| H5b: ICT-specialist share correlates with AI adoption (250+, 2025)          | D1     | Spearman rho                      |       0.62  | 0.0006    | rho=0.62                                 |   27 |                                  |
| H5b: OLS AI adoption(10+) = a + b*ICT share (2025)                          | D1     | Simple linear regression          |       5.704 | <0.0001   | b=5.09 pp per 1 pp ICT share; R2=0.57    |   27 |                                  |
| H6: AI-exposed adverts differ in demand for data skills                     | D3     | Chi-square (1 df)                 |      11.785 | 0.0006    | OR=3.13; phi=0.27                        |  163 | Holm-adjusted p=0.0024           |
| H6: AI-exposed adverts differ in demand for reg skills                      | D3     | Chi-square (1 df)                 |      24.15  | <0.0001   | OR=0.19; phi=0.38                        |  163 | Holm-adjusted p=0.0000           |
| H6: AI-exposed adverts differ in demand for cyber skills                    | D3     | Chi-square (1 df)                 |       7.596 | 0.0058    | OR=4.15; phi=0.22                        |  163 | Holm-adjusted p=0.0175           |
| H6: AI-exposed adverts differ in demand for automation skills               | D3     | Chi-square (1 df)                 |      24.581 | <0.0001   | OR=6.23; phi=0.39                        |  163 | Holm-adjusted p=0.0000           |
| H6: AI-exposed adverts differ in demand for cert skills                     | D3     | Chi-square (1 df)                 |       0.35  | 0.5539    | OR=1.31; phi=0.05                        |  163 | Holm-adjusted p=1.0000           |
| H6: AI-exposed adverts differ in demand for governance skills               | D3     | Chi-square (1 df)                 |       0.315 | 0.5746    | OR=1.19; phi=0.04                        |  163 | Holm-adjusted p=1.0000           |
| H6 (robustness): AI-titled vs traditional adverts, data                     | D3     | Fisher exact                      |       2.089 | 0.1375    | OR=2.09                                  |  163 | AI-titled n small; indicative    |
| H6 (robustness): AI-titled vs traditional adverts, reg                      | D3     | Fisher exact                      |       0.667 | 0.4567    | OR=0.67                                  |  163 | AI-titled n small; indicative    |
| H6 (robustness): AI-titled vs traditional adverts, cyber                    | D3     | Fisher exact                      |       4.651 | 0.0116    | OR=4.65                                  |  163 | AI-titled n small; indicative    |
| H6 (robustness): AI-titled vs traditional adverts, automation               | D3     | Fisher exact                      |       2.511 | 0.1025    | OR=2.51                                  |  163 | AI-titled n small; indicative    |
| H6 (robustness): AI-titled vs traditional adverts, cert                     | D3     | Fisher exact                      |       0.729 | 1.0000    | OR=0.73                                  |  163 | AI-titled n small; indicative    |
| H6 (robustness): AI-titled vs traditional adverts, governance               | D3     | Fisher exact                      |       1.414 | 0.6266    | OR=1.41                                  |  163 | AI-titled n small; indicative    |
| H7: AI-exposed vs not adverts offer higher pay                              | D3     | Mann-Whitney U (one-sided)        |     898.5   | 0.1931    | median £70,000 vs £59,250 (+18%)         |   83 | n=31 vs 52                       |
| H7: AI-exposed vs not adverts offer higher pay                              | D3     | Welch t-test (one-sided)          |       0.581 | 0.2817    | mean £71,364 vs £67,031                  |   83 |                                  |
| H7: AI-titled vs traditional adverts offer higher pay                       | D3     | Mann-Whitney U (one-sided)        |     453.5   | 0.0091    | median £90,000 vs £60,000 (+50%)         |   83 | n=8 vs 75                        |
| H7: AI-titled vs traditional adverts offer higher pay                       | D3     | Welch t-test (one-sided)          |       2.015 | 0.0402    | mean £99,349 vs £65,375                  |   83 |                                  |
| H8: share of UK FS firms using AI rose 2022->2024                           | D4     | Two-proportion z-test (one-sided) |       2.407 | 0.0080    | 58% (n=71) -> 75% (n=118)                |  189 | Different firm samples each wave |
| H9: majority of firms see talent/skills as a large or medium AI constraint  | D4     | One-sample z-test vs 50%          |       1.487 | 0.0686    | 25%+32%=57%                              |  118 |                                  |
| H9: majority agree - IIA: experienced auditors need more tech skills        | D4     | One-sample z-test vs 50%          |     189.442 | <0.0001   | 96%                                      | 6506 |                                  |
| H9: majority agree - TR: professionals expect high/transformative AI impact | D4     | One-sample z-test vs 50%          |      35.773 | <0.0001   | 80%                                      | 2275 |                                  |

## D1 Eurostat: descriptives (EU27 countries, % of enterprises / % of employment)

|   ('year', '') |   ('ai_ge10', 'mean') |   ('ai_ge10', 'median') |   ('ai_ge10', 'std') |   ('ai_ge250', 'mean') |   ('ai_ge250', 'median') |   ('ai_ge250', 'std') |   ('ict_spec_pc_emp', 'mean') |   ('ict_spec_pc_emp', 'median') |   ('ict_spec_pc_emp', 'std') |
|---------------:|----------------------:|------------------------:|---------------------:|-----------------------:|-------------------------:|----------------------:|------------------------------:|--------------------------------:|-----------------------------:|
|           2021 |                  7.7  |                    7.2  |                 5.03 |                  27.46 |                    24.38 |                 13.44 |                          4.77 |                             4.5 |                         1.39 |
|           2023 |                  8.24 |                    7.86 |                 4.17 |                  30.18 |                    28.34 |                 12.89 |                          5.09 |                             4.7 |                         1.49 |
|           2024 |                 14.28 |                   11.31 |                 7.18 |                  41.15 |                    40.48 |                 14.75 |                          5.31 |                             5   |                         1.43 |
|           2025 |                 20.73 |                   19.64 |                10.26 |                  53.56 |                    53.09 |                 14.96 |                          5.35 |                             4.9 |                         1.52 |

## D3 Job adverts: skill prevalence by group (% of adverts)

| AI_exposed     |   data |   reg |   cyber |   automation |   cert |   governance |   n |
|:---------------|-------:|------:|--------:|-------------:|-------:|-------------:|----:|
| AI-exposed     |   51.4 |  40.3 |    19.4 |         48.6 |   15.3 |         52.8 |  72 |
| Not AI-exposed |   25.3 |  78   |     5.5 |         13.2 |   12.1 |         48.4 |  91 |

By title-based role type:

| role_type   |   data |   reg |   cyber |   automation |   cert |   governance |   ai_ml |   n |
|:------------|-------:|------:|--------:|-------------:|-------:|-------------:|--------:|----:|
| AI          |   52.6 |  52.6 |    31.6 |         47.4 |   10.5 |         57.9 |   100   |  19 |
| Traditional |   34.7 |  62.5 |     9   |         26.4 |   13.9 |         49.3 |    36.8 | 144 |

Share of financial-services GRC adverts mentioning AI/ML: 44.2% (95% Wilson CI 36.8% to 51.8%), n=163.


## D4 Published survey proportions with 95% Wilson CIs

| source                                       |   year |   proportion |    n |   ci_low |   ci_high |
|:---------------------------------------------|-------:|-------------:|-----:|---------:|----------:|
| BoE/FCA AI survey 2024                       |   2024 |         0.75 |  118 |    0.66  |     0.816 |
| BoE/FCA AI survey 2024 (2022 comparison)     |   2022 |         0.58 |   71 |    0.462 |     0.685 |
| BoE/FCA ML survey 2022                       |   2022 |         0.72 |   71 |    0.605 |     0.81  |
| BoE/FCA AI survey 2024                       |   2024 |         0.25 |  118 |    0.184 |     0.34  |
| BoE/FCA AI survey 2024                       |   2024 |         0.32 |  118 |    0.244 |     0.411 |
| IIA Vision 2035                              |   2025 |         0.96 | 6506 |    0.955 |     0.965 |
| IIA Vision 2035                              |   2025 |         0.81 | 6506 |    0.8   |     0.819 |
| Thomson Reuters Future of Professionals 2025 |   2025 |         0.46 | 2275 |    0.439 |     0.48  |
| Thomson Reuters Future of Professionals 2025 |   2025 |         0.8  | 2275 |    0.783 |     0.816 |