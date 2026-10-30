import unittest

from acoustic import harmonics
from acoustic.gcc_phat import estimate_azimuth
from acoustic.simulate import array_capture, bird_chirp, rotor_signal

FS = 16000


class TestAcoustic(unittest.TestCase):
    def test_drone_detected_bird_rejected(self):
        self.assertTrue(harmonics.detect(rotor_signal(FS, 1.0), FS).is_drone)
        self.assertFalse(harmonics.detect(bird_chirp(FS, 1.0), FS).is_drone)

    def test_bearing_within_10_deg(self):
        for true_az in (30, 125, 260):
            az, _ = estimate_azimuth(array_capture(rotor_signal(FS, 0.5), FS, true_az), FS)
            diff = abs((az - true_az + 180) % 360 - 180)
            self.assertLess(diff, 10, f"true {true_az} est {az}")


if __name__ == "__main__":
    unittest.main()
