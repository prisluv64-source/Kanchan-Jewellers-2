import re
from pathlib import Path

import requests
from bs4 import BeautifulSoup

GOLD_URL = "https://malayalam.goodreturns.in/gold-rates/delhi.html"
SILVER_URL = "https://malayalam.goodreturns.in/silver-rates/delhi.html"
INDEX_PATH = Path("index.html")

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0 Safari/537.36"
    ),
    "Accept-Language": "en-US,en;q=0.9",
}


def page_text(url: str) -> str:
    response = requests.get(url, headers=HEADERS, timeout=30)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")
    return " ".join(soup.stripped_strings)


def clean_number(value: str) -> str:
    number = float(value.replace(",", "").strip())
    if number.is_integer():
        return f"{int(number):,}"
    return f"{number:,.2f}".rstrip("0").rstrip(".")


def extract_gold_22k(text: str) -> str:
    patterns = [
        r"22K[^₹]{0,120}₹\s*([\d,.]+)",
        r"22\s*കാരറ്റ്[^₹]{0,120}₹\s*([\d,.]+)",
    ]
    for pattern in patterns:
        match = re.search(pattern, text, flags=re.IGNORECASE)
        if match:
            return clean_number(match.group(1))
    raise RuntimeError("Could not find Delhi 22K gold rate on Goodreturns page")


def extract_silver_1g(text: str) -> str:
    patterns = [
        r"(?:Silver|വെള്ളി)[^₹]{0,160}/g[^₹]{0,80}₹\s*([\d,.]+)",
        r"(?:Silver|വെള്ളി)[^₹]{0,160}gram[^₹]{0,80}₹\s*([\d,.]+)",
        r"1\s*\|\s*₹\s*([\d,.]+)",
    ]
    for pattern in patterns:
        match = re.search(pattern, text, flags=re.IGNORECASE)
        if match:
            return clean_number(match.group(1))
    raise RuntimeError("Could not find Delhi silver per-gram rate on Goodreturns page")


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
    gold_text = page_text(GOLD_URL)
    silver_text = page_text(SILVER_URL)
    gold = extract_gold_22k(gold_text)
    silver = extract_silver_1g(silver_text)
    update_index(gold, silver)


if __name__ == "__main__":
    main()
