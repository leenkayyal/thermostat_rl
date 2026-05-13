import sys
sys.path.insert(0, ".")   # make sure project root is on the path

import matplotlib.pyplot as plt
import numpy as np
from env.thermal_env import ThermalEnv

# ─── Sanity 1: Passive thermal lag (HVAC completely off) ─────────────────────
def sanity_passive_lag():
    env = ThermalEnv(seed=42)
    obs, _ = env.reset()

    T_in_log, T_out_log = [], []

    for step in range(72):   # simulate 72 hours (3 days)
        # Force HVAC off by making setpoint unreachable
        env.setpoint = -999  # way below T_in → cooling, but let's hack:
        # Cleaner way: directly call step and override P to 0
        row = env.weather.iloc[env.t]
        T_out = float(row["outdoor_T"])
        # Apply RC model with P=0 manually
        dT = (1.0/env.C) * ((T_out - env.T_in)/env.R) * 3600.0
        env.T_in = float(env.T_in + dT)
        env.t += 1

        T_in_log.append(env.T_in)
        T_out_log.append(T_out)

    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(T_out_log, label="Outdoor temperature", color="steelblue", linewidth=1.5)
    ax.plot(T_in_log,  label="Indoor temperature (HVAC off)", color="tomato",
            linewidth=1.5, linestyle="--")
    ax.set_xlabel("Hour")
    ax.set_ylabel("Temperature (°C)")
    ax.set_title("Sanity check 1: Indoor T tracks outdoor T with lag (HVAC off)")
    ax.legend()
    ax.grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig("docs/sanity_passive_lag.png", dpi=150)
    plt.close()
    print("Saved: docs/sanity_passive_lag.png")
    print("  → Indoor T should follow outdoor T but with a delay/smoothing effect")

# ─── Sanity 2: Setpoint convergence (HVAC on, no disturbance) ────────────────
def sanity_convergence():
    env = ThermalEnv(seed=42)
    env.reset()

    # Set up: cold room, setpoint 21°C, outdoor same as indoor (no disturbance)
    env.T_in = 10.0
    env.setpoint = 21.0
    TARGET = 21.0

    T_in_log = [env.T_in]

    for step in range(48):   # 48 hours max
        # Force outdoor = indoor so only HVAC matters
        env.weather.at[env.t, "outdoor_T"] = env.T_in
        obs, reward, done, _, info = env.step(1)  # action=1 = hold setpoint
        T_in_log.append(info["T_in"])
        if done:
            break

    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(T_in_log, label="Indoor temperature", color="tomato", linewidth=1.5)
    ax.axhline(TARGET, color="green", linestyle="--",
               linewidth=1.5, label=f"Setpoint ({TARGET}°C)")
    ax.axhspan(19.5, 22.5, alpha=0.1, color="green", label="Comfort band")
    ax.set_xlabel("Hour")
    ax.set_ylabel("Temperature (°C)")
    ax.set_title("Sanity check 2: HVAC heats room to setpoint and holds it")
    ax.legend()
    ax.grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig("docs/sanity_convergence.png", dpi=150)
    plt.close()
    print("Saved: docs/sanity_convergence.png")
    print("  → Indoor T should rise from 10°C and converge near 21°C")

if __name__ == "__main__":
    sanity_passive_lag()
    sanity_convergence()
    print("\nBoth sanity checks done. Include these plots in your report!")