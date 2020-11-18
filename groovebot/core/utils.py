import aiofiles as aiofiles


async def send_failure_message(ctx, message):
    await ctx.send(':x: **' + message + '**')


async def send_success_message(ctx, message, model=None, embed=None):
    success_message = ':white_check_mark: __** ' + message + '**__'
    if model:
        success_message += '\n' + str(model)
    await ctx.send(success_message, embed=embed)


async def read_file(path, as_array=False):
    async with aiofiles.open('resources/' + path, mode="r") as f:
        return await f.readlines() if as_array else await f.read()
