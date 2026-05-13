"""
agent/coach.py

LLM thermostat coach using Ollama.
"""

import sys
sys.path.insert(0, ".")

import ollama

from agent.tools import (
    current_temp,
    time_outside_comfort_today,
    cost_so_far,
    vs_yesterday,
)

MODEL = "llama3.2:3b"


def ask_coach(
    episode_log: list,
    yesterday_log: list = None,
    mode: str = "mid_run",
) -> str:

    # --- Tool calls ---
    t_info = current_temp(episode_log)

    comfort_info = time_outside_comfort_today(
        episode_log
    )

    cost_info = cost_so_far(episode_log)

    compare_info = vs_yesterday(
        episode_log,
        yesterday_log or []
    )

    # --- Prompt ---
    if mode == "mid_run":

        prompt = f"""
You are a smart thermostat AI coach.

Use ONLY the numbers below.
Do NOT invent temperatures or costs.

CURRENT STATUS:
- {t_info}
- Comfort today: {comfort_info}
- Cost today: {cost_info}
- Compared to yesterday: {compare_info}

Give a short 1-2 sentence recommendation.

Should the HVAC hold, pre-heat, or pre-cool?
Mention actual numbers from the data.
"""

    elif mode == "end_of_day":

        prompt = f"""
You are a smart thermostat AI coach.

Use ONLY the numbers below.
Do NOT invent figures.

TODAY'S RESULTS:
- {t_info}
- Comfort: {comfort_info}
- Energy cost: {cost_info}
- Compared to yesterday: {compare_info}

Write a 3-4 sentence personalized report.

Mention actual numbers above and suggest
one concrete improvement for tomorrow.
"""

    else:
        raise ValueError(
            "mode must be 'mid_run' or 'end_of_day'"
        )

    # --- LLM call ---
    response = ollama.chat(
        model=MODEL,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response["message"]["content"].strip()


def run_full_episode(
    env,
    model,
    yesterday_log=None
):
    """
    Run one full episode using DQN + LLM coach.
    """

    obs, _ = env.reset()

    episode_log = []

    done = False
    step = 0

    print("Starting episode with DQN + LLM coach...")

    while not done:

        action, _ = model.predict(
            obs,
            deterministic=True
        )

        obs, reward, done, _, info = env.step(
            int(action)
        )

        episode_log.append(info)

        # Coach update every 6 hours
        if step > 0 and step % 6 == 0 and not done:

            alert = ask_coach(
                episode_log,
                yesterday_log,
                mode="mid_run"
            )

            print(f"\n[Hour {step}]")
            print(alert)

        step += 1

    print("\n" + "=" * 50)

    print("[END OF DAY REPORT]")

    report = ask_coach(
        episode_log,
        yesterday_log,
        mode="end_of_day"
    )

    print(report)

    print("=" * 50)

    return episode_log, report