from config import config
from discord.ext.commands import Bot
import logging
from logging.handlers import TimedRotatingFileHandler
from logging import StreamHandler
from sys import stdout

major_version = 0
minor_version = 3
patch_version = 0

version = f"{major_version}.{minor_version}.{patch_version}"


def create_bot():
    return Bot(
        description=f"Thinkerbot version {version}",
        command_prefix=config.command_prefix,
        case_insensitive=True,
        owner_id=config.owner
    )


def setup_logging():
    # everything about logging
    # https://docs.python.org/3.7/library/logging.html
    formatter = logging.Formatter("[%(asctime)s] %(levelname)s [%(name)s.%(funcName)s:%(lineno)d] %(message)s")

    file_handler = TimedRotatingFileHandler(
        filename=config.log['file'],
        when=config.log['when'],
        interval=config.log['interval'],
        backupCount=config.log['backupCount'],
        utc=config.log['utc']
    )
    file_handler.setFormatter(formatter)

    console_handler = StreamHandler(stdout)
    console_handler.setFormatter(formatter)

    root_logger = logging.getLogger()
    # if we set it here we set all the logger even imported modules log level
    # but right now i dont know better ...
    root_logger.setLevel(config.log['level'])
    root_logger.addHandler(file_handler)
    root_logger.addHandler(console_handler)


if __name__ == '__main__':
    setup_logging()
    bot = create_bot()
    bot.load_extension('base')
    bot.run(config.token)
