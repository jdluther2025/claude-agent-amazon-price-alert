import json

import anthropic

client = anthropic.Anthropic()

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
    # Simulate a blocked request — Amazon rate-limiting
    raise ConnectionError("Request blocked: Amazon returned a 503. Try again later.")


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
    raise ValueError(f"Unknown tool: {name}")


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
    model="claude-opus-4-6",
    max_tokens=1024,
    tools=tools,
    messages=messages,
)

while response.stop_reason == "tool_use":
    tool_results = []
    for block in response.content:
        if block.type == "tool_use":
            print(f"Claude calls: {block.name}({block.input})")
            try:
                result = run_tool(block.name, block.input)
                print(f"Result: {json.dumps(result)}")
                tool_results.append(
                    {
                        "type": "tool_result",
                        "tool_use_id": block.id,
                        "content": json.dumps(result),
                    }
                )
            except Exception as exc:
                # Signal failure so Claude can retry or ask for clarification
                print(f"Error: {exc}")
                tool_results.append(
                    {
                        "type": "tool_result",
                        "tool_use_id": block.id,
                        "content": str(exc),
                        "is_error": True,
                    }
                )

    messages.append({"role": "assistant", "content": response.content})
    messages.append({"role": "user", "content": tool_results})

    response = client.messages.create(
        model="claude-opus-4-6",
        max_tokens=1024,
        tools=tools,
        messages=messages,
    )

final_text = next(block for block in response.content if block.type == "text")
print("\n--- Claude's answer ---")
print(final_text.text)
