from colorsys import hsv_to_rgb
from configparser import ConfigParser

import discord
from PIL import ImageDraw, ImageFont, Image
from discord import default_permissions, SlashCommandGroup
from tortoise import Tortoise

from groovebot.core.models import Album, Music

config = ConfigParser()
config.read("groove.ini")
bot = discord.Bot()
music_group = SlashCommandGroup("music", "Retrieve and manage music.")
album_group = SlashCommandGroup("album", "Retrieve and manage albums.")


@bot.event
async def on_ready():
    await Tortoise.init(
        db_url=config.get("TORTOISE", "database_url"),
        modules={"models": ["groovebot.core.models"]},
    )
    await Tortoise.generate_schemas()
    print("Groovebot initialized.")


async def response(ctx, message, *, success=True, model=None, embed=None):
    if success:
        response_message = f":white_check_mark: **{message}**"
        if model:
            response_message += f"\n{str(model)}"
    else:
        response_message = f":x: **{message}**"
    await ctx.respond(response_message, embed=embed)


@album_group.command(name="list", description="List all of Groovebot's available albums.")
async def list_albums(ctx):
    albums = await Album.all()
    if albums:
        embed = discord.Embed(colour=discord.Colour.purple())
        embed.set_author(name="Here are all of the album entries.")
        for album in albums:
            embed.add_field(name=album.acronym, value=album.title, inline=True)
        await response(ctx, "Albums retrieved!", embed=embed)
    else:
        await response(ctx, "No albums have been created.", success=False)


@album_group.command(name="get", description="Retrieve album title, description, and music.")
async def get_album(ctx, acronym: str):
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
        await ctx.send("Use **/music get** for more information.")
    else:
        await response(ctx, f"Album does not exist!", success=False)


@album_group.command(name="create", description="Create new album entry.")
@default_permissions(manage_messages=True)
async def create_album(ctx, acronym: str, title: str, description: str):
    album = await Album.create(
        acronym=acronym.upper(), title=title, description=description
    )
    await response(ctx, "Album added to database!", model=album)


@album_group.command(name="delete", description="Delete album entry.")
@default_permissions(manage_messages=True)
async def delete_album(ctx, acronym: str):
    if await Album.filter(acronym=acronym.upper()).delete() == 1:
        await response(ctx, "Album successfully deleted from database.")
    else:
        await response(ctx, "Album has not been deleted successfully.")


@music_group.command(name="get", description="Retrieve music title and URL.")
async def get_music(ctx, acronym: str):
    music = (
        await Music.filter(acronym=acronym.upper()).prefetch_related("album").first()
    )
    await response(ctx, "Music retrieved!", model=music)


@music_group.command(name="create", description="Create new music entry.")
@default_permissions(manage_messages=True)
async def create_music(
        ctx, acronym: str, title: str, album: str = None, url: str = None
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
async def delete_music(ctx, acronym: str):
    if await Music.filter(acronym=acronym.upper()).delete() == 1:
        await response(ctx, "Music successfully deleted from database.")
    else:
        await response(ctx, "Music has not been deleted successfully.")


@bot.slash_command(
    name="neuropol",
    description="Parses message into neuropol font. For color use RGB, HEX, or rainbow.",
)
async def neuropol(ctx, message: str, color: str = "#FFFFFF"):
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
        img.save("resources/neuropol.png")
        await ctx.respond(file=discord.File("resources/neuropol.png"))
    else:
        await response(ctx, "Message cannot be over 35 characters.", success=False)


bot.add_application_command(album_group)
bot.add_application_command(music_group)
if __name__ == "__main__":
    bot.run(config.get("GROOVE", "TOKEN"))
