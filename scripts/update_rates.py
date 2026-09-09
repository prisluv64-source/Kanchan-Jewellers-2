import re
from pathlib import Path

import requests

BASE_URL = "https://api.apimitra.in/commodities"
INDEX_PATH = Path("index.html")

HEADERS = {
    "User-Agent": "KanchanJewellersRateUpdater/1.0",
    "Accept": "application/json",
}


def get_city_rate(metal: str) -> dict:
    response = requests.get(
        BASE_URL,
        params={"metal": metal, "city": "delhi"},
        headers=HEADERS,
        timeout=30,
    )
    response.raise_for_status()
    payload = response.json()

    if payload.get("status") != "ok" or not payload.get("data"):
        raise RuntimeError(f"No Delhi {metal} data returned: {payload}")

    return payload["data"][0]


def clean_number(value) -> str:
    number = float(value)
    if number.is_integer():
        return f"{int(number):,}"
    return f"{number:,.2f}".rstrip("0").rstrip(".")


def extract_gold_22k(item: dict) -> str:
    details = item.get("details") or {}
    value = details.get("price_22k")
    if value is None:
        raise RuntimeError(f"Delhi gold response has no price_22k: {item}")
    return clean_number(value)


def extract_silver_1g(item: dict) -> str:
    details = item.get("details") or {}

    # Prefer an explicit 1-gram / 999-fineness field if the API provides one.
    for key in ("price_999", "price_1g", "price_per_gram", "silver_999"):
        if details.get(key) is not None:
            return clean_number(details[key])

    # API Mitra's commodity `price` is the headline city price. For silver this
    # endpoint is expected to be INR per gram.
    if item.get("price") is not None:
        return clean_number(item["price"])

    raise RuntimeError(f"Delhi silver response has no usable per-gram price: {item}")


def update_index(gold: str, silver: str) -> None:
    html = INDEX_PATH.read_text(encoding="utf-8")
    pattern = re.compile(
        r"(?:Today's Rate|Delhi Rate):\s*"
        r"<strong>Gold 22K ₹[^<]+</strong>\s*"
        r"&nbsp;•&nbsp;\s*"
        r"<strong>Silver ₹[^<]+</strong>"
    )
    replacement = (
        f"Delhi Rate: <strong>Gold 22K ₹{gold}/g</strong> "
        f"&nbsp;•&nbsp; <strong>Silver ₹{silver}/g</strong>"
    )

    updated, count = pattern.subn(replacement, html, count=1)
    if count != 1:
        raise RuntimeError("Could not locate the rate block in index.html")

    INDEX_PATH.write_text(updated, encoding="utf-8")
    print(f"Updated Delhi rates: 22K Gold ₹{gold}/g, Silver ₹{silver}/g")


def main() -> None:
    gold_item = get_city_rate("gold")
    silver_item = get_city_rate("silver")
    gold = extract_gold_22k(gold_item)
    silver = extract_silver_1g(silver_item)
    update_index(gold, silver)


if __name__ == "__main__":
    main()
