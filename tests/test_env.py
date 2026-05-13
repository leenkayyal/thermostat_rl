import sys
sys.path.insert(0, ".")

import numpy as np

from env.thermal_env import ThermalEnv


def test_obs_in_bounds():
    env = ThermalEnv()
    obs, _ = env.reset()

    assert env.observation_space.contains(obs)


def test_step_keys():
    env = ThermalEnv()

    env.reset()

    _, _, _, _, info = env.step(1)

    keys = [
        "T_in",
        "T_out",
        "setpoint",
        "energy_cost",
        "discomfort",
        "peak"
    ]

    for k in keys:
        assert k in info


def test_heating_increases_temp():
    env = ThermalEnv()

    env.reset()

    env.T_in = 10.0
    env.setpoint = 21.0

    _, _, _, _, info = env.step(1)

    assert info["T_in"] > 10.0


def test_cost_nonnegative():
    env = ThermalEnv()

    env.reset()

    for _ in range(10):

        _, _, done, _, info = env.step(
            env.action_space.sample()
        )

        assert info["energy_cost"] >= 0

        if done:
            break


def test_reset_reproducible():

    env1 = ThermalEnv(seed=42)
    env2 = ThermalEnv(seed=42)

    o1, _ = env1.reset()
    o2, _ = env2.reset()

    np.testing.assert_array_equal(o1, o2)