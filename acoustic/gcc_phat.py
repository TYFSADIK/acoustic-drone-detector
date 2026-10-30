"""GCC-PHAT time-delay estimation and azimuth search."""
import numpy as np

from .array import MIC_POSITIONS_M, SPEED_OF_SOUND, expected_tdoa


def gcc_phat(sig: np.ndarray, ref: np.ndarray, fs: int, max_tau: float | None = None,
             interp: int = 16) -> tuple[float, np.ndarray]:
    """Delay of `sig` relative to `ref` in seconds, using PHAT weighting.

    PHAT whitens the cross-spectrum so the strong rotor harmonics don't
    dominate; every frequency votes equally on the delay.
    """
    n = sig.shape[0] + ref.shape[0]
    SIG = np.fft.rfft(sig, n=n)
    REF = np.fft.rfft(ref, n=n)
    R = SIG * np.conj(REF)
    R /= np.abs(R) + 1e-12
    cc = np.fft.irfft(R, n=interp * n)
    max_shift = interp * n // 2
    if max_tau is not None:
        max_shift = min(int(interp * fs * max_tau), max_shift)
    cc = np.concatenate((cc[-max_shift:], cc[:max_shift + 1]))
    shift = np.argmax(np.abs(cc)) - max_shift
    return shift / float(interp * fs), cc


def estimate_azimuth(frames: np.ndarray, fs: int, mics=MIC_POSITIONS_M,
                     c=SPEED_OF_SOUND, step_deg: float = 1.0) -> tuple[float, float]:
    """Estimate azimuth (deg) from a (n_mics, n_samples) frame.

    Measures pairwise TDOAs to mic 0, then grid-searches the azimuth whose
    expected TDOAs best match. Returns (azimuth_deg, rms_error_seconds).
    """
    aperture = np.max(np.linalg.norm(mics - mics[0], axis=1))
    max_tau = aperture / c * 1.2
    measured = np.zeros(len(mics))
    for i in range(1, len(mics)):
        measured[i], _ = gcc_phat(frames[i], frames[0], fs, max_tau=max_tau)
    grid = np.arange(0.0, 360.0, step_deg)
    errors = np.array([np.sqrt(np.mean((expected_tdoa(a, mics, c) - measured) ** 2)) for a in grid])
    best = int(np.argmin(errors))
    return float(grid[best]), float(errors[best])
