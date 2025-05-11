import unittest
from unittest.mock import patch, MagicMock
from speedtest_pypy.network import NetworkTester
import asyncio

class TestNetworkTester(unittest.TestCase):
    def setUp(self):
        self.network_tester = NetworkTester()

    @patch('asyncio.open_connection')
    async def test_measure_latency(self, mock_open_connection):
        mock_writer = MagicMock()
        mock_reader = MagicMock()
        mock_open_connection.return_value = (mock_reader, mock_writer)

        latency = await self.network_tester.measure_latency("example.com")
        self.assertIsInstance(latency, float)

    # Add more test cases...

if __name__ == '__main__':
    unittest.main()