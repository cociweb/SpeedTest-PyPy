import asyncio
import aiohttp
import socket
import time
from typing import List
from .utils import generate_payload

class NetworkTester:
    async def measure_latency(self, host: str, samples: int = 4) -> float:
        """Measure latency to a host"""
        latencies = []
        for _ in range(samples):
            start = time.time()
            try:
                reader, writer = await asyncio.open_connection(host, 80)
                writer.close()
                await writer.wait_closed()
                latencies.append((time.time() - start) * 1000)
            except:
                continue
        return sum(latencies) / len(latencies) if latencies else float('inf')

    async def measure_download(self, server, threads: int) -> float:
        """Measure download speed"""
        async def download_chunk():
            async with aiohttp.ClientSession() as session:
                async with session.get(f"{server.url}/download") as response:
                    while True:
                        chunk = await response.content.read(8192)
                        if not chunk:
                            break
                        yield len(chunk)

        total_bytes = 0
        start_time = time.time()
        tasks = [download_chunk() for _ in range(threads)]

        async def process_task(task):
            nonlocal total_bytes
            async for chunk_size in task:
                total_bytes += chunk_size

        await asyncio.gather(*(process_task(task) for task in tasks))
        duration = time.time() - start_time

        return (total_bytes * 8) / (1000000 * duration)  # Mbps

    async def measure_upload(self, server, threads: int) -> float:
        """Measure upload speed"""
        payload = generate_payload(1024 * 1024)  # 1MB chunks

        async def upload_chunk():
            async with aiohttp.ClientSession() as session:
                async with session.post(f"{server.url}/upload", data=payload) as response:
                    await response.read()
                    return len(payload)

        total_bytes = 0
        start_time = time.time()
        tasks = [upload_chunk() for _ in range(threads)]
        results = await asyncio.gather(*tasks)
        total_bytes = sum(results)
        duration = time.time() - start_time

        return (total_bytes * 8) / (1000000 * duration)  # Mbps