import random

from discord.ext import commands

from groovebot.core.cogs import MusicCog, UtilsCog
from groovebot.core.config import config_parser
from groovebot.core.lib.tortoise import tortoise_init
from groovebot.core.utils import read_file

bot = commands.Bot(help_command=None, command_prefix=None)


@bot.event
async def on_ready():
    print("Hi! I'm alive and ready.")


@bot.command()
async def fact(ctx):
    await ctx.send(random.choice(await read_file('facts.txt', True)))


@bot.command()
async def neuropol(ctx, *args):
    neuropol_message = ''
    for char in "{}".format(" ".join(args)).upper():
        if char != ' ':
            neuropol_message += ':' + char + '_: '
    await ctx.send(neuropol_message)
    await ctx.message.delete()


if __name__ == '__main__':
    bot.add_cog(MusicCog(bot))
    bot.add_cog(UtilsCog(bot))
    bot.loop.create_task(tortoise_init())
    bot.command_prefix = config_parser['GROOVE']['prefix']

    bot.run(config_parser['GROOVE']['token'], bot=True)
