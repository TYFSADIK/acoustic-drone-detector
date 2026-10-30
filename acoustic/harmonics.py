"""Rotor harmonic comb detector.

Multirotors produce a blade-pass fundamental (~100-400 Hz) with a comb of
integer harmonics. Birds (chirps, no stable comb) and aircraft (low, broadband,
slowly varying) score poorly against a harmonic comb.
"""
from dataclasses import dataclass

import numpy as np


@dataclass
class HarmonicResult:
    is_drone: bool
    f0_hz: float
    comb_score: float      # fraction of band energy explained by the comb
    n_harmonics: int


def spectrum(x: np.ndarray, fs: int) -> tuple[np.ndarray, np.ndarray]:
    win = np.hanning(len(x))
    mag = np.abs(np.fft.rfft(x * win))
    freqs = np.fft.rfftfreq(len(x), 1.0 / fs)
    return freqs, mag ** 2


def comb_score(freqs, power, f0, n_harm=8, bw_hz=6.0, fmax=4000.0):
    band = (freqs > 50) & (freqs < fmax)
    total = power[band].sum() + 1e-12
    comb = 0.0
    hits = 0
    for k in range(1, n_harm + 1):
        fk = k * f0
        if fk >= fmax:
            break
        sel = np.abs(freqs - fk) <= bw_hz
        e = power[sel].sum()
        comb += e
        # count a harmonic as present if it stands above the local floor
        local = (np.abs(freqs - fk) <= 5 * bw_hz) & ~sel
        if local.any() and e / max(sel.sum(), 1) > 4 * power[local].mean():
            hits += 1
    return comb / total, hits


def detect(x: np.ndarray, fs: int, f0_range=(80.0, 400.0), threshold=0.35,
           min_harmonics=3) -> HarmonicResult:
    """Search fundamentals in f0_range and report the best-fitting comb."""
    freqs, power = spectrum(x, fs)
    best = (0.0, 0.0, 0)
    for f0 in np.arange(f0_range[0], f0_range[1], 1.0):
        score, hits = comb_score(freqs, power, f0)
        if score > best[1]:
            best = (f0, score, hits)
    f0, score, hits = best
    return HarmonicResult(score >= threshold and hits >= min_harmonics, float(f0), float(score), hits)
