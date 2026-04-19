# Claude Agent — Amazon Price Alert

Companion code for the tutorial:

**[🔔 Claude Tutorial — Building a Production Ready AI Agent, Agentic Loop in Five Concentric Rings](https://medium.com/ai-ml-human-training-coaching/claude-tutorial-building-a-production-ready-ai-agent-agentic-loop-in-five-concentric-rings-b1ea4596b92f)**

A hands-on step-by-step guide on building a tool-using agent with Claude — from a single tool call to running a production-ready agentic loop.

---

## What's in This Repo

| File | Ring | What It Teaches |
|------|------|-----------------|
| `intro_basic_call.py` | Intro | First Claude API call — no tools |
| `ring1_tool_use.py` | Ring 1 | Single tool, single turn |
| `ring2_agentic_loop.py` | Ring 2 | The agentic loop — run until done |
| `ring3_multiple_tools.py` | Ring 3 | Multiple tools, parallel calls |
| `ring4_error_handling.py` | Ring 4 | Tools fail — handle it gracefully |
| `ring5_tool_runner.py` | Ring 5 | SDK abstraction — production-ready |
| `scraper.py` | Bonus | Real Amazon prices via FireCrawl |
| `watchlist.json` | Bonus | Monitor multiple products at once |

Each file is standalone. Run any ring independently.

---

## Setup

```bash
# Clone the repo
git clone https://github.com/jdluther2025/claude-agent-amazon-price-alert.git
cd claude-agent-amazon-price-alert

# Create and activate a virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install the SDK
pip install anthropic

# Set your API key
export ANTHROPIC_API_KEY=sk-ant-...

# Set the model (default: Haiku)
export MODEL="claude-haiku-4-5-20251001"
```

---

## Run the Rings

```bash
python3 intro_basic_call.py
python3 ring1_tool_use.py
python3 ring2_agentic_loop.py
python3 ring3_multiple_tools.py
python3 ring4_error_handling.py
python3 ring5_tool_runner.py
```

## Run the Real Scraper

```bash
pip install firecrawl-py
export FIRECRAWL_API_KEY=fc-...

python3 scraper.py --watchlist watchlist.json
```

---

## Model Options

All scripts read the model from the `MODEL` environment variable:

```bash
export MODEL="claude-haiku-4-5-20251001"   # fast, cost-efficient (default)
export MODEL="claude-sonnet-4-6"            # balanced, strong reasoning
export MODEL="claude-opus-4-6"              # most capable
```
