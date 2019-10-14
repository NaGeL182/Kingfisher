from __future__ import annotations
from discord import Guild, Member, Role, User


class KingfisherException(Exception):
    """Base Kingfisher Exception class"""
    pass


class ServerNotFoundException(KingfisherException):
    def __init__(self, guild: Guild):
        message = f"Server ({guild.name}, {guild.id}) was not found in Database"
        super().__init__(message)


class RoleNotFoundException(KingfisherException):
    def __init__(self, role: Role):
        message = f"Role ({role.name}, {role.id}, server: {role.guild.name}) was not found in Database"
        super().__init__(message)


class MemberNotFoundException(KingfisherException):
    def __init__(self, member: Member):
        message = f"Member ({member.name}, {member.id}) was not found in Database"
        super().__init__(message)


class UserNotFoundException(KingfisherException):
    def __init__(self, user: User):
        message = f"User ({user.name}, {user.id}) was not found in Database"
        super().__init__(message)


class GuildRoleNotFoundException(KingfisherException):
    def __init__(self, rid: int, guild: Guild):
        message = f"Guild Role Id: {rid} was not found on {guild.name}!"
        super().__init__(message)
