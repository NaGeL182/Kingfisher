from discord.ext.commands import Cog
from discord import Guild
import logging
from .models import Server, Role
from datetime import datetime
from .Kingfisher import KingfisherBot
from sqlalchemy.orm import Session
from pprint import pprint


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
                server = self._get_server_from_guild(session, guild)
                server. joined_at = guild.me.joined_at

    # TODO: on guild update

    @Cog.listener()
    async def on_guild_remove(self, guild: Guild):
        with self.bot.get_session() as session:
            self.logger.info(f"left  server `{guild.name}` at {datetime.now()}")
            server = self._get_server_from_guild(session, guild)
            server.left_at = datetime.now()

    @classmethod
    def _check_server_registered(cls, session: Session, guild: Guild) -> bool:
        return bool(cls._get_server_from_guild(session, guild))

    @staticmethod
    def _get_server_from_guild(session: Session, guild: Guild):
        return session.query(Server).filter(Server.sid == guild.id).one_or_none()

    @staticmethod
    def _add_new_server(session: Session, server: Guild):
        me = server.me
        joined_at = me.joined_at
        if not joined_at:
            joined_at = datetime.now()
        new_server = Server(sid=server.id, name=server.name, joined_at=joined_at)
        session.add(new_server)

        # since new server the roles aren't in there, so add them as well.
        for role in server.roles:
            Role(rid=role.id, name=role.name, server=new_server, role_created_at=role.created_at)
