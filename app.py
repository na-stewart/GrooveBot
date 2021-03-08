import asyncio
import random

import discord
from discord.ext import commands

from groovebot.core.cogs import MusicCog, AbbreviationCog, HelpCog, ExtrasCog, ModerationCog, AlbumCog
from groovebot.core.config import config
from groovebot.core.lib.tortoise import tortoise_init
from groovebot.core.utils import read_file

intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(help_command=None, command_prefix=None, intents=intents)


@bot.event
async def on_ready():
    print("Hi! I'm alive and ready.")


@bot.event
async def on_member_join(member):
    channel = discord.utils.get(member.guild.text_channels, name=config['GROOVE']['general'])
    response = random.choice(read_file('greetings.txt', as_array=True)).format(member.mention)
    await channel.send(response)


@bot.event
async def on_member_remove(member):
    channel = discord.utils.get(member.guild.text_channels, name=config['GROOVE']['general'])
    response = random.choice(read_file('farewells.txt', as_array=True)).format(member.mention)
    await channel.send(response)


if __name__ == '__main__':
    bot.add_cog(AlbumCog(bot))
    bot.add_cog(MusicCog(bot))
    bot.add_cog(HelpCog(bot))
    bot.add_cog(ExtrasCog(bot))
    bot.add_cog(AbbreviationCog(bot))
    bot.add_cog(ModerationCog(bot))
    bot.loop.create_task(tortoise_init())
    bot.command_prefix = config['GROOVE']['prefix']
    bot.run(config['GROOVE']['token'], bot=True)
