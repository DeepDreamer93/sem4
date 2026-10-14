#!/usr/bin/env python3
"""Collect verbatim survey proportions from the specified local and official sources."""

import csv
import re
import shutil
import subprocess
import time
from html.parser import HTMLParser
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


ROOT = Path(__file__).resolve().parents[1]
RESEARCH = Path("/home/ubuntu/thesis/research")
RAW = ROOT / "raw" / "d4"
OUTPUT = ROOT / "data" / "D4_survey_props.csv"
URL_2024 = "https://www.bankofengland.co.uk/report/2024/artificial-intelligence-in-uk-financial-services-2024"
URL_2022 = "https://www.bankofengland.co.uk/report/2022/machine-learning-in-uk-financial-services"
HTML_2024 = RAW / "boe_fca_ai_2024.html"
HTML_2022 = RAW / "boe_fca_ml_2022.html"
FIELDS = ["source", "year", "statement", "proportion", "n_respondents", "n_quote", "page"]
DELAY_SECONDS = 3.05
USER_AGENT = "MBA-thesis-public-dataset/1.0"


class VisibleText(HTMLParser):
    def __init__(self):
        super().__init__()
        self.skip_depth = 0
        self.parts = []

    def handle_starttag(self, tag, attrs):
        if tag in {"script", "style", "nav", "footer"}:
            self.skip_depth += 1

    def handle_endtag(self, tag):
        if tag in {"script", "style", "nav", "footer"} and self.skip_depth:
            self.skip_depth -= 1

    def handle_data(self, data):
        if not self.skip_depth and data.strip():
            self.parts.append(data.strip())


def normalized(text):
    text = re.sub(r"(?<=\w)-\s*(?=\w)", "", text)
    text = re.sub(r"\s+([.,;:!?])", r"\1", text)
    return re.sub(r"\s+", " ", text).strip().casefold()


def fetch_html_if_missing(path, url):
    if path.exists() and path.stat().st_size:
        return
    host = "www.bankofengland.co.uk"
    time.sleep(DELAY_SECONDS)
    request = Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with urlopen(request, timeout=60) as response:
            content = response.read()
    except HTTPError as exc:
        if exc.code in (403, 429):
            raise RuntimeError(f"Source access returned HTTP {exc.code}; no retry or bypass attempted.") from exc
        raise
    except (URLError, TimeoutError, OSError) as exc:
        raise RuntimeError("Official survey source could not be retrieved.") from exc
    if not content:
        raise RuntimeError(f"Empty response from {host}.")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(content)


def html_text(path):
    parser = VisibleText()
    parser.feed(path.read_text(encoding="utf-8", errors="replace"))
    return " ".join(parser.parts)


def pdf_text(path):
    pdftotext = shutil.which("pdftotext")
    if not pdftotext:
        raise RuntimeError("pdftotext is required but was not found.")
    result = subprocess.run(
        [pdftotext, "-layout", "-enc", "UTF-8", str(path), "-"],
        check=False,
        text=True,
        capture_output=True,
        timeout=180,
    )
    if result.returncode:
        raise RuntimeError(f"pdftotext failed for {path.name}.")
    return result.stdout


def require_statement(corpus, statement, label):
    if normalized(statement) not in normalized(corpus):
        raise RuntimeError(f"Verbatim statement no longer matches the source: {label}.")


def row(source, year, statement, proportion, n, n_quote, page):
    return {
        "source": source,
        "year": year,
        "statement": statement,
        "proportion": f"{proportion:.2f}",
        "n_respondents": "" if n is None else n,
        "n_quote": n_quote,
        "page": page,
    }


def main():
    RAW.mkdir(parents=True, exist_ok=True)
    fetch_html_if_missing(HTML_2024, URL_2024)
    fetch_html_if_missing(HTML_2022, URL_2022)
    boe24 = html_text(HTML_2024)
    boe22 = html_text(HTML_2022)
    iia = (RESEARCH / "iia.txt").read_text(encoding="utf-8", errors="replace")
    tr_text = RESEARCH / "tr.txt"
    tr = (
        tr_text.read_text(encoding="utf-8", errors="replace")
        if tr_text.exists()
        else pdf_text(RESEARCH / "tr.pdf")
    )

    boe24_n = "The survey received 118 responses with the number of respondents from each sector shown in the chart below."
    boe22_n = "In total, 168 firms received the questionnaire and 71 submitted responses (42% overall response rate)."
    iia_n = "6,506 participants in a global survey (the map below presents the percentage of survey respondents per region):"
    tr_n = (
        "The data was gathered in February and March 2025 from 2,275 responses to a survey sent to professionals "
        "in the legal, risk, compliance, tax, accounting, audit, and trade industries, both among outside firms and "
        "in-house corporate functions."
    )

    use24 = (
        "Overall, 75% of firms that responded to the survey said they are already using AI with a further 10% "
        "planning to use AI over the next three years."
    )
    use22_comparison = (
        "This is an increase on the figures from our 2022 survey which showed that 58% of firms were using AI "
        "and a further 14% were planning to do so."
    )
    use22 = "Overall, 72% of firms that responded to the survey reported using or developing ML applications."
    understanding = (
        "Of the firms using or planning to use AI over the next three years, 46% reported having only ‘partial "
        "understanding’ of the AI technologies they use versus 34% of firms that said they have ‘complete "
        "understanding’."
    )
    talent = (
        "Insufficient talent/access to skills was considered by 25% of firms to be a large constraint, by 32% "
        "to be medium, and by 24% to be a small constraint."
    )
    accountable = "84% of firms reported having an accountable person for their AI framework."
    iia_skills = (
        "Further, 96% agree that experienced internal auditors will need to increase their technology skills to "
        "remain relevant and 81% agree that entry-level internal auditors will require an elevated skill set to "
        "be successful (refer to Figure 2)."
    )
    tr_gap = "46% report skills gaps within teams"
    tr_ai = (
        "For example, while 80% of respondents said they see AI as having a high or transformative impact on "
        "their profession over the next five years, only about one-third of professionals (38%) said they expect "
        "that change to happen this year — and 3 out of 10 said their organizations are moving too slowly in "
        "AI adoption."
    )

    for statement, label in [
        (use24, "2024 AI usage"),
        (use22_comparison, "2022 comparable AI usage"),
        (understanding, "2024 AI understanding"),
        (talent, "2024 talent constraint"),
        (accountable, "2024 accountable person"),
    ]:
        require_statement(boe24, statement, label)
    require_statement(boe22, use22, "2022 ML usage")
    require_statement(iia, iia_skills, "IIA skills")
    require_statement(tr, tr_ai, "Thomson Reuters AI impact")
    tr_skill_page = tr.split("\f")[23]
    if "46%" not in tr_skill_page or "report skills gaps within teams" not in normalized(tr_skill_page):
        raise RuntimeError("The 46% Thomson Reuters chart label was not found on printed page 24.")
    if "2,275 responses to a survey" not in normalized(tr):
        raise RuntimeError("The Thomson Reuters sample-size quote was not found.")

    rows = [
        row("BoE/FCA AI survey 2024", 2024, use24, 0.75, 118, boe24_n, ""),
        row("BoE/FCA AI survey 2024 (2022 comparison)", 2022, use22_comparison, 0.58, 71, boe22_n, ""),
        row("BoE/FCA ML survey 2022", 2022, use22, 0.72, 71, boe22_n, ""),
        row("BoE/FCA AI survey 2024", 2024, understanding, 0.46, None, "", ""),
        row("BoE/FCA AI survey 2024", 2024, understanding, 0.34, None, "", ""),
        row("BoE/FCA AI survey 2024", 2024, talent, 0.25, 118, boe24_n, ""),
        row("BoE/FCA AI survey 2024", 2024, talent, 0.32, 118, boe24_n, ""),
        row("BoE/FCA AI survey 2024", 2024, accountable, 0.84, None, "", ""),
        row("IIA Vision 2035", 2025, iia_skills, 0.96, 6506, iia_n, "vi"),
        row("IIA Vision 2035", 2025, iia_skills, 0.81, 6506, iia_n, "vi"),
        row(
            "Thomson Reuters Future of Professionals 2025",
            2025,
            tr_gap,
            0.46,
            2275,
            tr_n,
            "24",
        ),
        row(
            "Thomson Reuters Future of Professionals 2025",
            2025,
            tr_ai,
            0.80,
            2275,
            tr_n,
            "7",
        ),
    ]
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    with OUTPUT.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(rows)
    print(f"Rows written: {len(rows)}; rows with reported n: {sum(bool(item['n_respondents']) for item in rows)}.")
    print(f"Rows with missing item denominator: {sum(not bool(item['n_respondents']) for item in rows)}.")
    print(f"Output: {OUTPUT}")


if __name__ == "__main__":
    main()
