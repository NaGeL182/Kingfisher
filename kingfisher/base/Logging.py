from discord.ext.commands import Cog
import logging
import discord
import platform


class Logging(Cog, name="Logging"):

    logger = None

    def __init__(self, bot):
        self.bot = bot
        self.logger = logging.getLogger(__name__)

    @Cog.listener()
    async def on_connect(self):
        self.logger.info("Successful Connection")

    @Cog.listener()
    async def on_ready(self):
        self.logger.info('Logged in as ' + self.bot.user.name + ' (ID:' + str(self.bot.user.id) + ') | Connected to '
                         + str(len(self.bot.guilds)) + ' servers | Connected to '
                         + str(len(set(self.bot.get_all_members()))) + ' users')
        self.logger.info(f"Current Discord.py Version: {discord.__version__}" +
                         f"| Current Python Version: {platform.python_version()}")
        self.logger.info("Ready")

    @Cog.listener()
    async def on_member_join(self, member):
        self.logger.debug(f"New member Joined: {member.guild.name}: {member.name}" +
                          f"\n Account creation on {member.created_at}"
                          )

    @Cog.listener()
    async def on_member_remove(self, member):
        self.logger.debug(f"{member.name} left {member.guild.name}")

    @Cog.listener()
    async def on_command_error(self, context, exception):
        self.logger.exception(exception)
