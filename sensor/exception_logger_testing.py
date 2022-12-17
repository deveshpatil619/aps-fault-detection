from sensor.logger import logging
from sensor.exception import SensorException
import os,sys


def test_log_exception():
    try:
        logging.info("Starting the test_log_exception")
        result = 3/0
        print(result)
        logging.info("Starting the test_log_exception")
    except Exception as e:
        logging.debug("stopping the test logger and exception")
        raise SensorException(e, sys)

if __name__ == "__main__":
        try:
            test_log_exception()
        except Exception as e:
            print(e) 




