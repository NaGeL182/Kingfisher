from __future__ import annotations

import logging
from datetime import datetime

from discord import Guild, Role as GuildRole
from discord.ext.commands import Cog
from sqlalchemy.orm import Session, Query

from .Kingfisher import KingfisherBot
from .exception import ServerNotFoundException, RoleNotFoundException
from .models import Server, Role


class ServerRegistry(Cog, name="ServerRegistry"):

    logger = None

    def __init__(self, bot: KingfisherBot):
        self.bot = bot
        self.logger = logging.getLogger(__name__)

    @Cog.listener()
    async def on_ready(self):
        # get all the server the bot connected, and see if they are already registered
        # if not register them
        with self.bot.get_session() as session:
            for server in self.bot.guilds:
                if not self._check_server_registered(session, server):
                    # get the time when the bot joined
                    self.logger.info(f"New Server found on ready: {server.name}")
                    self._add_new_server(session, server)
                else:
                    # server is there so update
                    self._update_server(session, server)

    @Cog.listener()
    async def on_guild_join(self, guild: Guild):
        with self.bot.get_session() as session:
            if not self._check_server_registered(session, guild):
                # get the time when the bot joined
                self.logger.info(f"New Server found on guild join: {guild.name}")
                self._add_new_server(session, guild)
            else:
                # we were already on the server so just update the joined at
                self.logger.info(f"Rejoined Guild: {guild.name}")
                server = self.get_server_from_guild(session, guild)
                server. joined_at = guild.me.joined_at

    @Cog.listener()
    async def on_guild_update(self, before: Guild, after: Guild):
        with self.bot.get_session() as session:
            server = self.get_server_from_guild(session, after)

            if before.name != after.name:
                self.logger.info(f"{before.name} renamed to {after.name}")
                server.name = after.name

    @Cog.listener()
    async def on_guild_remove(self, guild: Guild):
        with self.bot.get_session() as session:
            self.logger.info(f"Left server `{guild.name}` at {datetime.now()}")
            server = self.get_server_from_guild(session, guild)

            server.left_at = datetime.now()

    @staticmethod
    def _get_server_from_guild_query(session: Session, guild: Guild) -> Query:
        return session.query(Server).filter(Server.sid == guild.id)

    @classmethod
    def _check_server_registered(cls, session: Session, guild: Guild) -> bool:
        return bool(cls._get_server_from_guild_query(session, guild).one_or_none())

    @classmethod
    def get_server_from_guild(cls, session: Session, guild: Guild) -> Server:
        server = cls._get_server_from_guild_query(session, guild).one_or_none()
        if not server:
            raise ServerNotFoundException(guild)
        return server

    def _add_new_server(self, session: Session, server: Guild):
        me = server.me
        joined_at = me.joined_at
        if not joined_at:
            joined_at = datetime.now()
        new_server = Server(sid=server.id, name=server.name, joined_at=joined_at)
        session.add(new_server)

        # since new server the roles aren't in there, so add them as well.
        for role in server.roles:
            if role.name != "@everyone":
                self._add_new_role(role=role, server=new_server)
        pass

    @Cog.listener()
    async def on_guild_role_create(self, role: GuildRole):
        with self.bot.get_session() as session:
            # check if the role already exists, if not create it.
            if not self._check_role_registered(session, role):
                server = self.get_server_from_guild(session, role.guild)

                self._add_new_role(role, server)

    @Cog.listener()
    async def on_guild_role_update(self, before: GuildRole, after: GuildRole):
        if before.name != "@everyone":
            with self.bot.get_session() as session:
                role = self.get_role_from_guild_role(session, after)
                if before.name != after.name:
                    self.logger.info(f"Role {before.name} renamed to {after.name}")
                    role.name = after.name

    @Cog.listener()
    async def on_guild_role_delete(self, role: GuildRole):
        with self.bot.get_session() as session:
            # check if the role exists, if yes yet the delete date.
            server_role = self.get_role_from_guild_role(session, role)
            if server_role:
                self.logger.info(f"Role {role.name} ({role.id}) has been deleted.")
                server_role.role_deleted_at = datetime.now()
                # clear the users associated with this so we dont add the non existent role again
                server_role.members.clear()

    @classmethod
    def _check_role_registered(cls, session: Session, role: GuildRole) -> bool:
        return bool(cls._get_role_from_guild_role_query(session, role).one_or_none())

    @classmethod
    def get_role_from_guild_role(cls, session: Session, role: GuildRole) -> Role:
        role = cls._get_role_from_guild_role_query(session, role).one_or_none()
        if not role:
            raise RoleNotFoundException(role)
        return role

    @staticmethod
    def _get_role_from_guild_role_query(session: Session, role: GuildRole) -> Query:
        return session.query(Role).filter(Role.rid == role.id)

    def _add_new_role(self, role: GuildRole, server: Server):
        Role(rid=role.id, name=role.name, server=server, role_created_at=role.created_at)
        self.logger.info(f"Role {role.name} ({role.id}) has been added.")

    def _update_server(self, session: Session, guild: Guild):
        server = self.get_server_from_guild(session, guild)
        self.logger.info(f"Updating Guild {guild.name}.")
        if server.name != guild.name:
            server.name = guild.name
        for grole in guild.roles:
            if grole.name != "@everyone":
                if self._check_role_registered(session, grole):
                    role = self.get_role_from_guild_role(session, grole)
                    if grole.name != role.name:
                        role.name = grole
                else:
                    # new role
                    self._add_new_role(grole, server)
