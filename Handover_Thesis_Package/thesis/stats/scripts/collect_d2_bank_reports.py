#!/usr/bin/env python3
"""Collect and code bank annual reports whose official IR URLs are in the private key."""

import csv
import re
import shutil
import subprocess
import time
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urlsplit
from urllib.request import Request, urlopen


ROOT = Path(__file__).resolve().parents[1]
SPEC = ROOT / "DATA_SPEC.md"
KEY = ROOT / "data" / "PRIVATE_bank_key.csv"
OUTPUT = ROOT / "data" / "D2_bank_reports.csv"
RAW = ROOT / "raw" / "d2"
FIELDS = [
    "bank_code",
    "region",
    "fy",
    "total_words",
    "ai",
    "reskill",
    "aigov",
    "reg",
    "aigov_body",
    "ai_d",
    "reskill_d",
    "aigov_d",
    "reg_d",
]
DELAY_SECONDS = 3.05
USER_AGENT = (
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/131.0 Safari/537.36"
)

PATTERNS = {
    "ai": r"\bartificial intelligence\b|\bmachine learning\b|\bgenerative ai\b|\bgen ?ai\b|\blarge language models?\b|\bllms?\b|\bai\b",
    "reskill": r"\bre-?skill\w*|\bup-?skill\w*|\bretrain\w*|\bdigital skills?\b|\bai literacy\b|\bdata literacy\b|\bskills? (gap|development)\b",
    "aigov": r"\bai governance\b|\bresponsible ai\b|\bai ethics\b|\bethical ai\b|\bhuman oversight\b|\bhuman[- ]in[- ]the[- ]loop\b|\bexplainab\w*|\bmodel risk\b",
    "reg": r"\bai act\b|\bartificial intelligence act\b|\bdora\b|\bdigital operational resilience\b|\bss1/23\b",
}
AIGOV_BODY = re.compile(
    r"chief (ai|artificial intelligence|data( and| &) ai|data) officer"
    r"|ai (council|committee|board|office|centre of excellence|center of excellence)"
    r"|responsible ai (office|council|committee|lead|team|framework)",
    re.IGNORECASE,
)
COMPILED = {name: re.compile(pattern, re.IGNORECASE) for name, pattern in PATTERNS.items()}
_last_request_by_host = {}


def frame_regions():
    text = SPEC.read_text(encoding="utf-8")
    section = text.split("Frame (fixed list, 29 groups):", 1)[1].split(
        "- Use the main Annual Report", 1
    )[0]
    regions = {}
    for match in re.finditer(r"\b(UK|EU):\s*(.*?)(?=\b(?:UK|EU):|$)", section, re.S):
        region, body = match.groups()
        for name in body.split(","):
            name = name.strip().rstrip(".")
            if name:
                regions[name] = region
    if len(regions) != 29:
        raise RuntimeError("The fixed frame in DATA_SPEC.md no longer parses as 29 groups.")
    return regions


def load_key():
    with KEY.open(encoding="utf-8-sig", newline="") as stream:
        rows = list(csv.DictReader(stream))
    if len(rows) != 58 or not {"bank_code", "bank_name", "fy", "doc_title", "url"} <= set(rows[0]):
        raise RuntimeError("PRIVATE_bank_key.csv must contain 58 rows and the specified columns.")
    for row in rows:
        row.setdefault("reason", "")
    return rows


def wait_for_host(url):
    host = urlsplit(url).netloc.lower()
    now = time.monotonic()
    remaining = DELAY_SECONDS - (now - _last_request_by_host.get(host, 0))
    if remaining > 0:
        time.sleep(remaining)
    _last_request_by_host[host] = time.monotonic()


def download_pdf(url, destination):
    if destination.exists() and destination.stat().st_size:
        return True
    wait_for_host(url)
    request = Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with urlopen(request, timeout=90) as response:
            payload = response.read()
    except HTTPError as exc:
        if exc.code in (403, 429):
            return False
        return False
    except (URLError, TimeoutError, OSError):
        return False
    if not payload.startswith(b"%PDF-"):
        return False
    destination.write_bytes(payload)
    return True


def pdf_title(pdf_path):
    pdfinfo = shutil.which("pdfinfo")
    if not pdfinfo:
        return ""
    result = subprocess.run(
        [pdfinfo, str(pdf_path)],
        check=False,
        text=True,
        capture_output=True,
        timeout=30,
    )
    if result.returncode:
        return ""
    for line in result.stdout.splitlines():
        if line.startswith("Title:"):
            return line.partition(":")[2].strip()
    return ""


def extract_text(pdf_path, text_path):
    pdftotext = shutil.which("pdftotext")
    if not pdftotext:
        raise RuntimeError("pdftotext is required but was not found.")
    result = subprocess.run(
        [pdftotext, "-enc", "UTF-8", str(pdf_path), str(text_path)],
        check=False,
        text=True,
        capture_output=True,
        timeout=180,
    )
    if result.returncode:
        text_path.unlink(missing_ok=True)
        return None
    return text_path.read_text(encoding="utf-8", errors="replace")


def count_matches(text, pattern):
    return len(list(pattern.finditer(text)))


def main():
    ROOT.joinpath("data").mkdir(exist_ok=True)
    RAW.mkdir(parents=True, exist_ok=True)
    regions = frame_regions()
    key_rows = load_key()
    results = []
    for item in key_rows:
        code = item["bank_code"]
        fy = int(item["fy"])
        region = regions.get(item["bank_name"], "")
        pdf_path = RAW / f"{code}_FY{fy}.pdf"
        text_path = RAW / f"{code}_FY{fy}.txt"
        text = None
        source_url = item["url"].strip()
        if source_url and download_pdf(source_url, pdf_path):
            text = extract_text(pdf_path, text_path)
            if text and not item["doc_title"]:
                item["doc_title"] = pdf_title(pdf_path)
            if text is not None:
                item["reason"] = ""
        elif not source_url:
            item["reason"] = item.get("reason") or "not yet searched"
        row = {
            "bank_code": code,
            "region": region,
            "fy": fy,
            "total_words": "",
            "ai": "",
            "reskill": "",
            "aigov": "",
            "reg": "",
            "aigov_body": "",
            "ai_d": "",
            "reskill_d": "",
            "aigov_d": "",
            "reg_d": "",
        }
        if text is not None:
            lowered = text.lower()
            total_words = len(lowered.split())
            counts = {name: count_matches(lowered, pattern) for name, pattern in COMPILED.items()}
            row["total_words"] = total_words
            row.update(counts)
            row["aigov_body"] = int(bool(AIGOV_BODY.search(lowered)))
            for name in counts:
                row[f"{name}_d"] = round(counts[name] / total_words * 10000, 4) if total_words else ""
        results.append(row)

    with KEY.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(
            stream,
            fieldnames=["bank_code", "bank_name", "fy", "doc_title", "url", "reason"],
        )
        writer.writeheader()
        writer.writerows(key_rows)
    with OUTPUT.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(results)
    coded = sum(bool(row["total_words"]) for row in results)
    print(f"Rows written: {len(results)}; coded reports: {coded}; missing reports: {len(results) - coded}.")
    print(f"Output: {OUTPUT}")
    print("Missing rows are retained with blank report metrics; no counts or densities are imputed.")


if __name__ == "__main__":
    main()
