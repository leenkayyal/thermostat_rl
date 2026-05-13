"""
agent/tools.py

Tool functions for extracting real metrics from thermostat episodes.
"""


def current_temp(episode_log: list) -> str:
    """Return latest temperature readings."""

    if not episode_log:
        return "No data recorded yet."

    last = episode_log[-1]

    if last["T_in"] < last["setpoint"]:
        direction = "heating"
    elif last["T_in"] > last["setpoint"]:
        direction = "cooling"
    else:
        direction = "holding"

    return (
        f"Indoor: {last['T_in']:.1f}°C  "
        f"Outdoor: {last['T_out']:.1f}°C  "
        f"Setpoint: {last['setpoint']:.1f}°C  "
        f"HVAC: {direction}"
    )


def time_outside_comfort_today(episode_log: list) -> str:
    """How many hours outside comfort band."""

    if not episode_log:
        return "No data yet."

    violated = [
        s for s in episode_log
        if s["T_in"] < 20.0 or s["T_in"] > 22.0
    ]

    pct = 100 * len(violated) / len(episode_log)

    too_cold = sum(
        1 for s in episode_log
        if s["T_in"] < 20.0
    )

    too_hot = sum(
        1 for s in episode_log
        if s["T_in"] > 22.0
    )

    return (
        f"{len(violated)} of {len(episode_log)} hours outside comfort "
        f"({pct:.0f}%) — "
        f"{too_cold}h too cold, "
        f"{too_hot}h too warm"
    )


def cost_so_far(episode_log: list) -> str:
    """Cumulative energy cost."""

    if not episode_log:
        return "No cost recorded yet."

    peak_cost = sum(
        s["energy_cost"]
        for s in episode_log
        if s.get("peak")
    )

    offpeak_cost = sum(
        s["energy_cost"]
        for s in episode_log
        if not s.get("peak")
    )

    total = peak_cost + offpeak_cost

    return (
        f"Total so far: ${total:.4f}  "
        f"(peak-rate: ${peak_cost:.4f}  "
        f"off-peak: ${offpeak_cost:.4f})"
    )


def vs_yesterday(
    episode_log: list,
    yesterday_log: list
) -> str:
    """Compare today's performance to yesterday."""

    if not yesterday_log:
        return "No previous episode to compare against."

    today_cost = sum(
        s["energy_cost"] for s in episode_log
    )

    yest_cost = sum(
        s["energy_cost"] for s in yesterday_log
    )

    today_dis = sum(
        s["discomfort"] for s in episode_log
    )

    yest_dis = sum(
        s["discomfort"] for s in yesterday_log
    )

    cost_arrow = (
        "↑ worse"
        if today_cost > yest_cost
        else "↓ better"
    )

    dis_arrow = (
        "↑ worse"
        if today_dis > yest_dis
        else "↓ better"
    )

    return (
        f"Cost: ${today_cost:.4f} today vs "
        f"${yest_cost:.4f} yesterday — {cost_arrow}. "
        f"Discomfort: {today_dis:.2f} vs "
        f"{yest_dis:.2f} — {dis_arrow}."
    )