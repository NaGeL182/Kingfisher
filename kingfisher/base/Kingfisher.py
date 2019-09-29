from discord.ext.commands import Bot
import os
import yaml
from logging import config as log_config
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models import Base


class KingfisherBot(Bot):
    def __init__(self, command_prefix, config, **options):
        super().__init__(command_prefix, **options)
        self.config = config
        self._setup_logging()
        self._setup_engine()

    @staticmethod
    def _setup_logging():
        # everything about logging
        # https://docs.python.org/3.7/library/logging.html
        """
        Basically I'm loading the yaml file with logging configuration so we use that.
        """
        path = os.path.dirname(os.path.realpath(__file__))
        logging_conf = open(f"{path}/../config/logging.yaml", 'r')
        log_config.dictConfig(yaml.load(logging_conf, Loader=yaml.SafeLoader))

    def _setup_engine(self):
        # engine creates the basic database connection and ORM
        self.engine = create_engine(self.config.db_url)
        # we gonna use self.Session() to create sessions where we gonna communicate with the DB
        self.Session = sessionmaker(self.engine)

        Base.metadata.create_all(self.engine)

