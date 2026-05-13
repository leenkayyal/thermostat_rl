import sys
sys.path.insert(0, ".")

from agent.tools import (
    current_temp,
    cost_so_far,
    time_outside_comfort_today,
    vs_yesterday
)

FAKE = [
    {
        "T_in": 19.0,
        "T_out": 5.0,
        "setpoint": 21.0,
        "energy_cost": 0.05,
        "discomfort": 1.0,
        "peak": False
    },
    {
        "T_in": 21.5,
        "T_out": 6.0,
        "setpoint": 21.0,
        "energy_cost": 0.09,
        "discomfort": 0.0,
        "peak": True
    }
]


def test_current_temp_empty():
    assert "No data" in current_temp([])


def test_current_temp_returns_numbers():
    r = current_temp(FAKE)

    assert "21.5" in r or "19.0" in r


def test_cost_total():
    r = cost_so_far(FAKE)

    assert "0.14" in r


def test_comfort_counts():
    r = time_outside_comfort_today(FAKE)

    assert "1 of 2" in r


def test_vs_yesterday_no_data():
    assert "No previous" in vs_yesterday(FAKE, [])