import aiofiles as aiofiles


async def send_failure_message(ctx, message):
    await ctx.send(':x: **' + message + '**')


async def send_success_message(ctx, message):
    await ctx.send(':white_check_mark: **' + message + '**')


async def read_file(path, as_array=False):
    async with aiofiles.open('resources/' + path, mode="r") as f:
        return await f.readlines() if as_array else await f.read()
