import logging
import sys
import sys
import os

PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))


from tion_btle.s3 import S3

logging.basicConfig(level=logging.DEBUG)
_LOGGER = logging.getLogger(__name__)
_LOGGER.setLevel("DEBUG")
try:
    mac = sys.argv[1]
except IndexError:
    mac = "dummy"

device = S3(mac)

result = device.get()

_LOGGER.debug("Result is %s " % result)

_LOGGER.info("Initial state: device is %s, sound is %s, heater is %s, fan_speed is %d, target_temp is %d",
              device.state,
              device.sound,
              device.heater,
              device.fan_speed,
              device.target_temp
              )


