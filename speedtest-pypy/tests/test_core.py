import unittest
from unittest.mock import patch, MagicMock
from speedtest-pypy.core import SpeedTest
import asyncio

class TestSpeedTest(unittest.TestCase):
    def setUp(self):
        self.speed_test = SpeedTest()

    @patch('aiohttp.ClientSession.get')
    async def test_get_ip_info(self, mock_get):
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "ip": "1.1.1.1",
            "location": {"latitude": 0, "longitude": 0}
        }
        mock_get.return_value.__aenter__.return_value = mock_response

        result = await self.speed_test.get_ip_info()
        self.assertEqual(result["ip"], "1.1.1.1")

    # Add more test cases...

if __name__ == '__main__':
    unittest.main()