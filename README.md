# Project 8, RL Smart Thermostat

This project is an AI-powered smart thermostat system.

The goal is to control the indoor temperature of a house while balancing two things:

1. Keeping the house comfortable
2. Reducing electricity cost

The system combines three main layers:

- A thermal house simulator
- A reinforcement learning controller using DQN
- An LLM coach using Ollama

---

## Project Overview

This project simulates a single-zone house where indoor temperature changes based on outdoor weather, HVAC heating/cooling, and simple building physics.

A DQN reinforcement learning agent learns how to adjust the thermostat setpoint each hour.

An LLM coach reads real system metrics through tool functions and gives natural-language advice during the simulation.

The project includes:

- Weather data loading
- RC thermal simulator
- Gymnasium environment
- DQN training
- Baseline comparison
- Lambda sweep cost/comfort tradeoff
- LLM coach with grounded tools
- Two-day evaluation
- Automated tests
- Final plots and reports

---

## Project Structure

```text
thermostat_rl/
│
├── env/
│   └── thermal_env.py
│
├── rl/
│   ├── train.py
│   ├── evaluate.py
│   └── plot_learning_curve.py
│
├── agent/
│   ├── tools.py
│   └── coach.py
│
├── eval/
│   └── two_day_eval.py
│
├── tests/
│   ├── test_env.py
│   ├── test_tools.py
│   └── sanity_check.py
│
├── data/
│   ├── fetch_weather.py
│   └── weather.csv
│
├── docs/
│   ├── learning_curve.png
│   ├── lambda_sweep.png
│   ├── two_day_evaluation.png
│   ├── sanity_passive_lag.png
│   ├── sanity_convergence.png
│   ├── mild_day_report.txt
│   ├── extreme_day_report.txt
│   └── prompt_iterations/
│
├── models/
│   ├── dqn_thermostat.zip
│   ├── best_model.zip
│   ├── dqn_lambda_0.0.zip
│   ├── dqn_lambda_0.5.zip
│   └── dqn_lambda_2.0.zip
│
├── seeds.py
├── requirements.txt
├── report.md
├── contributions.md
└── README.md

```
