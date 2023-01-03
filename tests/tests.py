import time
import unittest
import mutagen
import tempfile
from mutagen.mp3 import MP3


class CutAudioTests(unittest.TestCase):
    def setUp(self):
        self.expected_duration = 10

    def test_duration(self):
        actual_duration = int(MP3("cut_test_cut.mp3").info.length)
        self.assertEqual(self.expected_duration, actual_duration)


class SpeedUpTests(unittest.TestCase):
    def setUp(self):
        self.expected_length = 10

    def test_speedup_x2(self):
        actual_length = int(MP3("speedup_test_speedup.mp3").info.length)
        self.assertEqual(actual_length, self.expected_length)


class SlowDownTests(unittest.TestCase):
    def setUp(self):
        self.expected_length = 40

    def test_slowdown_x05(self):
        actual_length = int(MP3("slowdown_test_slowdown.mp3").info.length)
        self.assertEqual(actual_length, self.expected_length)


if __name__ == "__main__":
    unittest.main()
