from models import MetricPoint


def calculate_momentum_score(history: list[MetricPoint]) -> float:
    if len(history) < 2:
        return 0.0
    first = history[0]
    last = history[-1]
    delta_stars = last.stars - first.stars
    delta_days = (last.metric_date - first.metric_date).days
    if delta_days == 0:
        return 0.0
    stars_per_day = delta_stars / delta_days
    return stars_per_day
