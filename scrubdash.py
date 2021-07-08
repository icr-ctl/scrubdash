#!/usr/bin/env python3

from multiprocessing import Process, Queue
from asyncio_server import asyncio_server
from multi_page_dash_server.dash_server import start_dash
import argparse
import logging

parser = argparse.ArgumentParser()
parser.add_argument('ip')
parser.add_argument('port')
args = parser.parse_args()
IP = args.ip
PORT = int(args.port)

logging.basicConfig(level=logging.INFO,
                    format='[%(levelname)s] %(message)s (%(name)s)')
log = logging.getLogger('main')

if __name__ == '__main__':
    q = Queue()
    asyncio_server = asyncio_server(q, IP, PORT)
    asyncio = Process(target=asyncio_server.start_server)
    dash = Process(target=start_dash, args=(q,))
    asyncio.start()
    dash.start()

    try:
        asyncio.join()
        dash.join()
    except KeyboardInterrupt:
        # waits for asyncio and dash to shut down
        while asyncio.is_alive() or dash.is_alive():
            pass
        log.info('Successfully shut down scrubdash.')
