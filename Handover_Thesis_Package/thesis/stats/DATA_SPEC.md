# Statistical add-on: data collection & coding spec (authored by lead; follow exactly)
Root: /home/ubuntu/thesis/stats  (raw/ caches, data/ final CSVs, scripts/ collection+coding code)
General: polite collection only (>=3 s between requests to the same host, respect robots.txt, no login walls, no bypassing 403/429). Keep raw downloads in raw/. Never put bank/employer names in any data/ file except data/PRIVATE_bank_key.csv.

## D1 Eurostat (country panel)
- isoc_eb_ai: indic_is=E_AI_TANY, unit=PC_ENT, nace_r2=C10-S951_X_K, size_emp in {GE10, GE250}; all geo that are EU27 member states individually (exclude EU aggregates, EA etc. -> but also save EU27_2020 aggregate in a separate row flagged is_aggregate=1); all available years.
- isoc_sks_itspt: unit=PC_EMP, same geos/years.
- Output data/D1_eurostat.csv long-ish: geo,year,ai_ge10,ai_ge250,ict_spec_pc_emp,is_aggregate,flag_notes (Eurostat status flags e.g. 'b','u' as text). Missing = blank.

## D2 Bank annual reports (FY2022 vs FY2025, English PDFs from the banks' own IR sites)
Frame (fixed list, 29 groups): UK: HSBC Holdings, Barclays, Lloyds Banking Group, NatWest Group, Standard Chartered, Santander UK, Nationwide Building Society. EU: BNP Paribas, Crédit Agricole, Société Générale, Groupe BPCE, Banco Santander, BBVA, CaixaBank, Deutsche Bank, Commerzbank, ING Group, ABN AMRO, Rabobank, UniCredit, Intesa Sanpaolo, Nordea, Danske Bank, KBC Group, Erste Group, SEB, Handelsbanken, Bank of Ireland, AIB Group.
- Use the main Annual Report (integrated annual report / annual report & accounts; if only a "Universal Registration Document" exists, use it). For FY2025 if unpublished/not English, mark missing. Record source URL + doc title in PRIVATE key.
- Extract text with pdftotext. Lower-case for matching. Count matches per regex (case-insensitive) below; compute total_words (whitespace tokens).
  - ai: `\bartificial intelligence\b|\bmachine learning\b|\bgenerative ai\b|\bgen ?ai\b|\blarge language models?\b|\bllms?\b|\bai\b`
  - reskill: `\bre-?skill\w*|\bup-?skill\w*|\bretrain\w*|\bdigital skills?\b|\bai literacy\b|\bdata literacy\b|\bskills? (gap|development)\b`
  - aigov: `\bai governance\b|\bresponsible ai\b|\bai ethics\b|\bethical ai\b|\bhuman oversight\b|\bhuman[- ]in[- ]the[- ]loop\b|\bexplainab\w*|\bmodel risk\b`
  - reg: `\bai act\b|\bartificial intelligence act\b|\bdora\b|\bdigital operational resilience\b|\bss1/23\b`
  - aigov_body (binary 0/1): `chief (ai|artificial intelligence|data( and| &) ai|data) officer|ai (council|committee|board|office|centre of excellence|center of excellence)|responsible ai (office|council|committee|lead|team|framework)`
  - Exclude false-positive tokens before counting `\bai\b`: remove the strings "a.i." none; but DO strip "aig" isn't affected; note the IDs 'AIB' are unaffected by \bai\b. Also remove the literal bank name tokens for AIB? (not needed).
- Output data/D2_bank_reports.csv: bank_code (A..AC assigned alphabetically by a RANDOM shuffle with seed 42, not by name), region (UK/EU), fy (2022/2025), total_words, ai, reskill, aigov, reg, aigov_body, then densities per 10,000 words: ai_d, reskill_d, aigov_d, reg_d. One row per bank-year. data/PRIVATE_bank_key.csv: bank_code,bank_name,fy,doc_title,url.

## D3 Job adverts (Reed UK; EU optional)
- Queries (Reed search URL pattern https://www.reed.co.uk/jobs/<slug>-jobs, pages 1-2 only):
  AI-related: "ai governance", "ai risk", "ai compliance", "responsible ai", "ai audit", "ai model risk"
  Traditional GRC: "compliance analyst", "kyc analyst", "aml analyst", "risk analyst", "regulatory reporting", "internal auditor", "operational risk", "model risk"
- Open each job detail page (/jobs/<slug>/<id>), take full description text. Dedupe on job id.
- Keep only financial-services adverts: description matches `\bbank\w*|financial services|financial institution|fintech|asset manag|insurer|insurance|wealth manag|payments?|lending|building society|fca|pra` (case-insens.). Record kept/excluded counts.
- role_type: "AI" if TITLE matches `\b(ai|a\.i\.|artificial intelligence|machine learning|ml|genai|generative|llm)\b` else "Traditional".
- Skill flags 0/1 on DESCRIPTION:
  data: `\bsql\b|\bpython\b|\br\b programming|data analy\w*|power ?bi|tableau|\banalytics\b|data science`
  ai_ml: `\bai\b|artificial intelligence|machine learning|\bllms?\b|generative|gen ?ai`
  reg: `\bfca\b|\bpra\b|regulat\w*|\bdora\b|ai act|sm&cr|smcr|consumer duty|basel|\bgdpr\b`
  cyber: `cyber|information security|iso ?27001|\bnist\b`
  automation: `automat\w*|\brpa\b`
  cert: `\bcipp|\baigp\b|\bcams\b|\bcisa\b|\bcissp\b|\bcrisc\b|\bacca\b|\bcfa\b|\bica\b|\biapp\b|iso ?42001|\bfrm\b|\bprm\b|\bcia\b`
  governance: `governance|oversight|accountab\w*`
- Salary: from page JSON salaryFrom/salaryTo/salaryType. Keep salary_annual_mid only when it is an annual figure (if salaryType code is ambiguous, inspect a few pages to establish which code means annual vs daily/hourly and record mapping in scripts/README). Otherwise blank.
- Output data/D3_job_ads.csv: ad_id (sequential, not Reed id), query, role_type, date_posted, location_region (city/region text ok), salary_from, salary_to, salary_annual_mid, title, flags..., word_count. NO employer name. raw HTML in raw/reed/.
- Target >= 120 kept ads with >= 35 in each role_type; if short, add pages 3 of the same queries only. Optional EU: check if EURES (eures.europa.eu) public job search is accessible without login; if yes, report how, do NOT collect yet.

## D4 Published survey proportions
From /home/ubuntu/thesis/research/ files and the official BoE/FCA "Artificial intelligence in UK financial services 2024" report (download PDF to raw/ if not present) and the 2022 BoE/FCA ML survey, plus IIA Vision 2035 and Thomson Reuters Future of Professionals 2025 PDFs in research/:
- Rows: source, year, statement (verbatim), proportion (0-1), n_respondents, n_quote (verbatim sentence giving sample size), page.
- Include at least: % firms using AI (2024) and the comparable 2022 figure; % partial understanding; % complete understanding; talent large constraint; talent medium constraint; % with accountable person; IIA 96% and 81%; TR >40% skills gap (record exact %), TR 80%.
- Only record a row when both the proportion and n are found verbatim. Missing n -> include row with n blank and note.
Output data/D4_survey_props.csv.
