"""Synthetic test signals so the pipeline can be developed without a drone."""
import numpy as np

from .array import MIC_POSITIONS_M, SPEED_OF_SOUND


def rotor_signal(fs, seconds, f0=180.0, n_harm=10, rng=None):
    rng = rng or np.random.default_rng(0)
    t = np.arange(int(fs * seconds)) / fs
    jitter = 1 + 0.005 * np.sin(2 * np.pi * 0.7 * t)  # throttle wobble
    phase = 2 * np.pi * f0 * np.cumsum(jitter) / fs
    return sum((1.0 / k) * np.sin(k * phase + rng.uniform(0, 2 * np.pi)) for k in range(1, n_harm + 1))


def bird_chirp(fs, seconds):
    t = np.arange(int(fs * seconds)) / fs
    f = 2500 + 1500 * np.sin(2 * np.pi * 3 * t)
    return np.sin(2 * np.pi * np.cumsum(f) / fs) * (np.sin(2 * np.pi * 6 * t) > 0)


def array_capture(source, fs, azimuth_deg, mics=MIC_POSITIONS_M, c=SPEED_OF_SOUND,
                  snr_db=10.0, rng=None):
    """Delay a mono source onto each mic (fractional delay via FFT) and add noise."""
    rng = rng or np.random.default_rng(1)
    az = np.deg2rad(azimuth_deg)
    d = np.array([np.cos(az), np.sin(az)])
    delays = -(mics @ d) / c
    n = len(source)
    freqs = np.fft.rfftfreq(n, 1 / fs)
    S = np.fft.rfft(source)
    out = np.stack([np.fft.irfft(S * np.exp(-2j * np.pi * freqs * tau), n=n) for tau in delays])
    noise_p = np.mean(source ** 2) / 10 ** (snr_db / 10)
    return out + rng.normal(0, np.sqrt(noise_p), out.shape)
