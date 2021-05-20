from tortoise import Tortoise

from groovebot.core.utils import config


async def tortoise_init():
    username = config['TORTOISE']['username']
    password = config['TORTOISE']['password']
    endpoint = config['TORTOISE']['endpoint']
    schema = config['TORTOISE']['schema']
    engine = config['TORTOISE']['engine']
    models = config['TORTOISE']['models'].replace(' ', '').split(',')
    url = engine + '://{0}:{1}@{2}/{3}'.format(username, password, endpoint, schema)
    await Tortoise.init(db_url=url, modules={"models": models})
    if config['TORTOISE']['generate'] == 'true':
        await Tortoise.generate_schemas()
