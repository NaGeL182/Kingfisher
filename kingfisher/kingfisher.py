from config import config
from base.Kingfisher import KingfisherBot

major_version = 0
minor_version = 3
patch_version = 0

version = f"{major_version}.{minor_version}.{patch_version}"


def create_bot():
    db = {}
    return KingfisherBot(
        description=f"Thinkerbot version {version}",
        command_prefix=config.command_prefix,
        case_insensitive=True,
        owner_id=config.owner,
        db=db,
        config=config,
    )


def main():
    bot = create_bot()
    bot.load_extension('base')
    bot.run(config.token)


if __name__ == '__main__':
    main()
