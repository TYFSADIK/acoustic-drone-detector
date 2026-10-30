# Passive Acoustic Drone Detector

Private research repo. MEMS microphone array (ReSpeaker 4-mic on a Raspberry Pi) that detects multirotor rotor harmonics, rejects birds and aircraft, and estimates direction of arrival with GCC-PHAT.

Full write-up: [`docs/project-page.md`](docs/project-page.md)

## What's here

| File | Purpose |
|---|---|
| `acoustic/array.py` | Mic geometry (**replace with your measured positions**), temperature-corrected speed of sound |
| `acoustic/harmonics.py` | Harmonic comb detector: finds the blade-pass f0 and scores how much energy sits on its harmonics |
| `acoustic/gcc_phat.py` | GCC-PHAT delay estimation and azimuth grid search |
| `acoustic/simulate.py` | Synthetic rotor, bird chirp, and multi-mic capture, so you can develop without flying |
| `demo.py` | End-to-end demo on simulated data |

## Quickstart

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python demo.py
python -m unittest -v
```

## Next steps
- [ ] Capture 4-channel audio on the Pi (`arecord -D ac108 -c 4 -r 16000 -f S16_LE`) and feed it to `estimate_azimuth`
- [ ] Put the tap-test channel map and measured mic positions into `array.py`
- [ ] Log every detection with a timestamp and compare it with flight-log ground truth (bearing error, Pd, false alarms per hour)
- [ ] Add an aircraft rejector (low f0 and slowly drifting spectrum) and record a bird/wind negative set
- [ ] Use `speed_of_sound(temp_c)` from a temperature sensor during winter runs

Receive-only and detection-only. See the Legal & Safety Notes in the project page.
