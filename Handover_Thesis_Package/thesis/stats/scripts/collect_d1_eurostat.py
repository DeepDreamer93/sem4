#!/usr/bin/env python3
"""Collect the specified annual EU27 Eurostat country panel."""

import csv
import json
import time
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "data" / "D1_eurostat.csv"
API = "https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data"
USER_AGENT = "MBA-thesis-public-dataset/1.0"
DELAY_SECONDS = 3.05
GEOS = [
    "AT", "BE", "BG", "CY", "CZ", "DE", "DK", "EE", "EL", "ES", "FI",
    "FR", "HR", "HU", "IE", "IT", "LT", "LU", "LV", "MT", "NL", "PL",
    "PT", "RO", "SE", "SI", "SK",
]
AGGREGATE = "EU27_2020"
EXPECTED_DIMS = {
    "isoc_eb_ai": {"freq", "size_emp", "nace_r2", "indic_is", "unit", "geo", "time"},
    "isoc_sks_itspt": {"freq", "unit", "geo", "time"},
}
FIELDS = [
    "geo",
    "year",
    "ai_ge10",
    "ai_ge250",
    "ict_spec_pc_emp",
    "is_aggregate",
    "flag_notes",
]
_last_request = 0.0


def fetch_json(dataset, params):
    global _last_request
    delay = DELAY_SECONDS - (time.monotonic() - _last_request)
    if delay > 0:
        time.sleep(delay)
    url = f"{API}/{dataset}?{urlencode(params, doseq=True)}"
    request = Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with urlopen(request, timeout=90) as response:
            payload = json.load(response)
    except HTTPError as exc:
        raise RuntimeError(f"Eurostat returned HTTP {exc.code} for {dataset}.") from exc
    except (URLError, TimeoutError, OSError) as exc:
        raise RuntimeError(f"Eurostat request failed for {dataset}: {exc}") from exc
    _last_request = time.monotonic()
    return payload


def category_index(payload, dimension):
    raw = payload["dimension"][dimension]["category"]["index"]
    if isinstance(raw, dict):
        return {str(code): int(index) for code, index in raw.items()}
    return {str(code): index for index, code in enumerate(raw)}


def validate_schema(payload, dataset):
    dimensions = set(payload.get("id", []))
    if dimensions != EXPECTED_DIMS[dataset]:
        raise RuntimeError(
            f"Unexpected {dataset} dimensions: {sorted(dimensions)}; "
            f"expected {sorted(EXPECTED_DIMS[dataset])}."
        )
    freq = category_index(payload, "freq")
    if set(freq) != {"A"}:
        raise RuntimeError(f"Unexpected {dataset} freq values: {sorted(freq)}.")


def flat_index(payload, selections):
    dimensions = payload["id"]
    sizes = payload["size"]
    offset = 0
    for dimension, size in zip(dimensions, sizes):
        index = category_index(payload, dimension).get(selections[dimension])
        if index is None:
            return None
        offset = offset * size + index
    return offset


def cell(payload, selections):
    offset = flat_index(payload, selections)
    if offset is None:
        return "", ""
    values = payload.get("value", [])
    if isinstance(values, dict):
        value = values.get(str(offset), "")
    else:
        value = values[offset] if offset < len(values) else ""
    status = payload.get("status", {})
    if isinstance(status, dict):
        flag = status.get(str(offset), "")
    else:
        flag = status[offset] if offset < len(status) else ""
    return "" if value is None else value, "" if flag is None else str(flag)


def main():
    geo_params = GEOS + [AGGREGATE]
    ai = fetch_json(
        "isoc_eb_ai",
        [
            ("lang", "en"),
            ("freq", "A"),
            ("unit", "PC_ENT"),
            ("indic_is", "E_AI_TANY"),
            ("nace_r2", "C10-S951_X_K"),
            ("size_emp", "GE10"),
            ("size_emp", "GE250"),
            *[("geo", geo) for geo in geo_params],
        ],
    )
    validate_schema(ai, "isoc_eb_ai")
    ict = fetch_json(
        "isoc_sks_itspt",
        [
            ("lang", "en"),
            ("freq", "A"),
            ("unit", "PC_EMP"),
            *[("geo", geo) for geo in geo_params],
        ],
    )
    validate_schema(ict, "isoc_sks_itspt")

    years = sorted(category_index(ai, "time"), key=int)
    rows = []
    for geo in GEOS + [AGGREGATE]:
        aggregate = int(geo == AGGREGATE)
        for year in years:
            common = {"freq": "A", "geo": geo, "time": year}
            ai_ge10, flag_ge10 = cell(
                ai,
                {
                    **common,
                    "size_emp": "GE10",
                    "nace_r2": "C10-S951_X_K",
                    "indic_is": "E_AI_TANY",
                    "unit": "PC_ENT",
                },
            )
            ai_ge250, flag_ge250 = cell(
                ai,
                {
                    **common,
                    "size_emp": "GE250",
                    "nace_r2": "C10-S951_X_K",
                    "indic_is": "E_AI_TANY",
                    "unit": "PC_ENT",
                },
            )
            ict_value, flag_ict = cell(
                ict,
                {**common, "unit": "PC_EMP"},
            )
            flags = []
            for field, flag in (
                ("ai_ge10", flag_ge10),
                ("ai_ge250", flag_ge250),
                ("ict_spec_pc_emp", flag_ict),
            ):
                if flag:
                    flags.append(f"{field}={flag}")
            rows.append(
                {
                    "geo": geo,
                    "year": year,
                    "ai_ge10": ai_ge10,
                    "ai_ge250": ai_ge250,
                    "ict_spec_pc_emp": ict_value,
                    "is_aggregate": aggregate,
                    "flag_notes": "; ".join(flags),
                }
            )

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    with OUTPUT.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(rows)
    print(f"Rows written: {len(rows)}; geos: {len(geo_params)}; years: {', '.join(years)}.")
    print(f"Aggregate rows: {sum(row['is_aggregate'] for row in rows)}; output: {OUTPUT}")


if __name__ == "__main__":
    main()
