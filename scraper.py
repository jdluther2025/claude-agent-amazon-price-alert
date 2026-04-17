import json
import os
import sys

from firecrawl import FirecrawlApp


def fetch_product_price(url: str) -> dict:
    """Fetches the current price of a product from a given URL.

    Uses FireCrawl extract to handle JavaScript-rendered pages and
    return structured data. Works with Amazon and most retail sites.

    Args:
        url: The product URL to fetch the price from.

    Returns:
        A dict with product, price, and currency keys.

    Raises:
        ValueError: If the price could not be extracted from the page.
    """
    app = FirecrawlApp(api_key=os.environ["FIRECRAWL_API_KEY"])
    result = app.extract(
        [url],
        prompt="Extract the main product name and its current selling price.",
        schema={
            "type": "object",
            "properties": {
                "product": {"type": "string"},
                "price": {"type": "number"},
                "currency": {"type": "string"},
            },
            "required": ["product", "price", "currency"],
        },
    )

    if not result.success or not result.data:
        raise ValueError(f"Failed to extract price from {url}")

    currency_map = {"USD": "$", "US$": "$", "CAD": "CA$", "EUR": "€", "GBP": "£"}
    raw_currency = result.data["currency"]
    currency = currency_map.get(raw_currency.upper(), raw_currency)

    return {
        "product": result.data["product"],
        "price": result.data["price"],
        "currency": currency,
    }


def check_watchlist(path: str) -> list[dict]:
    """Fetches prices for all products in a watchlist file.

    The watchlist is a JSON array of objects with url, and optional
    name and threshold fields.

    Args:
        path: Path to the watchlist JSON file.

    Returns:
        A list of results with current price and alert status.
    """
    with open(path) as f:
        watchlist = json.load(f)

    results = []
    for item in watchlist:
        url = item["url"]
        threshold = item.get("threshold")
        print(f"Checking: {item.get('name', url)}")
        try:
            data = fetch_product_price(url)
            alert = threshold is not None and data["price"] <= threshold
            results.append({**data, "url": url, "threshold": threshold, "alert": alert})
        except ValueError as e:
            results.append({"url": url, "error": str(e), "alert": False})

    return results


if __name__ == "__main__":
    if len(sys.argv) == 1:
        # Default: single product
        url = "https://www.amazon.com/dp/B09XS7JWHH"
        print(json.dumps(fetch_product_price(url), indent=2))

    elif sys.argv[1] == "--watchlist":
        # Watchlist mode: python3 scraper.py --watchlist watchlist.json
        path = sys.argv[2] if len(sys.argv) > 2 else "watchlist.json"
        results = check_watchlist(path)
        print("\n--- Results ---")
        for r in results:
            if "error" in r:
                print(f"ERROR  {r['url']}: {r['error']}")
            else:
                alert_flag = " *** ALERT: AT OR BELOW THRESHOLD ***" if r["alert"] else ""
                print(f"{r['currency']}{r['price']:>8.2f}  {r['product'][:60]}{alert_flag}")

    else:
        # Single URL passed as argument
        url = sys.argv[1]
        print(json.dumps(fetch_product_price(url), indent=2))
