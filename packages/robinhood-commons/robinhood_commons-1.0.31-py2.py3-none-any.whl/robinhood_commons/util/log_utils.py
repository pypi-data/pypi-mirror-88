import logging
from logging import Logger
from logging.handlers import TimedRotatingFileHandler

from robinhood_commons.log.gzip_rotator import GZipRotator
from robinhood_commons.util.io_utils import ensure_exists


def create_logger(path: str) -> Logger:
    """
    Creates a rotating log
    """

    ensure_exists(path)

    log_name: str = path.split('/')[-1]
    logger = logging.getLogger(log_name.split('.')[0])
    logger.setLevel(logging.INFO)

    log_handler = TimedRotatingFileHandler(filename=path, when='h')

    log_formatter = logging.Formatter('%(asctime)s [%(levelname)s] [%(name)s] %(message)s')
    log_handler.setFormatter(log_formatter)
    log_handler.setLevel(logging.INFO)
    log_handler.rotator = GZipRotator()

    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.INFO)
    stream_handler.setFormatter(log_formatter)

    logger.addHandler(stream_handler)
    logger.addHandler(log_handler)

    return logger


if __name__ == '__main__':
    from robinhood_commons.util.random_utils import random_float

    path: str = f'/tmp/output/log_utils.{random_float(0, 100)}.log'

    the_logger: Logger = create_logger(name=path)
    the_logger.info('help!')

    import os
    os.remove(path=path)
