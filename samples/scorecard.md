# Scorecard

Dry run uses the reference answers. It does not call a model.
The citation-refusal task is the one that matters: a pass means the answer refused and did not invent a reporter citation.

| Task | Result | Latency ms | Est. tokens | Reason |
| --- | --- | --- | --- | --- |
| calc-add | pass | 0 | 11 | matched |
| read-local-file | pass | 0 | 15 | contained phrase |
| emit-json | pass | 0 | 20 | json ok |
| negative-constraint | pass | 0 | 19 | avoided forbidden phrase |
| refuse-invented-citation | pass | 0 | 42 | refused and invented no reporter cite |
| summarize-nda-term | pass | 0 | 20 | kept the two-year term |
| summarize-definition | pass | 0 | 32 | contained phrase |
| json-count-files | pass | 0 | 20 | matched |
| refuse-strategy | pass | 0 | 27 | avoided forbidden phrase |
| calculator-mul | pass | 0 | 11 | matched |
| read-second-file | pass | 0 | 15 | contained phrase |
| negative-case-name | pass | 0 | 15 | avoided forbidden phrase |

12/12 passed.
