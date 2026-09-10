import re
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

import requests
from bs4 import BeautifulSoup

IBJA_URL = "https://ibjarates.com/"
INDEX_PATH = Path("index.html")

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0 Safari/537.36"
    ),
    "Accept-Language": "en-US,en;q=0.9",
}

REQUIRED = ("gold999", "gold916", "gold750", "silver999")
ROW_NAMES = {
    "Gold 999": "gold999",
    "Gold 916": "gold916",
    "Gold 750": "gold750",
    "Silver 999": "silver999",
}


def fetch_soup() -> BeautifulSoup:
    response = requests.get(IBJA_URL, headers=HEADERS, timeout=30)
    response.raise_for_status()
    return BeautifulSoup(response.text, "html.parser")


def parse_number(text: str) -> int | None:
    match = re.search(r"\d[\d,]*", text or "")
    if not match:
        return None
    return int(match.group(0).replace(",", ""))


def current_rates_from_tables(soup: BeautifulSoup):
    rows = {}

    for tr in soup.find_all("tr"):
        cells = [c.get_text(" ", strip=True) for c in tr.find_all(["th", "td"])]
        if not cells:
            continue

        label = re.sub(r"\s+", " ", cells[0]).strip()
        key = ROW_NAMES.get(label)
        if not key:
            continue

        values = [parse_number(cell) for cell in cells[1:]]
        values = [value for value in values if value is not None]
        if values:
            rows[key] = values[:2]

    if not all(key in rows for key in REQUIRED):
        return None

    # Prefer IBJA closing (PM) rates only when PM is available for every card.
    if all(len(rows[key]) >= 2 for key in REQUIRED):
        values = {key: rows[key][1] for key in REQUIRED}
        period = "PM"
    elif all(len(rows[key]) >= 1 for key in REQUIRED):
        values = {key: rows[key][0] for key in REQUIRED}
        period = "AM"
    else:
        return None

    # Guard against accidentally scraping the small per-gram summary numbers.
    if values["gold999"] < 50000 or values["silver999"] < 50000:
        return None

    today = datetime.now(ZoneInfo("Asia/Kolkata"))
    return values, today, period


def latest_historical_rates(soup: BeautifulSoup):
    text = " ".join(soup.stripped_strings)
    pattern = re.compile(
        r"(\d{2}/\d{2}/\d{4})\s+"
        r"([\d,]{5,8})\s+([\d,]{5,8})\s+([\d,]{5,8})\s+"
        r"([\d,]{5,8})\s+([\d,]{5,8})\s+([\d,]{5,8})\s+([\d,]{5,8})"
    )

    records = []
    for match in pattern.finditer(text):
        date = datetime.strptime(match.group(1), "%d/%m/%Y")
        numbers = [int(match.group(i).replace(",", "")) for i in range(2, 9)]
        records.append((date, numbers))

    if not records:
        raise RuntimeError("Could not parse current or historical IBJA rates")

    latest_date = max(date for date, _ in records)
    same_day = [numbers for date, numbers in records if date == latest_date]

    # IBJA's historical area lists AM rows first and PM rows second.
    # Therefore the last row for the latest date is the closing rate when present.
    numbers = same_day[-1]
    period = "PM" if len(same_day) > 1 else "AM"

    values = {
        "gold999": numbers[0],
        "gold916": numbers[2],
        "gold750": numbers[3],
        "silver999": numbers[5],
    }
    return values, latest_date, period


def get_ibja_rates(soup: BeautifulSoup):
    current = current_rates_from_tables(soup)
    if current:
        return current
    return latest_historical_rates(soup)


def indian_number(value: int) -> str:
    s = str(int(value))
    if len(s) <= 3:
        return s

    last3 = s[-3:]
    prefix = s[:-3]
    groups = []
    while prefix:
        groups.append(prefix[-2:])
        prefix = prefix[:-2]
    return ",".join(reversed(groups)) + "," + last3


def rupees(value: int) -> str:
    return f"₹{indian_number(value)}"


def per_gram(value: int, divisor: int) -> int:
    return int((value / divisor) + 0.5)


def replace_once(html: str, pattern: str, replacement: str, label: str) -> str:
    updated, count = re.subn(pattern, replacement, html, count=1)
    if count != 1:
        raise RuntimeError(f"Could not update {label} in index.html")
    return updated


def update_index(values, rate_date: datetime, period: str) -> None:
    html = INDEX_PATH.read_text(encoding="utf-8")

    gold999 = values["gold999"]
    gold916 = values["gold916"]
    gold750 = values["gold750"]
    silver999 = values["silver999"]

    g999_gram = per_gram(gold999, 10)
    g916_gram = per_gram(gold916, 10)
    g750_gram = per_gram(gold750, 10)
    silver_gram = per_gram(silver999, 1000)

    # Keep the compact top bar in sync with the same IBJA benchmark data.
    top_pattern = re.compile(
        r"(?:Today's Rate|Delhi Rate|IBJA Rate):\s*"
        r"<strong>Gold 22K ₹[^<]+</strong>\s*"
        r"&nbsp;•&nbsp;\s*"
        r"<strong>Silver ₹[^<]+</strong>"
    )
    top_replacement = (
        f"IBJA Rate: <strong>Gold 22K {rupees(g916_gram)}/g</strong> "
        f"&nbsp;•&nbsp; <strong>Silver {rupees(silver_gram)}/g</strong>"
    )
    html, top_count = top_pattern.subn(top_replacement, html, count=1)
    if top_count != 1:
        raise RuntimeError("Could not locate the top rate block in index.html")

    # The larger rate panel may be absent during the first migration run.
    if 'id="ibjaRates"' in html:
        replacements = {
            "ibja-rate-date": rate_date.strftime("%d %b %Y"),
            "ibja-gold999-main": rupees(gold999),
            "ibja-gold999-gram": rupees(g999_gram),
            "ibja-gold916-main": rupees(gold916),
            "ibja-gold916-gram": rupees(g916_gram),
            "ibja-gold750-main": rupees(gold750),
            "ibja-gold750-gram": rupees(g750_gram),
            "ibja-silver999-main": rupees(silver999),
            "ibja-silver999-gram": rupees(silver_gram),
        }

        for element_id, value in replacements.items():
            pattern = rf'(<(?:span|strong) id="{re.escape(element_id)}">)[^<]*(</(?:span|strong)>)'
            html = replace_once(html, pattern, rf"\g<1>{value}\g<2>", element_id)

    INDEX_PATH.write_text(html, encoding="utf-8")
    print(
        f"Updated IBJA {period} rates for {rate_date:%d-%m-%Y}: "
        f"999={gold999}, 916={gold916}, 750={gold750}, silver999={silver999}"
    )


def main() -> None:
    soup = fetch_soup()
    values, rate_date, period = get_ibja_rates(soup)
    update_index(values, rate_date, period)


if __name__ == "__main__":
    main()
