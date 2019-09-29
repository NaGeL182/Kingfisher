from sqlalchemy.ext.declarative import declarative_base, declared_attr
from sqlalchemy import Column, Integer, DateTime, func, text, String, Boolean, ForeignKey
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

    sid = Column(Integer, unique=True)
    name = Column(String)
    joined_at = Column(DateTime, nullable=False, server_default=func.now())
    left_at = Column(DateTime, nullable=True, server_default=text('NULL'))

    flags = relationship("ServerFlag", back_populates="server")
    roles = relationship("Role", back_populates="server")
    members = relationship("Member", back_populates="server")


class Role(Base):
    __tablename__ = "roles"

    rid = Column(Integer, unique=True)
    name = Column(String)
    server_id = Column(Integer, ForeignKey('servers.id'))
    role_created_at = Column(DateTime, nullable=False)
    role_deleted_at = Column(DateTime, nullable=True)

    server = relationship("Server", back_populates="roles")
    flags = relationship("RoleFlag", back_populates="role")


class User(Base):
    __tablename__ = "users"

    uid = Column(Integer, unique=True)
    name = Column(String)
    discriminator = Column(String)

    flags = relationship("UserFlag", back_populates="user")
    members = relationship("Member", back_populates="user")


class Member(Base):
    __tablename__ = "members"

    user_id = Column(Integer, ForeignKey('users.id'))
    server_id = Column(Integer, ForeignKey('servers.id'))
    joined_at = Column(DateTime, nullable=False)
    left_at = Column(DateTime, nullable=True)

    user = relationship("User", back_populates="members")
    server = relationship("Server", back_populates="members")
    flags = relationship("MemberFlag", back_populates="user")


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


class UserFlag(Base, FlagBase):
    __tablename__ = "user_flags"

    user_id = Column(Integer, ForeignKey('users.id'))

    user = relationship("User", back_populates="flags")


class MemberFlag(Base, FlagBase):
    __tablename__ = "member_flags"

    member_id = Column(Integer, ForeignKey('members.id'))

    user = relationship("Member", back_populates="flags")
