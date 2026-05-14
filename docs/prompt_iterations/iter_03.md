## Iteration 3

### Prompt used
```
You are a smart thermostat AI coach.
Use ONLY the numbers below. Do NOT invent any values.
Your response must contain at least one number from the CURRENT STATUS section.
Mention specific setpoint values, hour ranges, or cost comparisons in your advice.

CURRENT STATUS:
- {current_temp output}
- Comfort today: {time_outside_comfort_today output}
- Cost today: {cost_so_far output}
- Compared to yesterday: {vs_yesterday output}

Give a 1-2 sentence tactical recommendation right now.
Should the system pre-heat, pre-cool, or hold? Is there a drift warning? Be specific.
```

### What failed
The mid-run alert mode produced a 4-sentence paragraph instead of the requested 1-2 sentences. The extra length made the alerts noisy when printed to the terminal every 6 hours. The end-of-day mode (same prompt) produced adequate output. The problem was that a single prompt was being used for both modes without distinguishing the length requirements.

### What changed in next iteration
Split into two separate prompt modes: `mid_run` (1–2 sentences, tactical, immediate) and `end_of_day` (3–4 sentences, reflective, includes one concrete improvement for tomorrow). Each mode has its own prompt template in agent/coach.py with explicit length constraints.
