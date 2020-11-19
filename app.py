import asyncio
import random

from discord.ext import commands

from groovebot.core.cogs import MusicCog, UtilsCog, AbbreviationCog, NeuropolCog
from groovebot.core.config import config_parser
from groovebot.core.lib.tortoise import tortoise_init
from groovebot.core.utils import read_file

bot = commands.Bot(help_command=None, command_prefix=None)


@bot.event
async def on_ready():
    print("Hi! I'm alive and ready.")


@bot.command()
async def fact(ctx):
    await ctx.send(random.choice(read_file('facts.txt', True)))



async def disconnect_from_voice_when_alone():
    while True:
        for client in bot.voice_clients:
            if len(client.channel.members) == 1:
                await client.disconnect()
        await asyncio.sleep(3600)


if __name__ == '__main__':
    bot.add_cog(MusicCog(bot))
    bot.add_cog(NeuropolCog(bot))
    bot.add_cog(UtilsCog(bot))
    bot.add_cog(AbbreviationCog(bot))
    bot.loop.create_task(tortoise_init())
    bot.loop.create_task(disconnect_from_voice_when_alone())
    bot.command_prefix = config_parser['GROOVE']['prefix']
    bot.run(config_parser['GROOVE']['token'], bot=True)
