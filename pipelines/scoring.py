"""Shared scoring helpers for detector alert prioritization."""


def clamp(value: float, minimum: float = 0.0, maximum: float = 1.0) -> float:
    """Clamp a numeric value to an inclusive range."""
    return max(minimum, min(value, maximum))


def normalized_alert_score(
    primary_excess: float,
    secondary_excess: float,
) -> float:
    """Map two detector-specific excess measures to the shared 60-100 scale."""
    primary = clamp(primary_excess)
    secondary = clamp(secondary_excess)
    return round(60 + 20 * primary + 20 * secondary, 1)
