## Iteration 4

### Prompt used (end_of_day mode)
```
You are a smart thermostat AI coach.
Use ONLY the numbers below for your report. Do NOT invent figures.

TODAY'S FINAL RESULTS:
- {current_temp output}
- Comfort: {time_outside_comfort_today output}
- Energy cost: {cost_so_far output}
- vs Yesterday: {vs_yesterday output}

Write a personalized 3-4 sentence end-of-day coaching message.
Mention the specific numbers above. Suggest one concrete improvement for tomorrow.
```

### What failed
The end-of-day report omitted the vs_yesterday comparison entirely when yesterday_log was None (first episode). The LLM silently dropped the section rather than noting there was no previous day to compare against. This made the first episode's report appear incomplete and inconsistent with subsequent episodes.

### What changed in next iteration
The vs_yesterday tool function was updated to return "No previous episode to compare against — this is the first evaluated day." when yesterday_log is empty. This string is now always injected into the prompt, so the LLM explicitly acknowledges the absence of prior data rather than silently omitting the section.
