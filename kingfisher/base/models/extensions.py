from . import Base
from sqlalchemy import Column, Integer, String, Boolean


class Extension(Base):
    __tablename__ = 'extensions'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    enabled = Column(Boolean)
