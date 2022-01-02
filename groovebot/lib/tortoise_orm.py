from tortoise import Tortoise

from groovebot.core.utils import config


async def tortoise_init():
    await Tortoise.init(
        db_url=config["TORTOISE"]["database_url"], modules={"models": ["groovebot.core.models"]}
    )
    if config["TORTOISE"].getboolean("generate"):
        await Tortoise.generate_schemas()
