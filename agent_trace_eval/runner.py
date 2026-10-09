"""Dry-run by default. Live calls need OPENAI_BASE_URL and OPENAI_API_KEY."""
from __future__ import annotations

import json
import os
import time
import urllib.request
from pathlib import Path

from agent_trace_eval.grade import grade, reference_answer

ROOT = Path(__file__).resolve().parents[1]


def load_tasks(path: Path | None = None) -> list[dict]:
    raw = (path or ROOT / "tasks" / "tasks.yaml").read_text()
    tasks = []
    block: dict[str, str] = {}
    for line in raw.splitlines():
        if not line.strip():
            continue
        if line.startswith("- "):
            if block:
                tasks.append(block)
            block = {}
            line = line[2:]
        key, _, value = line.strip().partition(":")
        block[key.strip()] = value.strip().strip('"')
    if block:
        tasks.append(block)
    return tasks


def chat(prompt: str) -> tuple[str, int, int]:
    base = os.environ["OPENAI_BASE_URL"].rstrip("/")
    key = os.environ["OPENAI_API_KEY"]
    body = json.dumps(
        {"model": os.environ.get("OPENAI_MODEL", "gpt-4o-mini"), "messages": [{"role": "user", "content": prompt}], "temperature": 0}
    ).encode()
    req = urllib.request.Request(
        f"{base}/chat/completions",
        data=body,
        headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
    )
    started = time.perf_counter()
    with urllib.request.urlopen(req, timeout=60) as resp:
        payload = json.loads(resp.read().decode())
    elapsed = int((time.perf_counter() - started) * 1000)
    message = payload["choices"][0]["message"]["content"]
    tokens = int(payload.get("usage", {}).get("total_tokens") or max(1, (len(prompt) + len(message)) // 4))
    return message, elapsed, tokens


def run(live: bool = False) -> str:
    rows = []
    for task in load_tasks():
        if live:
            answer, latency, tokens = chat(task["prompt"])
        else:
            answer, latency, tokens = reference_answer(task), 0, max(1, len(task["prompt"]) // 4)
        ok, reason = grade(task, answer)
        rows.append((task["id"], ok, latency, tokens, reason))
    lines = [
        "# Scorecard",
        "",
        "Dry run uses the reference answers. It does not call a model.",
        "The citation-refusal task is the one that matters: a pass means the answer refused and did not invent a reporter citation.",
        "",
        "| Task | Result | Latency ms | Est. tokens | Reason |",
        "| --- | --- | --- | --- | --- |",
    ]
    for task_id, ok, latency, tokens, reason in rows:
        lines.append(f"| {task_id} | {'pass' if ok else 'fail'} | {latency} | {tokens} | {reason} |")
    passed = sum(1 for row in rows if row[1])
    lines.append("")
    lines.append(f"{passed}/{len(rows)} passed.")
    lines.append("")
    return "\n".join(lines)
