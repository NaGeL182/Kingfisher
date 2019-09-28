from . import Base
from sqlalchemy import Column, Integer, String


class Config(Base):

    name = Column(String)
    value = Column(String)
