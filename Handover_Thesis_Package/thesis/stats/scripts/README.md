# Dataset collection notes

## D1 — Eurostat

Collection stopped before output: the API response included an unexpected `freq` dimension, so the returned schema did not match the specified six dimensions. No D1 CSV or collector was created pending clarification.

## D2 — Annual reports

The private key contains 29 anonymised groups and two fiscal years each. No usable official investor-relations report URLs were identified, so the 58-row CSV retains all bank-years with blank metrics. No third-party report source was substituted.

## D3 — Reed salary coding and coverage

Observed Reed salary-type mappings on detail pages:

- `type.id=5`, `per annum`, `unitText=YEAR`: annual.
- `type.id=2`, `per day`, `unitText=DAY`: daily; not treated as annual.
- `type.id=1`, `per hour`, `unitText=HOUR`: hourly; not treated as annual.

The collector records an annual midpoint only when the page identifies an annual unit/name or supplies explicit annualized values. Daily and hourly salaries are not annualized.

The final collection contains 123 kept ads (14 AI, 109 Traditional), 103 excluded ads and 66 ads with an annual salary. It opened 226 detail pages across the required searches; page 3 added one new detail page. The minimum of 120 kept ads was met, but the minimum of 35 AI-role ads was not: the title-based role regex classified 14 as AI after pages 1–3. No later pages or alternate searches were used.

To honor the anonymisation constraint, cached detail HTML has employer-identification strings redacted, and search-result HTML is not retained. The CSV has no employer field.

## D4 — Survey denominators

Three D4 rows leave `n_respondents` blank: the 46% partial-understanding result, the 34% complete-understanding result, and the 84% accountable-person result from the 2024 BoE/FCA survey. The source does not report item-level denominators for those figures; the overall survey sample was not substituted.

## EURES

The English EURES public landing/search interface loaded without authentication at `/index_en` (HTTP 200, search form and job-related links present). No EURES job adverts were collected.
