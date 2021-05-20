import aiofiles
from configparser import ConfigParser

config = ConfigParser()
config.read('./groove.ini')


async def failure_message(ctx, message):
    await ctx.send(':x: **' + message + '**')


async def success_message(ctx, message, model=None, embed=None):
    message = ':white_check_mark: ** ' + message + '**'
    if model:
        message += '\n' + str(model)
    await ctx.send(message, embed=embed)


async def read_file(path, as_array=False):
    async with aiofiles.open('resources/' + path) as f:
        return [line.strip() async for line in f] if as_array else await f.read()
