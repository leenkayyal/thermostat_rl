## Iteration 2

### Prompt used
```
You are a smart thermostat AI coach.
Use ONLY the numbers below. Do NOT invent any values.

CURRENT STATUS:
- {current_temp output}
- Comfort today: {time_outside_comfort_today output}
- Cost today: {cost_so_far output}
- Compared to yesterday: {vs_yesterday output}

Summarize today's performance and suggest one improvement for tomorrow.
```

### What failed
The LLM still produced advice that was too vague: "consider adjusting the thermostat" without specifying direction, magnitude, or timing. It also did not reference the specific numbers from the injected tool outputs in its response — it acknowledged them but did not weave them into the recommendation. A professor reading the output would not be able to tell whether the LLM was grounded in real data or generating generic text.

### What changed in next iteration
Added the instruction: "Mention the specific numbers from above in your recommendation. Be concrete — state a specific setpoint value, a specific hour range, or a specific cost comparison." Also added: "Your response must contain at least one number from the CURRENT STATUS section above."
