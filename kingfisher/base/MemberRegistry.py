from __future__ import annotations

import logging
from datetime import datetime

from discord import (
    Member as GuildMember,
    User as GuildUser,
)
from discord.ext.commands import Cog
from sqlalchemy.orm import Session, Query

from .Kingfisher import KingfisherBot
from .ServerRegistry import ServerRegistry
from .exception import (
    MemberNotFoundException,
    GuildRoleNotFoundException,
    UserNotFoundException,
)
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
        self.logger.info("Updating Users...")
        for member in self.bot.get_all_members():
            if not member.bot:
                self.logger.debug(f"{member.name}#{member.discriminator}")
                self._check_and_add_new_member(member)
                await self._check_and_update_role_relationship(member)

    @Cog.listener()
    async def on_member_join(self, member: GuildMember):
        if not member.bot:
            self.logger.info(f"Member {member.name} joined guild {member.guild.name}.")
            self._check_and_add_new_member(member)
            await self._reapply_roles_to_member(member)

    @Cog.listener()
    async def on_member_remove(self, member: GuildMember):
        if not member.bot:
            with self.bot.get_session() as session:
                our_member = self.get_member_from_guild_member(session, member)
                our_member.left_at = datetime.now()

    @Cog.listener()
    async def on_member_update(self, before: GuildMember, after: GuildMember):
        if not before.bot:
            # with member we only care about roles for now so let see if that changed
            # https://stackoverflow.com/a/3462160/1297666
            diff_roles = set(before.roles).symmetric_difference(set(after.roles))
            if diff_roles:
                self.logger.info(f"Updating roles for {after.name}#{after.discriminator}")
                # there'sa a different
                with self.bot.get_session() as session:
                    member = self.get_member_from_guild_member(session, after)
                    # lets figure out if it's an add or remove
                    for drole in diff_roles:
                        server_role = ServerRegistry.get_role_from_guild_role(session, drole)
                        if drole in after.roles:
                            # an add
                            self.logger.debug(f"Adding role {drole.name} to {after.name}#{after.discriminator}")
                            member.roles.append(server_role)
                        else:
                            # a remove
                            self.logger.debug(f"Removing role {drole.name} from {after.name}#{after.discriminator}")
                            member.roles.remove(server_role)

    @Cog.listener()
    async def on_user_update(self, before: GuildUser, after: GuildUser):
        if not before.bot:
            with self.bot.get_session() as session:
                user = self.get_user_from_guild_user(session, after)
                if before.name != after.name:
                    self.logger.info(
                        f"User {before.name}#{before.discriminator} renamed to {after.name}#{after.discriminator}"
                    )
                    user.name = after.name
                if before.discriminator != after.discriminator:
                    self.logger.info(
                        f"User {before.name}#{before.discriminator} changed to {after.name}#{after.discriminator}"
                    )
                    user.discriminator = after.discriminator

    def _check_and_add_new_member(self, member: GuildMember):
        with self.bot.get_session() as session:
            if not member.bot:
                if not self._check_member_registered(session, member):
                    self.logger.info(f"New Member found on ready: {member.name} on {member.guild.name}")
                    self._add_new_member(session, member)

    @classmethod
    def _check_member_registered(cls, session: Session, member: GuildMember) -> bool:
        # here we reuse the ORM query and ask if there is a member like that.
        return bool(cls._get_member_from_guild_member_query(session, member).one_or_none())

    @classmethod
    def get_member_from_guild_member(cls, session: Session, guild_member:  GuildMember) -> Member:
        # here we reuse the ORM query and ask if there is a member like that.
        member = cls._get_member_from_guild_member_query(session, guild_member).one_or_none()
        # we could use just Query.one(), but then we could not use our own Exception and handle it
        # with ORM exceptions, i like it this way better.
        if not member:
            raise MemberNotFoundException(guild_member)
        return member

    @staticmethod
    def _get_member_from_guild_member_query(session: Session, member:  GuildMember) -> Query:
        # reusable ORM query, its not executed yet.
        return session.query(Member)\
            .join(Server)\
            .join(User)\
            .filter(Member.uid == member.id)\
            .filter(Member.sid == member.guild.id)

    @staticmethod
    def _get_user_from_guild_user_query(session: Session, user:  GuildUser) -> Query:
        return session.query(User).filter(User.uid == user.id)

    @classmethod
    def get_user_from_guild_user(cls, session: Session, user:  GuildUser) -> User:
        user = cls._get_user_from_guild_user_query(session, user).one_or_none()
        if not user:
            raise UserNotFoundException(user)
        return user

    def _add_new_member(self, session: Session, member: GuildMember):
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

        new_member = Member(user=user, server=server)
        session.add(new_member)

        # lets add his roles as well.
        self._connect_member_with_roles(session, new_member, member)

    async def _check_and_update_role_relationship(self, guild_member: GuildMember):
        with self.bot.get_session() as session:
            member = self.get_member_from_guild_member(session, guild_member)
            member.roles.clear()
            await self._connect_member_with_roles(session, member, guild_member)

    @staticmethod
    async def _connect_member_with_roles(session: Session, member: Member, guild_member: GuildMember):
        for guild_role in guild_member.roles:
            if guild_role.name != "@everyone":
                role = ServerRegistry.get_role_from_guild_role(session, guild_role)
                member.roles.append(role)

    async def _reapply_roles_to_member(self, guild_member: GuildMember):
        with self.bot.get_session() as session:
            member = self.get_member_from_guild_member(session, guild_member)
            roles_to_add = []
            for role in member.roles:
                if role.name != "@everyone":
                    guild_role = guild_member.guild.get_role(role.rid)
                    if not guild_role:
                        raise GuildRoleNotFoundException(role.rid, guild_member.guild)
                    roles_to_add.append(guild_role)

            if roles_to_add:
                self.logger.info(
                    f"Member {guild_member.name} actually rejoined {guild_member.guild.name}. Re-adding roles."
                )
                # the * is: https://docs.python.org/2.7/tutorial/controlflow.html#unpacking-argument-lists
                await guild_member.add_roles(*roles_to_add, reason=f"{member.name} rejoined. re-adding previous Roles.")
