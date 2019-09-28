from . import Base
from sqlalchemy import Column, Integer, String, Boolean


class Extension(Base):
    __tablename__ = 'extensions'

    name = Column(String)
    enabled = Column(Boolean)
