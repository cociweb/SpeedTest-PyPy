from dataclasses import dataclass
from .models import ServerInfo
from typing import List, Optional, Dict
import asyncio
import aiohttp
import socket
import time
import json
import xml.etree.ElementTree as ET
from concurrent.futures import ThreadPoolExecutor
from .network import NetworkTester
from .utils import calculate_distance, generate_payload


class SpeedTest:
    def __init__(self, min_server_version: float = 2.3):
        self.min_server_version = min_server_version
        self.servers: List[ServerInfo] = []
        self.selected_server: Optional[ServerInfo] = None
        self.ip_info: Dict = {}
        self.network = NetworkTester()

    async def initialize(self):
        """Initialize speed test by getting IP info and server list"""
        await self.get_ip_info()
        await self.get_server_list()

    async def get_ip_info(self):
        """Fetch IP information"""
        async with aiohttp.ClientSession() as session:
            async with session.get('https://api.ipapi.is/') as response:
                self.ip_info = await response.json()
                return self.ip_info

    async def get_server_list(self):
        """Fetch and parse server list"""
        async with aiohttp.ClientSession() as session:
            async with session.get('https://www.speedtest.net/speedtest-servers.php') as response:
                content = await response.text()
                root = ET.fromstring(content)
                for server in root.findall(".//server"):
                    self.servers.append(ServerInfo(
                        id=int(server.get("id")),
                        url=server.get("url"),
                        lat=float(server.get("lat")),
                        lon=float(server.get("lon")),
                        name=server.get("name"),
                        country=server.get("country"),
                        sponsor=server.get("sponsor"),
                        host=server.get("host")
                    ))


    async def test_latency(self, server: ServerInfo) -> float:
        """Test latency to a specific server"""
        return await self.network.measure_latency(server.host)

    async def find_best_server(self):
        """Find the best server based on latency and distance"""
        tasks = [self.test_latency(server) for server in self.servers[:10]]
        latencies = await asyncio.gather(*tasks)

        for server, latency in zip(self.servers[:10], latencies):
            server.latency = latency
            server.distance = calculate_distance(
                self.ip_info['location']['latitude'],
                self.ip_info['location']['longitude'],
                server.lat,
                server.lon
            )

        self.selected_server = min(self.servers[:10], key=lambda x: x.latency)
        return self.selected_server

    async def test_download(self, threads: int = 4) -> float:
        """Perform download speed test"""
        return await self.network.measure_download(self.selected_server, threads)

    async def test_upload(self, threads: int = 4) -> float:
        """Perform upload speed test"""
        return await self.network.measure_upload(self.selected_server, threads)

    async def run_complete_test(self, threads: int = 4):
        """Run a complete speed test"""
        await self.initialize()
        await self.find_best_server()

        download_speed = await self.test_download(threads)
        upload_speed = await self.test_upload(threads)

        return {
            'server': self.selected_server,
            'latency': self.selected_server.latency,
            'download': download_speed,
            'upload': upload_speed,
            'ip_info': self.ip_info
        }