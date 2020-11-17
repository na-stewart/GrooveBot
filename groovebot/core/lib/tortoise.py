from tortoise import Tortoise

from groovebot.core.config import config_parser


async def tortoise_init():
    schema = config_parser['TORTOISE']['schema']
    models_str = config_parser['TORTOISE']['models'].replace(']', '').replace('[', '').replace(' ', '')\
        .replace('\'', '').replace('\"', '')
    await Tortoise.init(
        db_url='sqlite://' + schema,
        modules={'models': models_str.split(",")}
    )
    if config_parser['TORTOISE']['generate'] == 'true':
        await Tortoise.generate_schemas()