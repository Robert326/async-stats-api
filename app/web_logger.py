import logging
from logging.handlers import RotatingFileHandler
import time

class UTCFormatter(logging.Formatter):
    converter = time.gmtime
    def formatTime(self, record, datefmt=None):
        ct = self.converter(record.created)
        if datefmt:
            t = time.strftime(datefmt, ct)
        else:
            t = time.strftime("%Y-%m-%d %H:%M:%S", ct)
        return t

def get_logger(name="webserver"):
    """Returnez un logger configurat pentru a scrie in fisierul webserver.log"""
    logger = logging.getLogger(name)

    if not logger.handlers:
        logger.setLevel(logging.INFO)

        handler = RotatingFileHandler(
            "webserver.log",
            maxBytes=1*1024*1024,
            backupCount=5
        )
        formatter = UTCFormatter("%(asctime)s - %(levelname)s - %(message)s")
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    return logger
