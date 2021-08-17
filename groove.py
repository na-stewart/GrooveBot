import random

import discord
from discord.ext import commands
from discord.ext.commands import MissingRequiredArgument, ExpectedClosingQuoteError, CommandNotFound
from tortoise.exceptions import ValidationError, IntegrityError

from groovebot.core.cogs import MusicCog, AlbumCog, MiscCog, AbbreviationCog, ModerationCog, RetrievalCog, \
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


async def handle_invalid_command(ctx, error):
    if isinstance(error, MissingRequiredArgument):
        await failure_message(ctx, 'You are missing one or more arguments in your command!', error)
    if isinstance(error, ExpectedClosingQuoteError):
        await failure_message(ctx, 'A closing quotation is missing in one or more of your command arguments.', error)


async def handle_command_error(ctx, error):
    if isinstance(error, ValidationError):
        await failure_message(ctx, 'One or more of your arguments in your command is too long!', error)
    elif isinstance(error, IntegrityError):
        if error.args[0].args[0] == 1062:
            await failure_message(ctx, 'This acronym is already being used in the database!', error)


@bot.event
async def on_command_error(ctx, error):
    if hasattr(error, 'original'):
        await handle_command_error(ctx, error.original)
    else:
        await handle_invalid_command(ctx, error)
    await failure_message(ctx, 'An unexpected error has occurred! Please see console.', error)


if __name__ == '__main__':
    bot.add_cog(AlbumCog(bot))
    bot.add_cog(MusicCog(bot))
    bot.add_cog(MiscCog(bot))
    bot.add_cog(AbbreviationCog(bot))
    bot.add_cog(ModerationCog(bot))
    bot.add_cog(RetrievalCog(bot))
    bot.add_cog(NeuropolCog(bot))
    bot.command_prefix = config['GROOVE']['prefix']
    bot.run(config['GROOVE']['token'], bot=True)
