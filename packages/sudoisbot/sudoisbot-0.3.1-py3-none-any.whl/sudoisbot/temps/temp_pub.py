#!/usr/bin/python3 -u

import time
from datetime import datetime

from loguru import logger

from sudoisbot.network.pub import Publisher
from sudoisbot.temps.sensors import TempSensor
from sudoisbot.temps.sensors import SensorDisconnectedError, NoSensorDetectedError


class TempPublisher(Publisher):
    def __init__(self, addr, freq, location, sensors):
        super().__init__(addr, b"temp", None, freq)

        logger.info(f"HWM: {self.socket.get_hwm()}")

        # might ditch 'frequency' here..
        self.tags = {'location': location, 'frequency': freq}
        self.sensors = sensors

    def publish(self):
        for sensor in self.sensors:

            reading = sensor.read()
            now = datetime.now().isoformat()

            for measurement, value in reading['measurements'].items():
                msg = {
                    'measurement': measurement,
                    'time': now,
                    'tags': {**self.tags, **sensor.as_dict()},
                    'fields': {
                        'value': float(value)
                    }
                }
                logmsg = f"{msg['tags']['name']} {measurement}: {value}"
                logger.log("TEMP", logmsg)
                self.pub(msg)

def main(config):
    broker = config['broker']
    freq = config['frequency']
    loc = config['location']

    log_no = config.get('sensor_log_no', 9)
    logger.level("TEMP", no=log_no, color="<green>")
    logger.info(f"logging level TEMP on no {log_no}")

    while True:
        try:
            conf_sensors = config['sensors']['temp']
            sensors = [TempSensor.from_kind(**a) for a in conf_sensors]
            for sensor in sensors:
                logger.info(f"loaded sensor: {sensor}")

            with TempPublisher(broker, freq, loc, sensors) as publisher:
                publisher.loop()
            return 0
        except NoSensorDetectedError as e:
            logger.error(e)
            return 1
        except SensorDisconnectedError as e:
            # especially usb sensors can be unplugged for a short time
            # for various reasons
            logger.exception(e)
            logger.info("waiting 30s for sensor to come back")
            time.sleep(30.0)
            continue
        except KeyboardInterrupt:
            logger.info("Exiting..")
            return 0
