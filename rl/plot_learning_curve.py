import sys; sys.path.insert(0, ".")
import numpy as np
import matplotlib.pyplot as plt

# Load the evaluation data saved by EvalCallback
data = np.load("models/evaluations.npz")
timesteps   = data["timesteps"]          # x-axis: training steps
mean_rewards = data["results"].mean(axis=1)  # y-axis: avg reward over 5 eval episodes

fig, ax = plt.subplots(figsize=(9, 4))
ax.plot(timesteps, mean_rewards, color="steelblue", linewidth=2)
ax.fill_between(timesteps,
                data["results"].min(axis=1),
                data["results"].max(axis=1),
                alpha=0.2, color="steelblue", label="Min/max range")
ax.axhline(mean_rewards[0], linestyle="--", color="red",
           alpha=0.7, label=f"Initial reward: {mean_rewards[0]:.1f}")
ax.set_xlabel("Training timesteps")
ax.set_ylabel("Mean episode reward")
ax.set_title("DQN learning curve — thermostat control")
ax.legend()
ax.grid(alpha=0.3)
plt.tight_layout()
plt.savefig("docs/learning_curve.png", dpi=150)
print("Saved: docs/learning_curve.png")
print(f"Reward improved from {mean_rewards[0]:.1f} to {mean_rewards[-1]:.1f}")