import json
import os

import anthropic

client = anthropic.Anthropic()

MODEL = os.environ.get("MODEL", "claude-haiku-4-5-20251001")

tools = [
    {
        "name": "fetch_product_price",
        "description": "Fetches the current price of a product from a given URL.",
        "input_schema": {
            "type": "object",
            "properties": {
                "url": {
                    "type": "string",
                    "description": "The product URL to fetch the price from.",
                }
            },
            "required": ["url"],
        },
    },
    {
        "name": "get_price_history",
        "description": "Returns the recent price history for a product URL.",
        "input_schema": {
            "type": "object",
            "properties": {
                "url": {
                    "type": "string",
                    "description": "The product URL to get price history for.",
                }
            },
            "required": ["url"],
        },
    },
]


def fetch_product_price(url: str) -> dict:
    return {"product": "Sony WH-1000XM5", "price": 279.00, "currency": "USD"}


def get_price_history(url: str) -> dict:
    return {
        "product": "Sony WH-1000XM5",
        "history": [
            {"date": "2025-04-01", "price": 320.00},
            {"date": "2025-04-05", "price": 310.00},
            {"date": "2025-04-09", "price": 299.00},
            {"date": "2025-04-12", "price": 289.00},
            {"date": "2025-04-14", "price": 279.00},
        ],
        "all_time_low": 248.00,
    }


def run_tool(name: str, tool_input: dict) -> dict:
    if name == "fetch_product_price":
        return fetch_product_price(**tool_input)
    if name == "get_price_history":
        return get_price_history(**tool_input)
    return {"error": f"Unknown tool: {name}"}


messages = [
    {
        "role": "user",
        "content": (
            "Check the current price and recent price history for "
            "https://www.amazon.com/dp/B09XS7JWHH. "
            "Is now a good time to buy?"
        ),
    }
]

response = client.messages.create(
    model=MODEL,
    max_tokens=1024,
    tools=tools,
    messages=messages,
)

while response.stop_reason == "tool_use":
    tool_results = []
    for block in response.content:
        if block.type == "tool_use":
            print(f"Claude calls: {block.name}({block.input})")
            result = run_tool(block.name, block.input)
            tool_results.append(
                {
                    "type": "tool_result",
                    "tool_use_id": block.id,
                    "content": json.dumps(result),
                }
            )

    messages.append({"role": "assistant", "content": response.content})
    messages.append({"role": "user", "content": tool_results})

    response = client.messages.create(
        model=MODEL,
        max_tokens=1024,
        tools=tools,
        messages=messages,
    )

final_text = next(block for block in response.content if block.type == "text")
print("\n--- Claude's answer ---")
print(final_text.text)
