import random

import discord
from discord.ext import commands

from groovebot.core.cogs import MusicCog, AbbreviationCog, HelpCog, MiscCog, ModerationCog, AlbumCog
from groovebot.core.config import config
from groovebot.core.lib.tortoise import tortoise_init
from groovebot.core.utils import read_file

intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(help_command=None, command_prefix=None, intents=intents)


@bot.event
async def on_ready():
    print("Groovebot is now live.")


async def on_member_event(member, file):
    channel = member.guild.get_channel(int(config['GROOVE']['general_channel_id']))
    response = random.choice(await read_file(file, as_array=True)).format(member.mention)
    await channel.send(response)


@bot.event
async def on_member_join(member):
    await on_member_event(member, 'greetings.txt')
    await member.send(await read_file('welcome.txt'))


@bot.event
async def on_member_remove(member):
    await on_member_event(member, 'farewells.txt')


if __name__ == '__main__':
    bot.add_cog(AlbumCog(bot))
    bot.add_cog(MusicCog(bot))
    bot.add_cog(HelpCog(bot))
    bot.add_cog(MiscCog(bot))
    bot.add_cog(AbbreviationCog(bot))
    bot.add_cog(ModerationCog(bot))
    bot.loop.create_task(tortoise_init())
    bot.command_prefix = config['GROOVE']['prefix']
    bot.run(config['GROOVE']['token'], bot=True)
