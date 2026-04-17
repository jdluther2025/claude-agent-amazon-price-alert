import json

import anthropic

client = anthropic.Anthropic()

# The tool schema — Claude reads this to know what the tool does
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


# The function Claude will ask us to run
def fetch_product_price(url: str) -> dict:
    # Hardcoded for now — real scraping comes later
    return {"product": "Sony WH-1000XM5", "price": 279.00, "currency": "USD"}


# Step 1 — send the first message with the tool available
messages = [
    {
        "role": "user",
        "content": "Check the price at https://www.amazon.com/dp/B09XS7JWHH and tell me if it's a good deal.",
    }
]

response = client.messages.create(
    model="claude-opus-4-6",
    max_tokens=1024,
    tools=tools,
    tool_choice={"type": "auto", "disable_parallel_tool_use": True},
    messages=messages,
)

print(f"Stop reason: {response.stop_reason}")

# Step 2 — handle the tool_use response
if response.stop_reason == "tool_use":
    tool_use_block = next(b for b in response.content if b.type == "tool_use")
    tool_name = tool_use_block.name
    tool_input = tool_use_block.input
    tool_use_id = tool_use_block.id

    print(f"Claude wants to call: {tool_name}({tool_input})")

    # Step 3 — execute the function
    result = fetch_product_price(**tool_input)
    print(f"Tool result: {result}")

    # Step 4 — send the result back
    messages.append({"role": "assistant", "content": response.content})
    messages.append(
        {
            "role": "user",
            "content": [
                {
                    "type": "tool_result",
                    "tool_use_id": tool_use_id,
                    "content": json.dumps(result),
                }
            ],
        }
    )

    # Step 5 — get Claude's final answer
    final_response = client.messages.create(
        model="claude-opus-4-6",
        max_tokens=1024,
        tools=tools,
        tool_choice={"type": "auto", "disable_parallel_tool_use": True},
        messages=messages,
    )

    print("\n--- Claude's answer ---")
    print(final_response.content[0].text)
