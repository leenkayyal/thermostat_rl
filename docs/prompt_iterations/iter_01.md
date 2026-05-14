## Iteration 1

### Prompt used
```
You are a smart thermostat AI coach. Summarize today's thermostat performance and give advice for tomorrow.
```

### What failed
The LLM invented temperature values not present in the episode log. Output stated "indoor temperature reached 24°C" when the actual logged maximum was 21.8°C. The response also fabricated a cost figure ("you spent approximately $0.45 today") with no relation to the actual energy_cost accumulated in the episode. The advice ("consider lowering your thermostat by 2 degrees") was generic and not grounded in any real observation.

### What changed in next iteration
Injected all 4 tool outputs (current_temp, time_outside_comfort_today, cost_so_far, vs_yesterday) directly into the prompt as clearly labelled facts. Added the explicit instruction: "Use ONLY the numbers below. Do NOT invent any values."
