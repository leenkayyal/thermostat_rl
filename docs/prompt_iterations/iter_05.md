## Iteration 5

### Prompt used
"Should the HVAC hold, pre-heat, or pre-cool? Use ONLY the numbers below."

### What failed
The coach still occasionally produced unrealistic recommendations despite grounded data.

### What changed in final version
Added stricter wording:
- "Do NOT invent values"
- "Mention actual numbers"
- "Use ONLY the metrics below"

Improved grounding by directly embedding all tool outputs into the final prompt.
