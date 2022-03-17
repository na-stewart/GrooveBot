import random

import discord
from discord.ext import commands
from discord.ext.commands import (
    CommandNotFound,
)
from tortoise import Tortoise
from tortoise.exceptions import ValidationError, IntegrityError

from groovebot.core.cogs import setup_cogs
from groovebot.core.models import Album, Music, Abbreviation, Strike
from groovebot.core.utils import failure_message, config, success_message

intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(
    help_command=None, command_prefix=config["GROOVE"]["prefix"], intents=intents
)


@bot.event
async def on_ready():
    await Tortoise.init(
        db_url=config["TORTOISE"]["database_url"],
        modules={"models": ["groovebot.core.models"]},
    )
    if config["TORTOISE"].getboolean("generate"):
        await Tortoise.generate_schemas()
    print("Groovebot initialized.")


@bot.event
async def on_member_join(member):
    with open("resources/welcome.txt", "r") as wf, open(
        "resources/greetings.txt", "r"
    ) as gf:
        await member.guild.get_channel(
            int(config["GROOVE"]["general_channel_id"])
        ).send(
            random.choice(gf.readlines()).format(
                member.mention, member.name, member.discriminator
            )
        )
        await member.guild.get_channel(
            int(config["GROOVE"]["verification_channel_id"])
        ).send(wf.read())


@bot.event
async def on_member_remove(member):
    with open("resources/farewells.txt", "r") as f:
        await member.guild.get_channel(
            int(config["GROOVE"]["general_channel_id"])
        ).send(
            random.choice(f.readlines()).format(
                member.mention, member.name, member.discriminator
            )
        )


@bot.event
async def on_command_error(ctx, error):
    if hasattr(error, "original"):
        if isinstance(error, ValidationError):
            await failure_message(
                ctx, "One or more of your arguments in your command may be too long."
            )
        elif isinstance(error, IntegrityError):
            await failure_message(ctx, "Creation failed. Please use a unique acronym.")
        else:
            await failure_message(
                ctx, "An unexpected error has occurred, please inform a developer."
            )
        raise error.original
    elif not isinstance(error, CommandNotFound):
        await failure_message(ctx, str(error))


@bot.command()
async def get(ctx, acronym):
    acronym_upper = acronym.upper()
    if await Album.filter(acronym=acronym_upper).exists():
        album = await Album.filter(acronym=acronym_upper).first()
        music = await Music.filter(album=album).all()
        if music:
            embed = discord.Embed(colour=discord.Colour.blue())
            embed.set_author(name="Here's a guide to all of the music abbreviations!")
            for song in music:
                embed.add_field(name=song.acronym, value=song.value, inline=True)
            await success_message(ctx, "Album retrieved!", album, embed)
        else:
            await failure_message(ctx, f"Album {album} contains no music.")
    elif await Music.filter(acronym=acronym_upper).exists():
        music = (
            await Music.filter(acronym=acronym_upper).prefetch_related("album").first()
        )
        await success_message(ctx, "Music retrieved!", music)
    elif await Abbreviation.filter(acronym=acronym_upper).exists():
        abbreviation = await Abbreviation.filter(acronym=acronym_upper).first()
        await success_message(ctx, "Abbreviation retrieved!", abbreviation)
    elif (
        ctx.channel.permissions_for(ctx.author).manage_messages
        and acronym.isnumeric()
        and await Strike.filter(id=acronym).exists()
    ):
        strike = await Strike.filter(id=acronym).first()
        await success_message(ctx, "Strike retrieved!", strike)
    else:
        await failure_message(ctx, "Please try again with a different acronym.")


if __name__ == "__main__":
    setup_cogs(bot)
    bot.run(config["GROOVE"]["token"], bot=True)
