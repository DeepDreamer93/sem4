#!/usr/bin/env python3
"""Collect and append coded public Reed UK job adverts."""

import csv
import html
import json
import re
import time
from collections import defaultdict
from html.parser import HTMLParser
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urljoin, urlsplit
from urllib.request import Request, urlopen


ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "raw" / "reed"
OUTPUT = ROOT / "data" / "D3_job_ads.csv"
BASE_URL = "https://www.reed.co.uk"
DELAY_SECONDS = 3.05
USER_AGENT = "MBA-thesis-public-dataset/1.0"
TARGET_KEPT = 120
TARGET_PER_ROLE = 35
FIELDS = [
    "ad_id",
    "query",
    "role_type",
    "date_posted",
    "location_region",
    "salary_from",
    "salary_to",
    "salary_annual_mid",
    "title",
    "data",
    "ai_ml",
    "reg",
    "cyber",
    "automation",
    "cert",
    "governance",
    "word_count",
]

QUERIES = [
    "ai governance",
    "ai risk",
    "ai compliance",
    "responsible ai",
    "ai audit",
    "ai model risk",
    "compliance analyst",
    "kyc analyst",
    "aml analyst",
    "risk analyst",
    "regulatory reporting",
    "internal auditor",
    "operational risk",
    "model risk",
]
ADDITIONAL_QUERIES = [
    "ai assurance",
    "ai ethics",
    "ai policy",
    "ai regulation",
    "model governance",
    "machine learning risk",
    "ai controls",
    "data and ai governance",
    "ai security",
    "ai product risk",
]

FINANCIAL = re.compile(
    r"\bbank\w*|financial services|financial institution|fintech|asset manag|"
    r"insurer|insurance|wealth manag|payments?|\blending\b|building society|\bfca\b|\bpra\b",
    re.IGNORECASE,
)
ROLE_AI = re.compile(
    r"\b(ai|a\.i\.|artificial intelligence|machine learning|ml|genai|generative|llm)\b",
    re.IGNORECASE,
)
SKILL_PATTERNS = {
    "data": r"\bsql\b|\bpython\b|\br\b programming|data analy\w*|power ?bi|tableau|\banalytics\b|data science",
    "ai_ml": r"\bai\b|artificial intelligence|machine learning|\bllms?\b|generative|gen ?ai",
    "reg": r"\bfca\b|\bpra\b|regulat\w*|\bdora\b|ai act|sm&cr|smcr|consumer duty|basel|\bgdpr\b",
    "cyber": r"cyber|information security|iso ?27001|\bnist\b",
    "automation": r"automat\w*|\brpa\b",
    "cert": r"\bcipp|\baigp\b|\bcams\b|\bcisa\b|\bcissp\b|\bcrisc\b|\bacca\b|\bcfa\b|\bica\b|\biapp\b|iso ?42001|\bfrm\b|\bprm\b|\bcia\b",
    "governance": r"governance|oversight|accountab\w*",
}
SKILL_REGEX = {name: re.compile(pattern, re.IGNORECASE) for name, pattern in SKILL_PATTERNS.items()}
_last_request_by_host = {}


class PageParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.hrefs = []
        self.scripts = []
        self._script = False
        self._script_attrs = {}
        self._script_buffer = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "a":
            href = attrs.get("href", "")
            if href:
                self.hrefs.append(href)
        elif tag == "script":
            self._script = True
            self._script_attrs = attrs
            self._script_buffer = []

    def handle_data(self, data):
        if self._script:
            self._script_buffer.append(data)

    def handle_endtag(self, tag):
        if tag == "script" and self._script:
            self.scripts.append((self._script_attrs, "".join(self._script_buffer)))
            self._script = False


class PlainText(HTMLParser):
    def __init__(self):
        super().__init__()
        self.skip = 0
        self.parts = []

    def handle_starttag(self, tag, attrs):
        if tag in {"script", "style", "nav", "footer", "header"}:
            self.skip += 1

    def handle_endtag(self, tag):
        if tag in {"script", "style", "nav", "footer", "header"} and self.skip:
            self.skip -= 1

    def handle_data(self, data):
        if not self.skip and data.strip():
            self.parts.append(data.strip())


class DescriptionBlock(HTMLParser):
    def __init__(self):
        super().__init__()
        self.depth = 0
        self.capturing = False
        self.parts = []
        self.title_parts = []
        self.title_depth = 0

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        classes = attrs.get("class", "").lower()
        ident = attrs.get("id", "").lower()
        if not self.capturing and (
            "job-description" in classes
            or "jobdescription" in classes
            or ident in {"job-description", "jobdescription"}
        ):
            self.capturing = True
            self.depth = 1
        elif self.capturing:
            self.depth += 1
        if tag == "h1" or "job-title" in classes:
            self.title_depth = 1
        elif self.title_depth:
            self.title_depth += 1

    def handle_endtag(self, tag):
        if self.capturing:
            self.depth -= 1
            if self.depth <= 0:
                self.capturing = False
        if self.title_depth:
            self.title_depth -= 1

    def handle_data(self, data):
        if self.capturing and data.strip():
            self.parts.append(data.strip())
        if self.title_depth and data.strip():
            self.title_parts.append(data.strip())


class SourceBlocked(RuntimeError):
    pass


def wait_for_host(url):
    host = urlsplit(url).netloc.lower()
    elapsed = time.monotonic() - _last_request_by_host.get(host, 0)
    if elapsed < DELAY_SECONDS:
        time.sleep(DELAY_SECONDS - elapsed)
    _last_request_by_host[host] = time.monotonic()


def fetch(url):
    wait_for_host(url)
    request = Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with urlopen(request, timeout=60) as response:
            return response.read(), response.geturl()
    except HTTPError as exc:
        if exc.code in (403, 429):
            raise SourceBlocked(f"Reed returned HTTP {exc.code}; no retry or bypass attempted.") from exc
        return None, None
    except (URLError, TimeoutError, OSError):
        return None, None


def query_slug(query):
    return re.sub(r"[^a-z0-9]+", "-", query.lower()).strip("-")


def get_cached_or_fetch(path, url, redact=False, cache=True):
    if cache and path.exists() and path.stat().st_size:
        body = path.read_bytes()
        if redact:
            path.write_bytes(redact_html(body))
        return body, url
    body, final_url = fetch(url)
    if body and cache:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(redact_html(body) if redact else body)
    return body, final_url


def job_links(search_html):
    parser = PageParser()
    parser.feed(search_html)
    found = []
    seen = set()
    for href in parser.hrefs:
        full_url = urljoin(BASE_URL, html.unescape(href))
        path = urlsplit(full_url).path.rstrip("/")
        match = re.fullmatch(r"/jobs/[^/]+/(\d+)", path, re.IGNORECASE)
        if match and match.group(1) not in seen:
            found.append((match.group(1), full_url))
            seen.add(match.group(1))
    return found


def walk_json(value):
    if isinstance(value, dict):
        yield value
        for nested in value.values():
            yield from walk_json(nested)
    elif isinstance(value, list):
        for nested in value:
            yield from walk_json(nested)


def json_objects(page_html):
    parser = PageParser()
    parser.feed(page_html)
    for attrs, source in parser.scripts:
        if not source.strip():
            continue
        try:
            value = json.loads(source)
        except (json.JSONDecodeError, TypeError):
            continue
        yield from walk_json(value)


def redact_html(body):
    text = body.decode("utf-8", "replace")
    employer_names = set()
    private_key = ROOT / "data" / "PRIVATE_bank_key.csv"
    if private_key.exists():
        with private_key.open(encoding="utf-8", newline="") as stream:
            employer_names.update(
                row["bank_name"].strip()
                for row in csv.DictReader(stream)
                if row.get("bank_name", "").strip()
            )
    for item in json_objects(text):
        for key in ("hiringOrganization", "employer", "company", "employerName", "companyName"):
            value = item.get(key)
            if isinstance(value, dict):
                value = value.get("name") or value.get("legalName")
            if isinstance(value, str) and len(value.strip()) >= 3:
                employer_names.add(value.strip())
    for name in sorted(employer_names, key=len, reverse=True):
        text = re.sub(re.escape(name), "[REDACTED EMPLOYER]", text, flags=re.IGNORECASE)
    return text.encode("utf-8")


def job_posting(page_html):
    for item in json_objects(page_html):
        kinds = item.get("@type", [])
        if isinstance(kinds, str):
            kinds = [kinds]
        if "JobPosting" in kinds:
            return item
    return {}


def description_text(markup):
    parser = PlainText()
    parser.feed(markup or "")
    return " ".join(parser.parts).strip()


def address_text(posting):
    locations = posting.get("jobLocation") or []
    if isinstance(locations, dict):
        locations = [locations]
    parts = []
    for location in locations:
        address = location.get("address", {}) if isinstance(location, dict) else {}
        if isinstance(address, list):
            address = address[0] if address else {}
        for key in ("addressLocality", "addressRegion"):
            value = address.get(key, "") if isinstance(address, dict) else ""
            if isinstance(value, dict):
                value = value.get("name", "")
            if value and value not in parts:
                parts.append(str(value).strip())
    return ", ".join(parts)


def numeric(value):
    if value in (None, ""):
        return None
    if isinstance(value, (int, float)):
        return float(value)
    cleaned = re.sub(r"[^0-9.\-]", "", str(value).replace(",", ""))
    try:
        return float(cleaned) if cleaned else None
    except ValueError:
        return None


def printable_number(value):
    if value is None:
        return ""
    return str(int(value)) if float(value).is_integer() else str(value)


def salary_data(posting, page_html):
    base = posting.get("baseSalary") or {}
    salary_value = base.get("value", {}) if isinstance(base, dict) else {}
    if isinstance(salary_value, list):
        salary_value = salary_value[0] if salary_value else {}
    minimum = numeric(salary_value.get("minValue")) if isinstance(salary_value, dict) else None
    maximum = numeric(salary_value.get("maxValue")) if isinstance(salary_value, dict) else None
    unit = str(salary_value.get("unitText", "") if isinstance(salary_value, dict) else "").strip()
    code = None
    type_name = ""
    matching = []
    if minimum is not None and maximum is not None:
        for item in json_objects(page_html):
            salary = item.get("jobSalary")
            if not isinstance(salary, dict):
                continue
            low, high = numeric(salary.get("from")), numeric(salary.get("to"))
            if low == minimum and high == maximum:
                matching.append(salary)
    if matching:
        details = matching[0].get("type", {})
        if isinstance(details, dict):
            code = details.get("id")
            type_name = str(details.get("name") or "").strip()

    annual_from = None
    annual_to = None
    unit_key = re.sub(r"[^a-z]", "", unit.casefold())
    name_key = re.sub(r"[^a-z]", "", type_name.casefold())
    annual_units = {"year", "yearly", "annual", "annum", "perannum", "peryear"}
    annual = unit_key in annual_units or name_key in annual_units or "perannum" in name_key
    if annual:
        annual_from, annual_to = minimum, maximum
    elif matching:
        item = matching[0]
        low = numeric(item.get("fromPerAnnum"))
        high = numeric(item.get("toPerAnnum"))
        if low and high and low > 0 and high > 0:
            annual_from, annual_to = low, high
    annual_mid = (annual_from + annual_to) / 2 if annual_from is not None and annual_to is not None else None
    return printable_number(minimum), printable_number(maximum), printable_number(annual_mid), unit, code, type_name


def extract_ad(job_id, page_html, query):
    posting = job_posting(page_html)
    fallback = DescriptionBlock()
    fallback.feed(page_html)
    title = str(posting.get("title") or " ".join(fallback.title_parts)).strip()
    description = description_text(posting.get("description", ""))
    if not description:
        description = " ".join(fallback.parts).strip()
    if not title or not description:
        return None
    date_posted = str(posting.get("datePosted", "") or "").strip()
    location = address_text(posting)
    salary_from, salary_to, annual_mid, unit, salary_code, salary_name = salary_data(posting, page_html)
    role_type = "AI" if ROLE_AI.search(title) else "Traditional"
    result = {
        "query": query,
        "role_type": role_type,
        "date_posted": date_posted,
        "location_region": location,
        "salary_from": salary_from,
        "salary_to": salary_to,
        "salary_annual_mid": annual_mid,
        "title": title,
        "word_count": len(description.split()),
        "_description": description,
        "_salary_unit": unit,
        "_salary_code": salary_code,
        "_salary_name": salary_name,
        "_job_id": job_id,
    }
    for name, pattern in SKILL_REGEX.items():
        result[name] = int(bool(pattern.search(description)))
    return result


def is_financial_services(description):
    return bool(FINANCIAL.search(description))


def iter_round_robin(by_query):
    cursors = {query: 0 for query in by_query}
    while True:
        progressed = False
        for query in by_query:
            index = cursors[query]
            if index < len(by_query[query]):
                cursors[query] += 1
                progressed = True
                yield by_query[query][index]
        if not progressed:
            return


def collect_search_results(queries, page_numbers):
    found = {query: [] for query in queries}
    seen_ids = set()
    blocked = False
    for page_number in page_numbers:
        for query in queries:
            path = RAW / f"search_{query_slug(query)}_{page_number}.html"
            url = f"{BASE_URL}/jobs/{query_slug(query)}-jobs?page={page_number}"
            try:
                body, _ = get_cached_or_fetch(path, url, cache=False)
            except SourceBlocked:
                blocked = True
                return found, blocked
            if not body:
                continue
            for job_id, detail_url in job_links(body.decode("utf-8", "replace")):
                if job_id not in seen_ids:
                    seen_ids.add(job_id)
                    found[query].append((job_id, detail_url))
    return found, blocked


def main():
    RAW.mkdir(parents=True, exist_ok=True)
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    if OUTPUT.exists():
        with OUTPUT.open(encoding="utf-8", newline="") as stream:
            existing_rows = list(csv.DictReader(stream))
    else:
        existing_rows = []
    queries = ADDITIONAL_QUERIES if existing_rows else QUERIES + ADDITIONAL_QUERIES
    by_query, blocked = collect_search_results(queries, [1, 2])
    detail_candidates = sum(len(items) for items in by_query.values())

    kept = []
    excluded = 0
    uncoded = 0
    examined = set()
    salary_mapping = defaultdict(set)
    role_counts = defaultdict(int)
    prior_ids = set()
    if existing_rows:
        for path in RAW.glob("*.html"):
            match = re.fullmatch(r"(?:reed_)?(\d+)\.html", path.name)
            if match:
                prior_ids.add(match.group(1))

    def target_met():
        total_ai = sum(row["role_type"] == "AI" for row in existing_rows) + role_counts["AI"]
        total_kept = len(existing_rows) + len(kept)
        return total_kept >= TARGET_KEPT and total_ai >= TARGET_PER_ROLE

    def process_candidates(candidate_map):
        nonlocal blocked, excluded, uncoded
        for job_id, detail_url in iter_round_robin(candidate_map):
            if job_id in examined or job_id in prior_ids:
                continue
            examined.add(job_id)
            cached = RAW / f"{job_id}.html"
            if not cached.exists():
                cached = RAW / f"reed_{job_id}.html"
            try:
                body, _ = get_cached_or_fetch(cached, detail_url, redact=True)
            except SourceBlocked:
                blocked = True
                break
            if not body:
                uncoded += 1
                continue
            query = next(q for q, items in candidate_map.items() if any(item[0] == job_id for item in items))
            ad = extract_ad(job_id, body.decode("utf-8", "replace"), query)
            if ad is None:
                uncoded += 1
                continue
            if ad["_salary_code"] is not None:
                salary_mapping[str(ad["_salary_code"])].add(f"{ad['_salary_name']}|{ad['_salary_unit']}")
            if not is_financial_services(ad.pop("_description")):
                excluded += 1
                continue
            role_counts[ad["role_type"]] += 1
            kept.append(ad)
            if target_met():
                break

    process_candidates(by_query)

    page3_candidates = 0
    if not target_met() and not blocked:
        page3, blocked_page3 = collect_search_results(queries, [3])
        blocked = blocked or blocked_page3
        page3_candidates = sum(len(items) for items in page3.values())
        process_candidates(page3)

    combined = existing_rows + kept
    with OUTPUT.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(existing_rows)
        for index, ad in enumerate(kept, len(existing_rows) + 1):
            writer.writerow(
                {
                    "ad_id": f"AD{index:03d}",
                    **{field: ad.get(field, "") for field in FIELDS if field != "ad_id"},
                }
            )
    total_roles = defaultdict(int)
    for ad in combined:
        total_roles[ad["role_type"]] += 1
    print(
        f"New detail pages opened: {len(examined)}; appended kept ads: {len(kept)}; "
        f"excluded: {excluded}; uncoded/unavailable: {uncoded}."
    )
    print(f"New role counts: AI={role_counts['AI']}; Traditional={role_counts['Traditional']}.")
    print(f"Total kept ads: {len(combined)}; total role counts: {dict(total_roles)}.")
    print(
        f"Search candidates pages 1-2={detail_candidates}; page 3={page3_candidates}; "
        f"HTTP access blocked: {blocked}."
    )
    print(
        f"Annual salary rows appended: {sum(bool(ad['salary_annual_mid']) for ad in kept)}; "
        f"output: {OUTPUT}"
    )
    print(f"Salary type observations: {dict(salary_mapping)}")
    if not target_met():
        print("The target count/AI-role minimum was not met after pages 1-3; no later pages were requested.")
    return
    for job_id, detail_url in iter_round_robin(by_query):
        if job_id in examined:
            continue
        examined.add(job_id)
        cached = RAW / f"{job_id}.html"
        if not cached.exists():
            cached = RAW / f"reed_{job_id}.html"
        try:
            body, _ = get_cached_or_fetch(cached, detail_url, redact=True)
        except SourceBlocked:
            blocked = True
            break
        if not body:
            uncoded += 1
            continue
        query = next(q for q, items in by_query.items() if any(item[0] == job_id for item in items))
        ad = extract_ad(job_id, body.decode("utf-8", "replace"), query)
        if ad is None:
            uncoded += 1
            continue
        if ad["_salary_code"] is not None:
            salary_mapping[str(ad["_salary_code"])].add(f"{ad['_salary_name']}|{ad['_salary_unit']}")
        if not is_financial_services(ad.pop("_description")):
            excluded += 1
            continue
        role_counts[ad["role_type"]] += 1
        kept.append(ad)
        if len(kept) >= TARGET_KEPT and all(role_counts[role] >= TARGET_PER_ROLE for role in ("AI", "Traditional")):
            break

    if len(kept) < TARGET_KEPT or any(role_counts[role] < TARGET_PER_ROLE for role in ("AI", "Traditional")):
        page3, blocked_page3 = collect_search_results(QUERIES, [3])
        blocked = blocked or blocked_page3
        page3_candidates = sum(len(items) for items in page3.values())
        for query, items in page3.items():
            existing = {job_id for job_id, _ in by_query[query]}
            by_query[query].extend(item for item in items if item[0] not in existing)
        for job_id, detail_url in iter_round_robin(page3):
            if job_id in examined:
                continue
            examined.add(job_id)
            cached = RAW / f"{job_id}.html"
            if not cached.exists():
                cached = RAW / f"reed_{job_id}.html"
            try:
                body, _ = get_cached_or_fetch(cached, detail_url, redact=True)
            except SourceBlocked:
                blocked = True
                break
            if not body:
                uncoded += 1
                continue
            query = next(q for q, items in page3.items() if any(item[0] == job_id for item in items))
            ad = extract_ad(job_id, body.decode("utf-8", "replace"), query)
            if ad is None:
                uncoded += 1
                continue
            if ad["_salary_code"] is not None:
                salary_mapping[str(ad["_salary_code"])].add(f"{ad['_salary_name']}|{ad['_salary_unit']}")
            if not is_financial_services(ad.pop("_description")):
                excluded += 1
                continue
            role_counts[ad["role_type"]] += 1
            kept.append(ad)
            if len(kept) >= TARGET_KEPT and all(role_counts[role] >= TARGET_PER_ROLE for role in ("AI", "Traditional")):
                break
    else:
        page3_candidates = 0

    with OUTPUT.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=FIELDS)
        writer.writeheader()
        for index, ad in enumerate(kept, 1):
            writer.writerow(
                {
                    "ad_id": f"AD{index:03d}",
                    **{field: ad.get(field, "") for field in FIELDS if field != "ad_id"},
                }
            )
    print(f"Detail pages opened: {len(examined)}; kept: {len(kept)}; excluded: {excluded}; uncoded/unavailable: {uncoded}.")
    print(f"Role counts: AI={role_counts['AI']}; Traditional={role_counts['Traditional']}.")
    print(
        f"Unique candidates: pages 1-2={detail_candidates}; page 3={page3_candidates}; "
        f"HTTP access blocked: {blocked}."
    )
    print(f"Annual salary rows: {sum(bool(ad['salary_annual_mid']) for ad in kept)}; output: {OUTPUT}")
    print(f"Salary type observations: {dict(salary_mapping)}")
    if len(kept) < TARGET_KEPT or any(role_counts[role] < TARGET_PER_ROLE for role in ("AI", "Traditional")):
        print("The target count was not met from pages 1-3; no pages beyond 3 were requested.")


if __name__ == "__main__":
    main()
