from tortoise import Tortoise

from groovebot.core.utils import config


async def tortoise_init():
    models = config["TORTOISE"]["models"].replace(" ", "").split(",")
    await Tortoise.init(
        db_url=config["TORTOISE"]["database_url"], modules={"models": models}
    )
    if config["TORTOISE"].getboolean("generate"):
        await Tortoise.generate_schemas()
