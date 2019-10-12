from __future__ import annotations

import logging
from datetime import datetime

from discord import Member as GuildMember
from discord.ext.commands import Cog
from sqlalchemy.orm import Session

from .Kingfisher import KingfisherBot
from .ServerRegistry import ServerRegistry
from .exception import ServerNotFoundException, MemberNotFoundException
from .models import User, Member, Server


class MemberRegistry(Cog, name="MemberRegistry"):
    logger = None

    def __init__(self, bot: KingfisherBot):
        self.bot = bot
        self.logger = logging.getLogger(__name__)

    @Cog.listener()
    async def on_ready(self):
        # get all the server the bot connected, and see if they are already registered
        # if not register them
        for member in self.bot.get_all_members():
            self._check_and_add_new_member(member)
            # TODO : update roles in database

    @Cog.listener()
    async def on_member_join(self, member: GuildMember):
        self._check_and_add_new_member(member)
        # TODO : re add roles

    @Cog.listener()
    async def on_member_remove(self, member: GuildMember):
        with self.bot.get_session() as session:
            our_member = self._get_member_from_guild_member(session, member)
            if not our_member:
                raise MemberNotFoundException(member)
            our_member.left_at = datetime.now()

    # TODO: on_member_update, on_user_update

    def _check_and_add_new_member(self, member: GuildMember):
        with self.bot.get_session() as session:
            if not member.bot:
                if not self._check_member_registered(session, member):
                    self.logger.info(f"New Member found on ready: {member.name} on {member.guild.name}")
                    self._add_new_member(session, member)

    @classmethod
    def _check_member_registered(cls, session: Session, member: GuildMember) -> bool:
        return bool(cls._get_member_from_guild_member(session, member))

    @staticmethod
    def _get_member_from_guild_member(session: Session, member:  GuildMember):
        return session.query(Member)\
            .join(Server)\
            .join(User)\
            .filter(Member.uid == member.id)\
            .filter(Member.sid == member.guild.id)\
            .one_or_none()

    @staticmethod
    def _add_new_member(session: Session, member: GuildMember):
        # first check if the Member is a new user or not.
        user = session.query(User)\
            .filter(User.uid == member.id)\
            .one_or_none()
        if not user:
            user = User()
            user.uid = member.id
            user.name = member.name
            user.discriminator = member.discriminator
            session.add(user)

        # lets get the server this member belongs to.
        server = ServerRegistry.get_server_from_guild(session, member.guild)
        if not server:
            raise ServerNotFoundException(member.guild)

        new_member = Member(user=user, server=server)
        session.add(new_member)

        # lets add his roles as well.
        # TODO: add roles


