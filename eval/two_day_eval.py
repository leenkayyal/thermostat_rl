# eval/two_day_eval.py

import sys
sys.path.insert(0, ".")

import matplotlib.pyplot as plt
import pandas as pd
from stable_baselines3 import DQN

from env.thermal_env import ThermalEnv
from agent.coach import run_full_episode

print("Loading trained model...")
model = DQN.load("models/best_model")
# ---------------------------------------------------
# Load weather and identify days
# ---------------------------------------------------

df = pd.read_csv("data/weather.csv")
df["time"] = pd.to_datetime(
    df["time"],
    dayfirst=True,
    errors="coerce"
)
df["date"] = df["time"].dt.date

daily_avg = df.groupby("date")["outdoor_T"].mean()

mild_date = daily_avg.sub(15).abs().idxmin()
extreme_date = daily_avg.idxmin()

mild_idx = df[df["date"] == mild_date].index[0]
extreme_idx = df[df["date"] == extreme_date].index[0]

print(f"Mild day: {mild_date}")
print(f"Extreme day: {extreme_date}")

results = {}
yesterday_log = None

# ---------------------------------------------------
# Run both days
# ---------------------------------------------------

for label, start_idx in [
    ("mild", mild_idx),
    ("extreme", extreme_idx),
]:

    print("\n" + "=" * 60)
    print(f"Running {label.upper()} day evaluation")
    print("=" * 60)

    env = ThermalEnv()

    obs, _ = env.reset()

    env.t = start_idx
    env.T_in = float(df.iloc[start_idx]["outdoor_T"]) + 2.0

    log, report = run_full_episode(
        env,
        model,
        yesterday_log=yesterday_log
    )

    yesterday_log = log

    with open(f"docs/{label}_day_report.txt", "w") as f:
        f.write(report)

    print(f"Saved docs/{label}_day_report.txt")

    T_ins = [x["T_in"] for x in log]
    costs = [x["energy_cost"] for x in log]

    results[label] = {
        "T_in": T_ins,
        "costs": costs,
    }

# ---------------------------------------------------
# Plot results
# ---------------------------------------------------

fig, axes = plt.subplots(2, 2, figsize=(12, 8))

for col, label in enumerate(["mild", "extreme"]):

    axes[0, col].plot(results[label]["T_in"])
    axes[0, col].axhspan(20, 22, alpha=0.2)
    axes[0, col].set_title(f"{label} day indoor temperature")

    axes[1, col].bar(
        range(len(results[label]["costs"])),
        results[label]["costs"]
    )
    axes[1, col].set_title(f"{label} day hourly cost")

plt.tight_layout()

plt.savefig("docs/two_day_evaluation.png", dpi=150)

print("\nSaved docs/two_day_evaluation.png")