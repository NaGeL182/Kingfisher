from .Logging import Logging
from.ServerRegistry import ServerRegistry

def setup(bot):
    bot.add_cog(Logging(bot))
    bot.add_cog(ServerRegistry(bot))


def teardown(bot):
    bot.remove_cog('Logging')
    bot.remove_cog('ServerRegistry')
