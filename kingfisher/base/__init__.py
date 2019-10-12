from .Logging import Logging
from .MemberRegistry import MemberRegistry
from .ServerRegistry import ServerRegistry


def setup(bot):
    bot.add_cog(Logging(bot))
    bot.add_cog(ServerRegistry(bot))
    bot.add_cog(MemberRegistry(bot))


def teardown(bot):
    bot.remove_cog('Logging')
    bot.remove_cog('ServerRegistry')
    bot.remove_cog('MemberRegistry')
