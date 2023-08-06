# -*- coding: utf-8 -*-
import logging


def get_logger(name: str, level=logging.INFO, handler=logging.StreamHandler()):
    LOG_FORMAT = "%(asctime)s.%(msecs)03d - %(levelname)s - [%(processName)s|%(threadName)s] - [%(filename)s - %(funcName)s] - line %(lineno)s: %(message)s"
    DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
    logger = logging.getLogger(name)  # __name__ or <cls name>.__name__
    logger.setLevel(level=level)
    formatter = logging.Formatter(fmt=LOG_FORMAT, datefmt=DATE_FORMAT)
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger


def get_debug_logger(name):
    return get_logger(name, level=logging.DEBUG)


def get_warn_logger(name):
    return get_logger(name, level=logging.WARN)


def get_error_logger(name):
    return get_logger(name, level=logging.ERROR)


if __name__ == '__main__':
    # logging定义可以放在文件的头部
    logging = get_logger(__name__)
    logging.info("test")
