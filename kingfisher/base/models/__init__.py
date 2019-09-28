from sqlalchemy.ext.declarative import declarative_base, declared_attr
from sqlalchemy import Column, Integer, DateTime, FetchedValue, func


class BaseClass(object):
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, nullable=False, server_default=FetchedValue())
    # PostgresSQL doesn't have ON UPDATE clause for columns so lets do that on python side
    updated_at = Column(DateTime, nullable=True, server_default=FetchedValue(), onupdate=func.now())


Base = declarative_base(cls=BaseClass)
