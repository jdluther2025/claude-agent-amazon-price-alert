import json

import anthropic
from anthropic import beta_tool

client = anthropic.Anthropic()


# @beta_tool infers the schema from type hints and the docstring —
# no more hand-written JSON schema
@beta_tool
def fetch_product_price(url: str) -> str:
    """Fetches the current price of a product from a given URL.

    Args:
        url: The product URL to fetch the price from.
    """
    return json.dumps({"product": "Sony WH-1000XM5", "price": 279.00, "currency": "USD"})


@beta_tool
def get_price_history(url: str) -> str:
    """Returns the recent price history for a product URL.

    Args:
        url: The product URL to get price history for.
    """
    return json.dumps({
        "product": "Sony WH-1000XM5",
        "history": [
            {"date": "2025-04-01", "price": 320.00},
            {"date": "2025-04-05", "price": 310.00},
            {"date": "2025-04-09", "price": 299.00},
            {"date": "2025-04-12", "price": 289.00},
            {"date": "2025-04-14", "price": 279.00},
        ],
        "all_time_low": 248.00,
    })


# tool_runner handles the agentic loop — no while loop, no manual
# stop_reason checking, no appending messages by hand
final_message = client.beta.messages.tool_runner(
    model="claude-opus-4-6",
    max_tokens=1024,
    tools=[fetch_product_price, get_price_history],
    messages=[
        {
            "role": "user",
            "content": (
                "Check the current price and recent price history for "
                "https://www.amazon.com/dp/B09XS7JWHH. "
                "Is now a good time to buy?"
            ),
        }
    ],
).until_done()

for block in final_message.content:
    if block.type == "text":
        print(block.text)
