import redis
import logging.config
from constants import LOGGING_CONFIG
import os
import string


class Config:
    logging.config.dictConfig(LOGGING_CONFIG)


config = Config()
