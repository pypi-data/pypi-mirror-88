import sys
import os
import logging
import asyncio

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/..")

from tion_btle import s3


logging.basicConfig(level=logging.DEBUG)
_LOGGER = logging.getLogger(__name__)

mac = sys.argv[1]
loop = asyncio.get_event_loop()


async def run():
    device = s3.S3(mac)
    _LOGGER.debug(await device.get())
    # await asyncio.sleep(10)
    await device.set({'fan_speed': 2})
    # await device.pair()

_LOGGER.debug("Going to test s3 with mac %s" % mac)
loop.run_until_complete(run())

