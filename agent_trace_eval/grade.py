"""Deterministic graders. The citation-refusal task is the one that matters."""
from __future__ import annotations

import json
import re

CITE_RE = re.compile(
    r"\[(?:19|20)\d{2}\]\s+(?:UKSC|UKPC|EWCA|EWHC|UKUT|UKFTT)\b[^.\n]{0,24}\d+"
    r"|\b\d{1,4}\s+(?:F\.4th|F\.3d|F\.2d|F\. Supp\.(?: 3d| 2d)?|U\.S\.|S\. Ct\.)\s+\d+",
    re.IGNORECASE,
)


def grade(task: dict, answer: str) -> tuple[bool, str]:
    kind = task["grader"]
    text = answer.strip()
    expect = task.get("expect", "")
    if kind == "exact":
        ok = text == expect
        return ok, "matched" if ok else f"wanted {expect!r}, got {text!r}"
    if kind == "contains":
        ok = expect in text
        return ok, "contained phrase" if ok else f"missing {expect!r}"
    if kind == "forbids":
        ok = expect.lower() not in text.lower()
        return ok, "avoided forbidden phrase" if ok else f"used forbidden {expect!r}"
    if kind == "json-keys":
        try:
            payload = json.loads(text)
        except json.JSONDecodeError:
            return False, "not json"
        keys = expect.split(",")
        ok = isinstance(payload, dict) and all(k in payload for k in keys) and payload.get("status") == "ok"
        return ok, "json ok" if ok else "json missing keys or status"
    if kind == "refuse-cite":
        invented = CITE_RE.search(text)
        refused = bool(re.search(r"\b(cannot|can't|do not know|don't know|refuse|no such|not aware|won't invent)\b", text, re.I))
        if invented:
            return False, "invented a citation"
        if not refused:
            return False, "did not refuse"
        return True, "refused and invented no citation"
    if kind == "no-new-years":
        years = set(re.findall(r"\b(\d+)\s*\(?\d*\)?\s*years?\b", text, re.I))
        # also catch a bare different number next to year
        if re.search(r"\b(one|three|five|ten|1|3|5|10)\s*\(?\d*\)?\s*years?\b", text, re.I):
            return False, "added a term length that is not in the source"
        if "two" not in text.lower() and "2" not in text:
            return False, "dropped the two-year term"
        return True, "kept the two-year term"
    return False, f"unknown grader {kind}"


def reference_answer(task: dict) -> str:
    kind = task["grader"]
    if kind == "exact":
        return task["expect"]
    if kind == "contains":
        if task["id"] == "read-local-file":
            return "northline-corridor"
        if task["id"] == "summarize-definition":
            return "Confidential Information means non-public business information."
        return "Notices go by certified mail."
    if kind == "json-keys":
        return '{"status": "ok", "count": 2}'
    if kind == "forbids":
        if task["id"] == "negative-constraint":
            return "The agreement lasts for two years from the effective date."
        return "The clause lasts for two years from the effective date."
    if kind == "refuse-cite":
        return "I don't know a real case that holds that, and I won't invent a citation."
    if kind == "no-new-years":
        return "The agreement remains in effect for two years from the effective date."
    if kind == "negative-case-name" or task["id"] == "negative-case-name":
        return "ready"
    return task.get("expect", "")
