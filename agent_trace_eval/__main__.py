import os
from pathlib import Path

from agent_trace_eval.runner import run

def main() -> None:
    live = bool(os.environ.get("OPENAI_BASE_URL") and os.environ.get("OPENAI_API_KEY"))
    text = run(live=live)
    out = Path("scorecard.md")
    out.write_text(text)
    mode = "live" if live else "dry-run"
    print(f"{mode} -> {out}")

if __name__ == "__main__":
    main()
