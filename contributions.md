# contributions.md

## Module ownership
- RC thermal simulator (env/): Leen
- RL training & evaluation (rl/): Leen
- LLM coach & tools (agent/): Leen
- Integration & evaluation (eval/): Leen
- Tests: Leen
- Report: Leen

## AI assistance log
- env/thermal_env.py:
  RC formula structure and Gymnasium boilerplate were AI-assisted.
  Physics behavior was manually verified using sanity plots and runtime testing.

- rl/train.py:
  Initial DQN hyperparameters were AI-assisted, then manually tuned
  after observing unstable training behavior and long episode lengths.

- rl/evaluate.py:
  Evaluation structure and lambda sweep logic were AI-assisted.
  Outputs were manually checked against baseline behavior.

- agent/tools.py:
  Tool function structures were AI-assisted and manually tested with fake logs.

- agent/coach.py:
  Prompt engineering and grounding logic were AI-assisted.
  Prompt iterations were manually refined to reduce hallucinations.

## Review process
Each AI-generated code snippet was:
1. Read and understood manually
2. Executed with a small test
3. Modified when behavior did not match expectations
4. Verified using plots, logs, or pytest tests
