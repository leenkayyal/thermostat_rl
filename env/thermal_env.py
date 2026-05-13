import gymnasium as gym
import numpy as np
import pandas as pd
from gymnasium import spaces


class ThermalEnv(gym.Env):
    """
    Smart thermostat environment.

    State:
        [indoor_T, outdoor_T, hour, occupied_next, price_now]

    Actions:
        0 = lower setpoint
        1 = hold
        2 = raise setpoint

    Reward:
        - energy_cost
        - lambda * discomfort
        - small action penalty
    """

    metadata = {"render_modes": []}

    # --- Thermal model ---
    R = 0.08
    C = 800_000.0
    P_hvac = 3500.0

    # --- Comfort ---
    T_comfort_low = 20.0
    T_comfort_high = 22.0
    T_setpoint_default = 21.0

    # --- Pricing ---
    PEAK_HOURS = set(range(14, 19))
    PRICE_PEAK = 0.30
    PRICE_OFFPEAK = 0.10

    EPISODE_LENGTH = 168  # 1 week

    def __init__(self, weather_csv="data/weather.csv", lam=0.5, seed=42):
        super().__init__()

        self.lam = lam
        self.rng = np.random.default_rng(seed)

        self.weather = pd.read_csv(weather_csv)

        self.weather["time"] = pd.to_datetime(
            self.weather["time"],
            dayfirst=True,
            errors="coerce"
        )

        self.n_steps = len(self.weather)

        self.action_space = spaces.Discrete(3)

        self.observation_space = spaces.Box(
            low=np.array([-10., -30., 0., 0., 0.], dtype=np.float32),
            high=np.array([40., 50., 1., 1., 1.], dtype=np.float32),
            dtype=np.float32,
        )

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)

        self.start_t = int(
            self.rng.integers(0, self.n_steps - self.EPISODE_LENGTH - 1)
        )

        self.t = self.start_t
        self.steps = 0

        row = self.weather.iloc[self.t]

        self.T_in = 21.0 + self.rng.uniform(-1.0, 1.0)
        self.setpoint = self.T_setpoint_default

        return self._get_obs(), {}

    def step(self, action):

        # --- Adjust setpoint ---
        delta = int(action) - 1
        self.setpoint = float(
            np.clip(self.setpoint + delta, 18.0, 24.0)
        )

        action_penalty = 0.02 * abs(delta)

        # --- Weather ---
        row = self.weather.iloc[self.t]

        T_out = float(row["outdoor_T"])
        current_time = row["time"]
        hour = int(current_time.hour)

        # --- HVAC control ---
        gap = self.setpoint - self.T_in

        if gap > 0.3:
            P = self.P_hvac
        elif gap < -0.3:
            P = -self.P_hvac
        else:
            P = 0.0

        # --- Thermal dynamics ---
        dT = (
            ((T_out - self.T_in) / self.R + P)
            / self.C
        ) * 3600.0

        self.T_in += dT

        self.T_in = float(np.clip(self.T_in, -10.0, 50.0))

        # --- Energy cost ---
        energy_kwh = abs(P) / 1000.0

        price = (
            self.PRICE_PEAK
            if hour in self.PEAK_HOURS
            else self.PRICE_OFFPEAK
        )

        energy_cost = energy_kwh * price

        # --- Comfort penalty ---
        discomfort = (
            max(0.0, self.T_comfort_low - self.T_in)
            + max(0.0, self.T_in - self.T_comfort_high)
        )

        # --- Reward ---
        reward = (
            -energy_cost
            - self.lam * discomfort
            - action_penalty
        )

        # --- Advance time ---
        self.t += 1
        self.steps += 1

        terminated = self.steps >= self.EPISODE_LENGTH
        truncated = False

        info = {
            "T_in": self.T_in,
            "T_out": T_out,
            "setpoint": self.setpoint,
            "energy_cost": energy_cost,
            "discomfort": discomfort,
            "peak": hour in self.PEAK_HOURS,
        }

        return self._get_obs(), reward, terminated, truncated, info

    def _get_obs(self):

        row = self.weather.iloc[self.t]

        current_time = row["time"]

        hour = int(current_time.hour)
        wday = int(current_time.weekday())

        next_hour = (hour + 1) % 24

        occupied_next = float(
            self._occupied(next_hour, wday < 5)
        )

        price_now = (
            1.0 if hour in self.PEAK_HOURS else 0.0
        )

        return np.array(
            [
                self.T_in,
                float(row["outdoor_T"]),
                hour / 23.0,
                occupied_next,
                price_now,
            ],
            dtype=np.float32,
        )

    def _occupied(self, hour, is_weekday):

        if is_weekday:
            return (7 <= hour <= 9) or (18 <= hour <= 22)

        return 9 <= hour <= 22