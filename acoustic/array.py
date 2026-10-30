"""Microphone array geometry.

Positions MUST come from your own tape-measure + tap-test map, not a datasheet.
Edit MIC_POSITIONS_M after measuring the installed board.
"""
import numpy as np

SPEED_OF_SOUND = 343.0  # m/s at ~20 C; use speed_of_sound(temp_c) in the field

# Placeholder: generic 4-mic circle, 32 mm radius. Replace with measured values.
MIC_POSITIONS_M = np.array([
    [0.032, 0.0],
    [0.0, 0.032],
    [-0.032, 0.0],
    [0.0, -0.032],
])


def speed_of_sound(temp_c: float) -> float:
    """Speed of sound in dry air; matters in a Canadian winter (-20 C -> ~319 m/s)."""
    return 331.3 * np.sqrt(1.0 + temp_c / 273.15)


def expected_tdoa(azimuth_deg: float, mics=MIC_POSITIONS_M, c=SPEED_OF_SOUND) -> np.ndarray:
    """Far-field time difference of arrival of every mic relative to mic 0 (seconds)."""
    az = np.deg2rad(azimuth_deg)
    direction = np.array([np.cos(az), np.sin(az)])
    # A plane wave from `direction` reaches mics with larger projection first.
    delays = -(mics @ direction) / c
    return delays - delays[0]
