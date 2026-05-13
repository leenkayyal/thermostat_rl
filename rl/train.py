import sys
sys.path.insert(0, ".")

from stable_baselines3 import DQN
from stable_baselines3.common.monitor import Monitor
from stable_baselines3.common.callbacks import EvalCallback

from env.thermal_env import ThermalEnv
from seeds import SEED, set_all_seeds

set_all_seeds()

LAM = 2.0
train_env = Monitor(
    ThermalEnv(lam=LAM, seed=SEED)
)

eval_env = Monitor(
    ThermalEnv(lam=LAM, seed=SEED + 1)
)

model = DQN(
    policy="MlpPolicy",
    env=train_env,

    learning_rate=3e-4,
    batch_size=64,
    buffer_size=100_000,

    learning_starts=5_000,

    exploration_fraction=0.3,
    exploration_final_eps=0.05,

    gamma=0.99,

    target_update_interval=1000,

    verbose=1,
    seed=SEED,

    tensorboard_log="./runs/"
)

eval_callback = EvalCallback(
    eval_env=eval_env,

    best_model_save_path="./models/",
    log_path="./models/",

    eval_freq=5_000,
    n_eval_episodes=5,

    deterministic=True,
    verbose=1,
)

print("Starting training...")

model.learn(
    total_timesteps=100_000,
    callback=eval_callback,
    progress_bar=False,
)

model.save("models/dqn_thermostat")

print("\nTraining complete.")
print("Saved: models/dqn_thermostat.zip")