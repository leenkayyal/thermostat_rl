# Contributions

## Team Members
- Leen
- Julnas

---

## Module Ownership

### Leen
Leen was responsible for:

- Reinforcement learning training and evaluation
- DQN model setup and tuning
- Baseline comparison
- Lambda sweep evaluation
- Learning curve generation
- Final testing and debugging

Main files worked on:

- `rl/train.py`
- `rl/evaluate.py`
- `rl/plot_learning_curve.py`
- `models/`
- `docs/learning_curve.png`
- `docs/lambda_sweep.png`

---

### Julnas
Julnas was responsible for:

- LLM coach integration
- Tool functions for grounded LLM output
- Two-day evaluation
- Coach report generation
- Prompt iteration documentation
- Demo/report support

Main files worked on:

- `agent/tools.py`
- `agent/coach.py`
- `eval/two_day_eval.py`
- `docs/mild_day_report.txt`
- `docs/extreme_day_report.txt`
- `docs/prompt_iterations/`

---

### Shared Work
Both Leen and Julnas contributed to:

- Project idea refinement
- Simulator testing
- Final integration
- Running pytest tests
- Reviewing outputs and plots
- Writing the final report
- Preparing the demo video

Shared files and folders:

- `env/thermal_env.py`
- `tests/`
- `docs/`
- `README.md`
- `report.md`

---

## AI Assistance and Generated Content

AI assistance was used during the project.

The following parts were AI-assisted:

- Code structure and project organization
- Python code for the RC thermal simulator
- Gymnasium environment boilerplate
- DQN training and evaluation scripts
- LLM coach prompt structure
- Tool function templates
- Two-day evaluation script
- README structure
- Report structure
- Architecture diagram content and layout ideas

The code and architecture diagram were AI-generated with student guidance, then reviewed and edited by the team.

---

## How AI-Generated Work Was Reviewed

All AI-generated work was reviewed before being included in the final project.

The review process included:

1. Reading the generated code line by line
2. Running each script to check that it worked
3. Debugging errors when they appeared
4. Testing the environment using pytest
5. Checking plots and outputs manually
6. Comparing LLM coach responses against real tool values
7. Editing prompts when the LLM gave vague or incorrect advice

---

## Testing and Verification

The final system was tested using:

```bash
pytest tests/ -v
