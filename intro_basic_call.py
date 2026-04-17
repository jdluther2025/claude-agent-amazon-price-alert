import anthropic

client = anthropic.Anthropic()

# Model options — swap as needed:
#
# Haiku (fast, cost-efficient — good for tutorials and high-volume tasks)
#   claude-haiku-4-5-20251001
#
# Sonnet (balanced — strong reasoning, good for most production use cases)
#   claude-sonnet-4-6
#
# Opus (most capable — best for complex reasoning and nuanced tasks)
#   claude-opus-4-6
#
MODEL = "claude-haiku-4-5-20251001"

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
