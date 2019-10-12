from __future__ import annotations

import os
from contextlib import contextmanager
from logging import config as log_config, getLogger
from typing import Iterator

import yaml
from discord.ext.commands import Bot
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import sessionmaker, scoped_session, Session


class KingfisherBot(Bot):
    def __init__(self, command_prefix, config, **options):
        super().__init__(command_prefix, **options)
        self.config = config
        self._setup_logging()
        self._setup_database()

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

    def _setup_database(self):
        # engine creates the basic database connection and ORM
        self._engine = create_engine(self.config.db_url)
        # we creating contectual Thrad local sessons:
        # https://docs.sqlalchemy.org/en/13/orm/contextual.html#unitofwork-contextual
        self._session_factory = sessionmaker(bind=self._engine)

    def _create_session(self) -> Session:
        return scoped_session(self._session_factory)()

    # https://docs.sqlalchemy.org/en/13/orm/session_basics.html#when-do-i-construct-a-session-when-do-i-commit-it-and-when-do-i-close-it
    @contextmanager
    def get_session(self) -> Iterator[Session]:
        session = self._create_session()
        try:
            yield session
            session.commit()
        except SQLAlchemyError as e:
            logging = getLogger(__name__)
            logging.error(e)
            session.rollback()
        finally:
            session.close()

