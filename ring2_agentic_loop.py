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
    }
]


def fetch_product_price(url: str) -> dict:
    # Hardcoded for now — real scraping comes later
    return {"product": "Sony WH-1000XM5", "price": 279.00, "currency": "USD"}


def run_tool(tool_name: str, tool_input: dict) -> str:
    if tool_name == "fetch_product_price":
        result = fetch_product_price(**tool_input)
        return json.dumps(result)
    return json.dumps({"error": f"Unknown tool: {tool_name}"})


messages = [
    {
        "role": "user",
        "content": (
            "Monitor the price at https://www.amazon.com/dp/B09XS7JWHH. "
            "Check it twice and tell me if the price changes between checks."
        ),
    }
]

response = client.messages.create(
    model="claude-opus-4-6",
    max_tokens=1024,
    tools=tools,
    tool_choice={"type": "auto", "disable_parallel_tool_use": True},
    messages=messages,
)

# The agentic loop — keeps running until Claude stops calling tools
while response.stop_reason == "tool_use":
    tool_use = next(block for block in response.content if block.type == "tool_use")

    print(f"Claude calls: {tool_use.name}({tool_use.input})")
    result = run_tool(tool_use.name, tool_use.input)
    print(f"Result: {result}")

    messages.append({"role": "assistant", "content": response.content})
    messages.append(
        {
            "role": "user",
            "content": [
                {
                    "type": "tool_result",
                    "tool_use_id": tool_use.id,
                    "content": result,
                }
            ],
        }
    )

    response = client.messages.create(
        model="claude-opus-4-6",
        max_tokens=1024,
        tools=tools,
        tool_choice={"type": "auto", "disable_parallel_tool_use": True},
        messages=messages,
    )

final_text = next(block for block in response.content if block.type == "text")
print("\n--- Claude's answer ---")
print(final_text.text)
