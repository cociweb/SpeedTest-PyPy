import asyncio
import aiohttp
import socket
import time
import logging
import sys
import os
from typing import List, Optional
from .utils import generate_payload

#logging.basicConfig(
#    level=logging.DEBUG,
#    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
#    handlers=[logging.StreamHandler(sys.stdout)]
#)
logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)

class NetworkTester:
    async def measure_latency(self, host: str, samples: int = 4) -> float:
        """Measure latency to a host using HTTP HEAD requests with fallback"""
        try:
            # Extract host and port
            if ':' in host:
                host, port = host.split(':')
                port = int(port)
            else:
                port = 80

            # Try PING/PONG first
            latencies = []
            for _ in range(samples):
                try:
                    reader, writer = await asyncio.open_connection(host, port)
                    latency = await self._ping_server(reader, writer)
                    if latency is not None:
                        latencies.append(latency)
                    writer.close()
                    await writer.wait_closed()
                except Exception as e:
                    logger.debug(f"PING/PONG latency measurement failed: {e}")
                    continue

            if latencies:
                return sum(latencies) / len(latencies)

            # Fallback to HTTP HEAD requests if PING/PONG fails
            logger.debug("Falling back to HTTP HEAD requests for latency measurement")
            async with aiohttp.ClientSession() as session:
                latencies = []
                for _ in range(samples):
                    try:
                        start_time = time.time() * 1000
                        url = f"http://{host}:{port}/speedtest/upload.php"
                        async with session.head(url) as response:
                            if response.status == 200:
                                end_time = time.time() * 1000
                                latencies.append(end_time - start_time)
                    except Exception as e:
                        logger.debug(f"HTTP latency measurement failed: {e}")
                        continue

                return sum(latencies) / len(latencies) if latencies else float('inf')

        except Exception as e:
            logger.error(f"All latency measurements failed for {host}: {e}")
            return float('inf')
    async def _ping_server(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter) -> Optional[float]:
        """Send PING and wait for PONG response"""
        try:
            start_time = time.time() * 1000  # Convert to milliseconds
            ping_msg = f"PING {int(start_time)}\n"

            # Send PING
            writer.write(ping_msg.encode())
            await writer.drain()

            # Wait for PONG
            response = await reader.readline()
            if not response:
                return None

            response = response.decode().strip()
            if response.startswith("PONG "):
                end_time = time.time() * 1000
                return end_time - start_time

        except Exception as e:
            logger.debug(f"Ping failed: {e}")
            return None

        return None
    async def measure_download(self, server, threads: int) -> float:
        """Measure download speed using direct TCP socket"""
        size = 200 * 1024 * 1024  # 250MB total download size
        chunk_size = 8192  # 8KB chunks
        total_bytes = 0
        tasks = []

        async def download_thread():
            nonlocal total_bytes
            try:
                reader, writer = await asyncio.open_connection(server.host.split(':')[0], int(server.host.split(':')[1]))

                # Send download command
                cmd = f"DOWNLOAD {size}\n"
                writer.write(cmd.encode())
                await writer.drain()

                # Read response in chunks
                bytes_received = 0
                while bytes_received < size:
                    chunk = await reader.read(chunk_size)
                    if not chunk:
                        break
                    bytes_received += len(chunk)
                    total_bytes += len(chunk)
                    if bytes_received % (1024 * 1024 * 10) == 0:  # Every 10MB
                        sys.stdout.write(".")
                        sys.stdout.flush()

                writer.close()
                await writer.wait_closed()

            except Exception as e:
                logger.error(f"Download thread failed: {e}")

        # Start timing
        start_time = time.time()

        # Create and run download threads
        for _ in range(threads):
            tasks.append(asyncio.create_task(download_thread()))

        await asyncio.gather(*tasks)
        duration = time.time() - start_time

        # Calculate speed in Mbps
        if duration > 0 and total_bytes > 0:
            return (total_bytes * 8) / (1000000 * duration)  # Convert to Mbps
        return 0.0

    async def measure_upload(self, server, threads: int) -> float:
        """Measure upload speed using direct TCP socket"""
        size = 15 * 1024 * 1024  # 25MB total upload size
        chunk_size = 8192  # 8KB chunks
        total_bytes = 0
        tasks = []

        async def upload_thread():
            nonlocal total_bytes
            try:
                # Connect to server
                reader, writer = await asyncio.open_connection(*server.host_port)

                # Send upload command
                cmd = f"UPLOAD {size}\n"
                writer.write(cmd.encode())
                await writer.drain()
                total_bytes += len(cmd)

                # Generate random payload once
                payload = bytearray(os.urandom(chunk_size))
                missing = size - len(cmd)

                # Send data in chunks
                while missing > 0:
                    if missing > chunk_size:
                        writer.write(payload)
                        await writer.drain()
                        bytes_sent = chunk_size
                    else:
                        # Last chunk, ensure it ends with newline
                        final_chunk = bytearray(payload[:missing-1])
                        final_chunk.append(ord('\n'))
                        writer.write(final_chunk)
                        await writer.drain()
                        bytes_sent = missing

                    total_bytes += bytes_sent
                    missing -= bytes_sent
                    if total_bytes % (1024 * 1024 * 1) == 0:  # Every 1MB
                        sys.stdout.write(".")
                        sys.stdout.flush()

                # Wait for server response
                response = await reader.readline()
                response = response.decode().strip()
                expected = f"OK {size}"
                if not response.startswith(expected):
                    logger.error(f"Invalid server response: {response}")
                    return

                writer.close()
                await writer.wait_closed()

            except Exception as e:
                logger.error(f"Upload thread failed: {e}")

        # Start timing and run threads
        start_time = time.time()
        for _ in range(threads):
            tasks.append(asyncio.create_task(upload_thread()))

        await asyncio.gather(*tasks)
        duration = time.time() - start_time

        # Calculate speed in Mbps
        if duration > 0 and total_bytes > 0:
            return (total_bytes * 8) / (1000000 * duration)
        return 0.0