async def failure_message(ctx, message):
    await ctx.send(':x: **' + message + '**')


async def success_message(ctx, message, model=None, embed=None):
    message = ':white_check_mark: __** ' + message + '**__'
    if model:
        message += '\n' + str(model)
    await ctx.send(message, embed=embed)


def read_file(path, as_array=False):
    with open('resources/' + path, mode="r") as f:
        return f.readlines() if as_array else f.read()
