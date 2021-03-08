from tortoise import Tortoise

from groovebot.core.config import config


async def tortoise_init():
    schema = config['TORTOISE']['schema']
    models_str = config['TORTOISE']['models'].replace(']', '').replace('[', '').replace(' ', '')\
        .replace('\'', '').replace('\"', '')
    await Tortoise.init(
        db_url='sqlite://' + schema,
        modules={'models': models_str.split(",")}
    )
    if config['TORTOISE']['generate'] == 'true':
        await Tortoise.generate_schemas()