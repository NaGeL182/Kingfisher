from discord import Guild, Member


class KingfisherException(Exception):
    """Base Kingfisher Exception class"""
    pass


class ServerNotFoundException(KingfisherException):
    def __init__(self, guild: Guild):
        message = f"Server ({guild.name}, {guild.id}) was not found in Database"
        super().__init__(message)


class MemberNotFoundException(KingfisherException):
    def __init__(self, member: Member):
        message = f"Member ({member.name}, {member.id}) was not found in Database"
        super().__init__(message)
