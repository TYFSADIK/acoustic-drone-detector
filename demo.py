"""Run: python demo.py  -> detects a simulated drone and estimates its bearing."""
from acoustic import harmonics
from acoustic.gcc_phat import estimate_azimuth
from acoustic.simulate import array_capture, bird_chirp, rotor_signal

FS = 16000

for name, src in [("drone", rotor_signal(FS, 1.0)), ("bird", bird_chirp(FS, 1.0))]:
    res = harmonics.detect(src, FS)
    print(f"{name:5s}: drone={res.is_drone} f0={res.f0_hz:.0f}Hz comb={res.comb_score:.2f} harmonics={res.n_harmonics}")

true_az = 125.0
frames = array_capture(rotor_signal(FS, 0.5), FS, true_az)
az, err = estimate_azimuth(frames, FS)
print(f"bearing: true={true_az:.0f} deg  estimated={az:.0f} deg  (tdoa rms err {err*1e6:.1f} us)")
