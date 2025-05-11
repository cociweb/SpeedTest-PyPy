import argparse
import asyncio
import json
import logging
import sys
from .core import SpeedTest

# Enhanced logging configuration
#logging.basicConfig(
#    level=logging.DEBUG,
#    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
#    handlers=[logging.StreamHandler(sys.stdout)]
#)
logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)
async def _async_main():
    parser = argparse.ArgumentParser(description='SpeedTest++ Python Implementation')
    parser.add_argument('--latency', action='store_true', help='Perform latency test only')
    parser.add_argument('--download', action='store_true', help='Perform download test only')
    parser.add_argument('--upload', action='store_true', help='Perform upload test only')
    parser.add_argument('--server', type=int, help='Use specific server ID')
    parser.add_argument('--threads', type=int, default=4, help='Number of threads to use')
    parser.add_argument('--json', action='store_true', help='Output in JSON format')
    args = parser.parse_args()

    speed_test = SpeedTest()
    try:
        print("Retrieving speedtest.net configuration...", flush=True)
        await speed_test.initialize()

        logger.debug(f"IP Info received: {speed_test.ip_info}")

        if not speed_test.ip_info:
            logger.error("IP info is None")
            return 1

        # Check required fields with nested structure
        ip_addr = speed_test.ip_info.get('ip')
        company_name = speed_test.ip_info.get('company', {}).get('name')
        location = speed_test.ip_info.get('location')

        if not all([ip_addr, company_name, location]):
            logger.error("Missing required IP info fields")
            logger.debug(f"IP: {ip_addr}, Company: {company_name}, Location: {location}")
            return 1

        print(f"Testing from {company_name} ({ip_addr})...", flush=True)


        print("Retrieving speedtest.net server list...", flush=True)
        print("Selecting best server based on ping...", flush=True)
        await speed_test.find_best_server()

        server = speed_test.selected_server
        if not server:
            logger.error("No server selected")
            return 1

        print(f"Hosted by {server.sponsor} ({server.name}) [{server.distance:.2f} km]: "
              f"{server.latency:.3f} ms", flush=True)


        if not any([args.latency, args.upload]) or args.download:
            sys.stdout.write("Testing download speed")
            sys.stdout.flush()
            download_speed = await speed_test.test_download(args.threads)
            print("\nDownload: %.2f Mbit/s" % download_speed, flush=True)

        if not any([args.latency, args.download]) or args.upload:
            sys.stdout.write("Testing upload speed")
            sys.stdout.flush()
            upload_speed = await speed_test.test_upload(args.threads)
            print("\nUpload: %.2f Mbit/s" % upload_speed, flush=True)

    except Exception as e:
        logger.error(f"Test failed: {str(e)}")
        logger.debug("Exception details:", exc_info=True)
        return 1

    return 0

def main():
    """Synchronous entry point for the command-line interface"""
    return asyncio.run(_async_main())

if __name__ == '__main__':
    main()