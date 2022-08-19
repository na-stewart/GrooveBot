import asyncio
import random
from colorsys import hsv_to_rgb
from configparser import ConfigParser

import discord
from PIL import ImageDraw, ImageFont, Image
from discord import default_permissions, SlashCommandGroup
from tortoise import Tortoise

from groovebot.core.models import Album, Music, Strike

config = ConfigParser()
config.read("groove.ini")
bot = discord.Bot()
music_group = SlashCommandGroup("music", "Retrieve and manage music.")
album_group = SlashCommandGroup("album", "Retrieve and manage albums.")
strike_group = SlashCommandGroup("strike", "Retrieve and manage strikes.")


@bot.event
async def on_ready():
    await Tortoise.init(
        db_url=config.get("TORTOISE", "database_url"),
        modules={"models": ["groovebot.core.models"]},
    )
    await Tortoise.generate_schemas()
    print("Groovebot initialized.")


@bot.event
async def on_member_join(member):
    with open("resources/greetings.txt", "r") as f:
        await member.guild.get_channel(
            int(config["GROOVE"]["general_channel_id"])
        ).send(
            random.choice(f.readlines()).format(
                member.mention, member.name, member.discriminator
            )
        )
    await member.guild.get_channel(
        int(config["GROOVE"]["verification_channel_id"])
    ).send(config["GROOVE"]["message_on_join"])


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
async def on_application_command_error(
        ctx: discord.ApplicationContext, error: discord.DiscordException
):
    await response(ctx, str(error), success=False)


async def response(
        ctx: discord.ApplicationContext,
        message: str,
        *,
        success: bool = True,
        model=None,
        embed: discord.Embed = None,
):
    if success:
        response_message = f":white_check_mark: **{message}**"
        if model:
            response_message += f"\n{str(model)}"
    else:
        response_message = f":x: **{message}**"
    await ctx.respond(response_message, embed=embed)


@album_group.command(
    name="list", description="List all of Groovebot's available albums."
)
async def list_albums(ctx: discord.ApplicationContext):
    albums = await Album.all()
    if albums:
        embed = discord.Embed(colour=discord.Colour.purple())
        embed.set_author(name="Here are all of the album entries.")
        for album in albums:
            embed.add_field(name=album.acronym, value=album.title, inline=True)
        await response(ctx, "Albums retrieved!", embed=embed)
    else:
        await response(ctx, "No albums have been created.", success=False)


@album_group.command(name="create", description="Create new album entry.")
@default_permissions(manage_messages=True)
async def create_album(
        ctx: discord.ApplicationContext, acronym: str, title: str, description: str
):
    album = await Album.create(
        acronym=acronym.upper(), title=title, description=description
    )
    await response(ctx, "Album added to database!", model=album)


@album_group.command(name="delete", description="Delete album entry.")
@default_permissions(manage_messages=True)
async def delete_album(ctx: discord.ApplicationContext, acronym: str):
    if await Album.filter(acronym=acronym.upper()).delete() == 1:
        await response(ctx, "Album successfully deleted from database.")
    else:
        await response(ctx, "Album has not been deleted successfully.")


@music_group.command(name="create", description="Create new music entry.")
@default_permissions(manage_messages=True)
async def create_music(
        ctx: discord.ApplicationContext,
        acronym: str,
        title: str,
        album: str = None,
        url: str = None,
):
    associated_album = (
        await Album.filter(acronym=album.upper()).first() if album else None
    )
    music = await Music.create(
        album=associated_album, acronym=acronym.upper(), title=title, url=url
    )
    await response(ctx, "Music added to database!", model=music)


@music_group.command(name="delete", description="Delete music entry.")
@default_permissions(manage_messages=True)
async def delete_music(ctx: discord.ApplicationContext, acronym: str):
    if await Music.filter(acronym=acronym.upper()).delete() == 1:
        await response(ctx, "Music successfully deleted from database.")
    else:
        await response(ctx, "Music has not been deleted successfully.")


@strike_group.command(name="create", description="Create a strike against a rule breaker >:(.")
@default_permissions(manage_messages=True)
async def create_strike(ctx: discord.ApplicationContext, member: discord.Member, reason: str, proof: str = "Not provided."):
    if ctx.message.attachments:
        for attachment in ctx.message.attachments:
            proof += f" {attachment.url}\n"
    strike = await Strike.create(member_id=member.id, reason=reason, proof=proof)
    await response(
        ctx, f"Strike against {member.mention} added to database!", model=strike
    )
    await member.send(
        f"You have incurred a strike against you! Please follow the rules. **Reason:** {strike.reason}"
    )


@strike_group.command(name="get", description="Retrieve a rule breaker's strikes.")
@default_permissions(manage_messages=True)
async def get_strikes(ctx: discord.ApplicationContext, member: discord.Member):
    strikes = await Strike.filter(member_id=member.id).all()
    if strikes:
        embed = discord.Embed(colour=discord.Colour.red())
        embed.set_author(
            name=f"Here's a list of all of the strikes against {member.display_name}!"
        )
        for strike in strikes:
            embed.add_field(
                name=f"ID: {strike.id}", value=strike.reason, inline=True
            )
        await response(ctx, "Strikes retrieved!", embed=embed)
    else:
        await response(
            ctx, f"No strikes associated with {member.mention} could be found!", success=False
        )


@strike_group.command(name="delete", description="Delete a rule breaker's strike.")
@default_permissions(manage_messages=True)
async def delete_strike(ctx: discord.ApplicationContext, strike_id: int):
    if await Strike.filter(id=strike_id).delete() == 1:
        await response(ctx, f"Strike with id {strike_id} deleted from database!")
    else:
        await response(ctx, f"Could not find strike with id {strike_id}.")


@bot.slash_command(name="whatis", description="Deciphers acronyms used in this server.")
async def what_is(ctx: discord.ApplicationContext, acronym: str):
    acronym_upper = acronym.upper()
    if await Album.filter(acronym=acronym_upper).exists():
        album = await Album.filter(acronym=acronym_upper).first()
        music = await Music.filter(album=album).all()
        embed = None
        if music:
            embed = discord.Embed(colour=discord.Colour.blue())
            embed.set_author(name="Here are all of this album's music. ")
            for song in music:
                embed.add_field(name=song.acronym, value=song.title, inline=True)
        await response(ctx, "Album retrieved!", model=album, embed=embed)
    elif await Music.filter(acronym=acronym_upper).exists():
        music = (
            await Music.filter(acronym=acronym.upper())
            .prefetch_related("album")
            .first()
        )
        await response(ctx, "Music retrieved!", model=music)
    else:
        await response(
            ctx, "I don't know what this acronym means, sorry!", success=False
        )


@bot.slash_command(name="fact", description="Random Animusic fact.")
async def fact(ctx: discord.ApplicationContext):
    with open("resources/facts.txt", "r") as f:
        await ctx.respond(random.choice(f.readlines()))


@bot.slash_command(name="verify", description="Verify your account to access server.")
async def verify(ctx: discord.ApplicationContext):
    role = ctx.guild.get_role(int(config["GROOVE"]["verified_role_id"]))
    if len(ctx.author.roles) <= 1:
        await ctx.author.add_roles(role)
        await response(ctx, "You have been verified.")
    else:
        await response(ctx, "You have already been verified.", success=False)


@bot.slash_command(
    name="neuropol",
    description="Parses message into neuropol font. For color use RGB, HEX, or rainbow.",
)
async def neuropol(
        ctx: discord.ApplicationContext, message: str, color: str = "#FFFFFF"
):
    if len(message) < 35:
        font = ImageFont.truetype("./resources/neuropol.ttf", 35)
        width = 0
        for i in range(len(message)):
            width += font.getbbox(message[i])[2]
        img = Image.new("RGBA", (width + 20, 40), (255, 0, 0, 0))
        if color == "rainbow":
            spacing = 0
            rgb_values = []
            image_draw = ImageDraw.Draw(img)
            for i in range(len(message)):
                map_range = 0 + (((i - 0) / (len(message) - 0)) * (1 - 0))
                rgb_values.append(
                    tuple(
                        round(map_range * 255)
                        for map_range in hsv_to_rgb(map_range, 1, 1)
                    )
                )
                image_draw.text(
                    (10 + spacing, 0), text=message[i], fill=rgb_values[i], font=font
                )
                spacing += font.getbbox(message[i])[2]
        else:
            ImageDraw.Draw(img).text((10, 5), message, fill=color, font=font)
        await asyncio.get_running_loop().run_in_executor(
            None, img.save, "resources/neuropol.png"
        )
        await ctx.respond(file=discord.File("resources/neuropol.png"))
    else:
        await response(ctx, "Message cannot be over 35 characters.", success=False)


bot.add_application_command(album_group)
bot.add_application_command(music_group)
bot.add_application_command(strike_group)
if __name__ == "__main__":
    bot.run(config.get("GROOVE", "TOKEN"))
