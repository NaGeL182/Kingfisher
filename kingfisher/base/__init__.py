from .Logging import Logging


def setup(bot):
    bot.add_cog(Logging(bot))


def teardown(bot):
    bot.remove_cog('Logging')
