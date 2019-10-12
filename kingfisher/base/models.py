from __future__ import annotations

from sqlalchemy import Column, Integer, DateTime, func, text, String, Boolean, ForeignKey, Table, BigInteger
from sqlalchemy.ext.declarative import declarative_base, declared_attr
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship


# I hate this setup
# The whole 1 file many classes thing
# but this is the only way that i know this whole SQlAlchemy thing works.


class BaseClass(object):
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    # PostgresSQL doesn't have ON UPDATE clause for columns so lets do that on python side
    updated_at = Column(DateTime, nullable=True, server_default=text("NULL"), onupdate=func.now())


Base = declarative_base(cls=BaseClass)


class Config(Base):

    name = Column(String)
    value = Column(String)


class Extension(Base):
    __tablename__ = 'extensions'

    name = Column(String)
    enabled = Column(Boolean)


class Server(Base):
    __tablename__ = "servers"

    # Big Integer cuz discord has a big Dick
    # pfff, naj just the ID is 18 character long integer.
    sid = Column(BigInteger, unique=True, nullable=False)
    name = Column(String)
    joined_at = Column(DateTime, nullable=False, server_default=func.now())
    left_at = Column(DateTime, nullable=True, server_default=text('NULL'))

    flags = relationship("ServerFlag", back_populates="server")
    roles = relationship("Role", back_populates="server")
    members = relationship("Member", back_populates="server")
    server_configs = relationship("ServerConfig", back_populates="server")


class ServerConfig(Base):
    __tablename__ = "server_config"

    server_id = Column(Integer, ForeignKey('servers.id'))
    name = Column(String)
    value = Column(String)

    server = relationship("Server", back_populates="server_configs")


member2Role_table = Table(
    'member2role',
    Base.metadata,
    Column('member_id', Integer, ForeignKey('members.id')),
    Column('role_id', Integer, ForeignKey('roles.id'))
)


class Role(Base):
    __tablename__ = "roles"

    rid = Column(BigInteger, unique=True, nullable=False)
    name = Column(String)
    server_id = Column(Integer, ForeignKey('servers.id'))
    role_created_at = Column(DateTime, nullable=False)
    role_deleted_at = Column(DateTime, nullable=True)

    server = relationship("Server", back_populates="roles")
    flags = relationship("RoleFlag", back_populates="role")
    members = relationship("Member", secondary=member2Role_table, back_populates="roles")


class User(Base):
    __tablename__ = "users"

    uid = Column(BigInteger, unique=True, nullable=False)
    name = Column(String)
    discriminator = Column(String)

    members = relationship("Member", back_populates="user")


class Member(Base):
    __tablename__ = "members"

    user_id = Column(Integer, ForeignKey('users.id'))
    server_id = Column(Integer, ForeignKey('servers.id'))
    joined_at = Column(DateTime, nullable=False, server_default=func.now())
    left_at = Column(DateTime, nullable=True)

    user = relationship("User", back_populates="members")
    server = relationship("Server", back_populates="members")
    flags = relationship("MemberFlag", back_populates="user")
    roles = relationship("Role", secondary=member2Role_table, back_populates="members")

    # This is set up this way so wen we ask for Member.name we actually get User.name
    # and should work with query as well.
    @hybrid_property
    def name(self):
        return self.user.name

    # this setter makes it so we can not only read but also set with Member.name
    @name.setter
    def name(self, value):
        self.user.name = value

    # thi is needed for relationship hybrid properties, so its knows its needs join.
    @name.expression
    def name(cls):
        return User.name

    @hybrid_property
    def uid(self):
        return self.user.uid

    @uid.setter
    def uid(self, value):
        self.user.uid = value

    @uid.expression
    def uid(cls):
        return User.uid

    @hybrid_property
    def discriminator(self):
        return self.user.discriminator

    @discriminator.setter
    def discriminator(self, value):
        self.user.discriminator = value

    @discriminator.expression
    def discriminator(cls):
        return User.discriminator


class FlagBase(object):
    name = Column(String)
    value = Column(String, nullable=True, server_default=text('NULL'))


class ServerFlag(Base, FlagBase):
    __tablename__ = "server_flags"

    server_id = Column(Integer, ForeignKey('servers.id'))

    server = relationship("Server", back_populates="flags")


class RoleFlag(Base, FlagBase):
    __tablename__ = "role_flags"

    role_id = Column(Integer, ForeignKey('roles.id'))

    role = relationship("Role", back_populates="flags")


class MemberFlag(Base, FlagBase):
    __tablename__ = "member_flags"

    member_id = Column(Integer, ForeignKey('members.id'))

    user = relationship("Member", back_populates="flags")
