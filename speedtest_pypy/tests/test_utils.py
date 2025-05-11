import unittest
from speedtest_pypy.utils import calculate_distance, generate_payload

class TestUtils(unittest.TestCase):
    def test_calculate_distance(self):
        # Test distance calculation between New York and London
        ny_lat, ny_lon = 40.7128, -74.0060
        london_lat, london_lon = 51.5074, -0.1278

        distance = calculate_distance(ny_lat, ny_lon, london_lat, london_lon)
        # Approximately 5570 km
        self.assertAlmostEqual(distance, 5570, delta=100)

    def test_generate_payload(self):
        size = 1024
        payload = generate_payload(size)
        self.assertEqual(len(payload), size)
        self.assertIsInstance(payload, bytes)

    # Add more test cases...

if __name__ == '__main__':
    unittest.main()