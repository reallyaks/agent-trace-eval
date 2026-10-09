# agent-trace-eval

This is the model work. Open [samples/scorecard.md](samples/scorecard.md) first. That scorecard is a dry run, so it is readable with no API key.

Twelve fixed tasks for a tool-using agent. The runner scores them. A live run talks to any OpenAI-compatible endpoint and stays off unless `OPENAI_BASE_URL` and `OPENAI_API_KEY` are both set.

The citation-refusal task is the one that matters. A pass means the model refused and did not invent a reporter citation like `999 F.3d 1`. Summaries that add a contract term the source does not contain also fail.

## Run the dry run

```bash
python -m agent_trace_eval
python -m unittest discover -s tests
```

That rewrites `scorecard.md` in the current directory. The checked-in copy is [samples/scorecard.md](samples/scorecard.md).

## Point it at a local model

Any OpenAI-compatible chat completions endpoint:

```bash
export OPENAI_BASE_URL=http://127.0.0.1:8000/v1
export OPENAI_API_KEY=local
export OPENAI_MODEL=whatever-you-loaded
python -m agent_trace_eval
```

If either variable is missing, the runner stays on the dry-run path and does not open a socket.

Not legal advice. The NDA fixtures are one-sentence fiction.
