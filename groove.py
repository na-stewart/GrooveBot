import random

import discord
from discord.ext import commands
from discord.ext.commands import MissingRequiredArgument
from tortoise.exceptions import ValidationError, IntegrityError

from groovebot.core.cogs import MusicCog, AlbumCog, HelpCog, MiscCog, AbbreviationCog, ModerationCog, RetrievalCog, \
    NeuropolCog
from groovebot.core.utils import read_file, failure_message, config
from groovebot.lib.tortoise import tortoise_init

intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(help_command=None, command_prefix=None, intents=intents)


@bot.event
async def on_ready():
    await tortoise_init()
    print('Groovebot initialized.')


async def on_member_event(member, file):
    channel = member.guild.get_channel(int(config['GROOVE']['general_channel_id']))
    response = random.choice(await read_file(file, as_array=True)).format(member.mention, member.name,
                                                                          member.discriminator)
    await channel.send(response)


@bot.event
async def on_member_join(member):
    await on_member_event(member, 'greetings.txt')
    await member.send(await read_file('welcome.txt'))


@bot.event
async def on_member_remove(member):
    await on_member_event(member, 'farewells.txt')


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, MissingRequiredArgument):
        await failure_message(ctx, 'You are missing one or more arguments in your command!')
    if error.original:
        if isinstance(error.original, ValidationError):
            await failure_message(ctx, 'One or more of your arguments in your command is too long!')
        if isinstance(error.original, IntegrityError):
            if error.original.args[0].args[0] == 1062:
                await failure_message(ctx, 'This acronym is already being used in the database!')

if __name__ == '__main__':
    bot.add_cog(AlbumCog(bot))
    bot.add_cog(MusicCog(bot))
    bot.add_cog(HelpCog(bot))
    bot.add_cog(MiscCog(bot))
    bot.add_cog(AbbreviationCog(bot))
    bot.add_cog(ModerationCog(bot))
    bot.add_cog(RetrievalCog(bot))
    bot.add_cog(NeuropolCog(bot))
    bot.command_prefix = config['GROOVE']['prefix']
    bot.run(config['GROOVE']['token'], bot=True)
