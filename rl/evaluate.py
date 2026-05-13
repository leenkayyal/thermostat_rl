import sys
sys.path.insert(0, ".")

import numpy as np
import matplotlib.pyplot as plt

from stable_baselines3 import DQN

from env.thermal_env import ThermalEnv
from seeds import SEED


def run_episode(env, policy_fn):

    obs, _ = env.reset()

    total_cost = 0.0
    total_discomfort = 0.0

    done = False

    while not done:

        action = policy_fn(obs)

        obs, reward, done, _, info = env.step(action)

        total_cost += info["energy_cost"]
        total_discomfort += info["discomfort"]

    return total_cost, total_discomfort


# =========================================================
# Baseline comparison
# =========================================================

model = DQN.load("models/dqn_lambda_0.5.zip")

dqn_policy = lambda obs: int(
    model.predict(obs, deterministic=True)[0]
)

baseline_policy = lambda obs: 1

dqn_costs = []
dqn_discomforts = []

base_costs = []
base_discomforts = []

print("Running evaluation...")

for ep in range(5):

    env = ThermalEnv(lam=0.5, seed=SEED + ep)

    c, d = run_episode(env, dqn_policy)

    dqn_costs.append(c)
    dqn_discomforts.append(d)

    env2 = ThermalEnv(lam=0.5, seed=SEED + ep)

    c2, d2 = run_episode(env2, baseline_policy)

    base_costs.append(c2)
    base_discomforts.append(d2)

print("\nBASELINE")
print(f"Cost: ${np.mean(base_costs):.2f}")
print(f"Discomfort: {np.mean(base_discomforts):.2f}")

print("\nDQN")
print(f"Cost: ${np.mean(dqn_costs):.2f}")
print(f"Discomfort: {np.mean(dqn_discomforts):.2f}")

beat = (
    np.mean(dqn_costs) < np.mean(base_costs)
    or
    np.mean(dqn_discomforts) < np.mean(base_discomforts)
)

print(f"\nDQN beats baseline: {'YES ✓' if beat else 'NO'}")


# =========================================================
# True lambda sweep
# =========================================================

lambdas = [0.0, 0.5, 2.0]

costs = []
discomforts = []

print("\nRunning TRUE lambda sweep...")

for lam in lambdas:

    model = DQN.load(f"models/dqn_lambda_{lam}.zip")

    policy = lambda obs: int(
        model.predict(obs, deterministic=True)[0]
    )

    env = ThermalEnv(
        lam=lam,
        seed=SEED + 100
    )

    c, d = run_episode(env, policy)

    costs.append(c)
    discomforts.append(d)

    print(
        f"lambda={lam:.1f}  "
        f"cost=${c:.2f}  "
        f"discomfort={d:.2f}"
    )

# Plot
plt.figure(figsize=(7, 5))

plt.plot(costs, discomforts, "o-")

for i, lam in enumerate(lambdas):

    plt.annotate(
        f"λ={lam}",
        (costs[i], discomforts[i]),
        textcoords="offset points",
        xytext=(5, 5),
    )

plt.xlabel("Energy Cost ($)")
plt.ylabel("Discomfort")

plt.title("Cost vs Comfort Trade-off")

plt.grid(alpha=0.3)

plt.tight_layout()

plt.savefig("docs/lambda_sweep.png", dpi=150)

print("\nSaved: docs/lambda_sweep.png")