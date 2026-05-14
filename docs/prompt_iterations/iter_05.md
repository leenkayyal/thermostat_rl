## Iteration 5

### Prompt used (mid_run mode — final version)
```
You are a smart thermostat AI coach.
Use ONLY the numbers below. Do NOT invent any temperatures or costs.

CURRENT STATUS:
- {current_temp output}
- Comfort today: {time_outside_comfort_today output}
- Cost today: {cost_so_far output}
- Compared to yesterday: {vs_yesterday output}

Give a 1-2 sentence tactical recommendation right now.
Should the system pre-heat, pre-cool, or hold? Is there a drift warning?
Be specific — mention actual numbers from above.
Note: the thermostat setpoint is clipped to the range [15, 28]°C by the system.
```

### What failed
In an earlier iteration the LLM occasionally suggested setpoint adjustments outside the physically safe range — for example "raise setpoint to 30°C to pre-heat aggressively". This would be clipped by the env but the advice itself looked wrong and confused a reader unfamiliar with the clipping logic.

### What changed in next iteration (final)
Added the note "the thermostat setpoint is clipped to the range [15, 28]°C by the system" to both prompt modes. After this change all generated advice stayed within the valid range. This is the version used in the two-day evaluation.
