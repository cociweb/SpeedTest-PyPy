import argparse
import asyncio
import json
from .core import SpeedTest

async def main():
    parser = argparse.ArgumentParser(description='SpeedTest++ Python Implementation')
    parser.add_argument('--latency', action='store_true', help='Perform latency test only')
    parser.add_argument('--download', action='store_true', help='Perform download test only')
    parser.add_argument('--upload', action='store_true', help='Perform upload test only')
    parser.add_argument('--server', type=int, help='Use specific server ID')
    parser.add_argument('--threads', type=int, default=4, help='Number of threads to use')
    parser.add_argument('--json', action='store_true', help='Output in JSON format')
    args = parser.parse_args()

    speed_test = SpeedTest()
    await speed_test.initialize()

    if args.server:
        speed_test.selected_server = next((s for s in speed_test.servers if s.id == args.server), None)
    else:
        await speed_test.find_best_server()

    results = {}

    if args.latency or (not any([args.download, args.upload])):
        results['latency'] = speed_test.selected_server.latency

    if args.download or (not any([args.latency, args.upload])):
        results['download'] = await speed_test.test_download(args.threads)

    if args.upload or (not any([args.latency, args.download])):
        results['upload'] = await speed_test.test_upload(args.threads)

    if args.json:
        print(json.dumps(results))
    else:
        if 'latency' in results:
            print(f"Latency: {results['latency']:.2f} ms")
        if 'download' in results:
            print(f"Download: {results['download']:.2f} Mbps")
        if 'upload' in results:
            print(f"Upload: {results['upload']:.2f} Mbps")

if __name__ == '__main__':
    asyncio.run(main())