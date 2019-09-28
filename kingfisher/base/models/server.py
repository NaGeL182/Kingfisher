from . import Base
from sqlalchemy import Column, Integer, String, DateTime, FetchedValue, ForeignKey, text
from sqlalchemy.orm import relationship


class Server(Base):
    __tablename__ = "servers"

    guid = Column(Integer, unique=True)
    name = Column(String)
    joined_at = Column(DateTime, nullable=False, server_default=FetchedValue())
    left_at = Column(DateTime, nullable=True, server_default=text('NULL'))

    flags = relationship("ServerFlag", back_populates="server")


class ServerFlag(Base):
    __tablename__ = "server_flags"

    server_id = Column(Integer, ForeignKey('servers.id'))
    name = Column(String)
    value = Column(String, nullable=True, server_default=text('NULL'))

    server = relationship("Server", back_populates="flags")
