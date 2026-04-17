import os

import anthropic

client = anthropic.Anthropic()

# Model is read from the MODEL environment variable.
# Set it in your shell before running:
#
#   export MODEL="claude-haiku-4-5-20251001"   # fast, cost-efficient (default)
#   export MODEL="claude-sonnet-4-6"            # balanced, strong reasoning
#   export MODEL="claude-opus-4-6"              # most capable
#
MODEL = os.environ.get("MODEL", "claude-haiku-4-5-20251001")

message = client.messages.create(
    model=MODEL,
    max_tokens=1024,
    messages=[
        {
            "role": "user",
            "content": "Sony WH-1000XM5 headphones are listed for $279. Is that a good price to buy?",
        }
    ],
)

print(message.content[0].text)
