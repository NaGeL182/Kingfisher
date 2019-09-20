from discord.ext.commands import Bot


class KingfisherBot(Bot):
    def __init__(self, command_prefix, db, config, **options):
        super().__init__(command_prefix, **options)
        self.db = db
        self.config = config
