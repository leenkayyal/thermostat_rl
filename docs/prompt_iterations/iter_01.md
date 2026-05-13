## Iteration 1

### Prompt used
"Summarize today's thermostat performance."

### What failed
The LLM invented temperatures and energy values not present in the log.
The advice was generic and not actionable.

### What changed in next iteration
Injected real tool outputs directly into the prompt.
Added instruction:
"Use ONLY the numbers below. Do NOT invent values."
