import discord
from discord.ext.commands import Bot
import logging
from logging.handlers import TimedRotatingFileHandler
from logging import StreamHandler
from sys import stdout
from pprint import pprint
import os
import yaml
from logging import config as log_config


class KingfisherBot(Bot):
    def __init__(self, command_prefix, db, config, **options):
        super().__init__(command_prefix, **options)
        self.db = db
        self.config = config
        self._setup_logging()

    @staticmethod
    def _setup_logging():
        # everything about logging
        # https://docs.python.org/3.7/library/logging.html
        """
        Basically I'm logging the yaml file with logging configuration so we use that.
        """
        path = os.path.dirname(os.path.realpath(__file__))
        logging_conf = open(f"{path}/../config/logging.yaml", 'r')
        log_config.dictConfig(yaml.load(logging_conf, Loader=yaml.SafeLoader))


