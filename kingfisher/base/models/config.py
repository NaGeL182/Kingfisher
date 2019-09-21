from . import Base
from sqlalchemy import Column, Integer, String


class Config(Base):
    __tablename__ = 'configs'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    value = Column(String)
