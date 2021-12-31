import random

import discord
from discord.ext import commands
from discord.ext.commands import has_permissions

from groovebot.core.models import Album, Music, Abbreviation, Strike
from groovebot.core.utils import (
    read_file,
    failure_message,
    success_message,
    config,
    text_to_neuropol,
)


class MusicCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @has_permissions(manage_messages=True)
    @commands.command(name="createmusic")
    async def create_music(self, ctx, album_acronym, acronym, title, url):
        album = await Album.filter(acronym=album_acronym.upper()).first()
        if album:
            music = await Music.create(
                album=album, acronym=acronym.upper(), value=title, url=url
            )
            await success_message(ctx, "Music added to database!", music)
        else:
            await failure_message(ctx, "No album with passed acronym exists.")

    @has_permissions(manage_messages=True)
    @commands.command(name="deletemusic")
    async def delete_music(self, ctx, acronym):
        if await Music.filter(acronym=acronym.upper()).delete() == 1:
            await success_message(ctx, "Music successfully deleted from database.")
        else:
            await failure_message(ctx, "Music has not been deleted successfully.")


class AlbumCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="getalbums")
    async def get_albums(self, ctx):
        albums = await Album.all()
        if albums:
            embed = discord.Embed(colour=discord.Colour.purple())
            embed.set_author(name="Here's a guide to all of the album abbreviations!")
            for album in albums:
                embed.add_field(name=album.acronym, value=album.value, inline=True)
            await success_message(ctx, "Albums retrieved!", embed=embed)
        else:
            await failure_message(ctx, "No albums have been created.")

    @has_permissions(manage_messages=True)
    @commands.command(name="createalbum")
    async def create_album(self, ctx, acronym, title, description):
        album = await Album.create(
            acronym=acronym.upper(), value=title, description=description
        )
        await success_message(ctx, "Album added to database.", album)

    @has_permissions(manage_messages=True)
    @commands.command(name="deletealbum")
    async def delete_album(self, ctx, acronym):
        if await Album.filter(acronym=acronym.upper()).delete() == 1:
            album = await Album.filter(acronym=acronym.upper()).first()
            await Music.filter(album=album).delete()
            await success_message(ctx, "Album deleted from database!")
        else:
            await failure_message(ctx, "No album with passed acronym exists.")


class AbbreviationCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="getabbreviations")
    async def get_abbreviations(self, ctx):
        abbreviations = await Abbreviation.all()
        if abbreviations:
            embed = discord.Embed(colour=discord.Colour.red())
            embed.set_author(
                name="Here's a guide to some of the server's abbreviations!"
            )
            for abbreviation in abbreviations:
                embed.add_field(
                    name=abbreviation.acronym, value=abbreviation.value, inline=True
                )
            await success_message(ctx, "Abbreviations retrieved!", embed=embed)
        else:
            await failure_message(ctx, "No abbreviations have been created.")

    @has_permissions(manage_messages=True)
    @commands.command(name="createabbreviation")
    async def create_abbreviation(self, ctx, acronym, description):
        abbreviation = await Abbreviation.create(
            acronym=acronym.upper(), value=description
        )
        await success_message(ctx, "Abbreviation added to database!", abbreviation)

    @has_permissions(manage_messages=True)
    @commands.command(name="deleteabbreviation")
    async def delete_abbreviation(self, ctx, acronym):
        if await Abbreviation.filter(acronym=acronym.upper()).delete() == 1:
            await success_message(ctx, "Abbreviation deleted from database!")
        else:
            await failure_message(ctx, "No abbreviation with passed acronym exists.")


class MiscCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def fact(self, ctx):
        await ctx.send(random.choice(await read_file("facts.txt", True)))

    @commands.command()
    async def help(self, ctx):
        await ctx.send(await read_file("help.txt"))

    @commands.command()
    async def neuropol(self, ctx, *args):
        neuropol_img_file = "neuropol.png"
        try:
            await text_to_neuropol(" ".join(args[:-1]), args[-1])
            await ctx.send(file=discord.File(neuropol_img_file))
        except ValueError:
            try:
                await text_to_neuropol(" ".join(args))
                await ctx.send(file=discord.File(neuropol_img_file))
            except ValueError:
                await failure_message(ctx, "Message cannot be over 35 characters.")

    @has_permissions(manage_messages=True)
    @commands.command(name="welcometest")
    async def welcome_test(self, ctx):
        await ctx.send(await read_file("welcome.txt"))


class ModerationCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @has_permissions(manage_messages=True)
    @commands.command(name="ahelp")
    async def admin_help(self, ctx):
        await ctx.send(await read_file("ahelp.txt"))

    @has_permissions(ban_members=True)
    @commands.command()
    async def ban(self, ctx, member: discord.Member, reason):
        await member.ban(reason=reason)
        await member.send(
            f"You have been banned from the Animusic server. If you would like to submit an appeal, "
            f"you can click here: https://forms.gle/FmkxeXaXSsUpS6Vv7 \nReason: {reason}"
        )
        await success_message(
            ctx,
            f"Successfully banned user {member.mention} ({member}) for reason: {reason}.",
        )

    @has_permissions(manage_messages=True)
    @commands.command()
    async def strike(self, ctx, member: discord.Member, reason, proof="Not provided."):
        if ctx.message.attachments:
            for attachment in ctx.message.attachments:
                proof += f" {attachment.url}\n"
        strike = await Strike.create(member_id=member.id, reason=reason, proof=proof)
        await success_message(
            ctx, f"Strike against {member.mention} added to database!", strike
        )
        await member.send(
            f"You have incurred a strike against you! Please follow the rules. **Reason:** {strike.reason}"
        )

    @has_permissions(manage_messages=True)
    @commands.command(name="getstrikes")
    async def get_strikes(self, ctx, member: discord.Member):
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
            await success_message(ctx, "Strikes retrieved!", embed=embed)
        else:
            await failure_message(
                ctx, f"No strikes associated with {member.mention} could be found!"
            )

    @has_permissions(manage_messages=True)
    @commands.command(name="deletestrike")
    async def delete_strike(self, ctx, number):
        if await Strike.filter(id=number).delete() == 1:
            await success_message(ctx, f"Strike id {number} deleted from database!")
        else:
            await failure_message(ctx, f"Could not find strike with id {number}.")

    @commands.command()
    async def verify(self, ctx):
        if len(ctx.author.roles) <= 1:
            role = ctx.guild.get_role(int(config["GROOVE"]["verified_role_id"]))
            await ctx.author.add_roles(role)


class RetrievalCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def _get_album(self, ctx, album):
        music = await Music.filter(album=album).all()
        if music:
            embed = discord.Embed(colour=discord.Colour.blue())
            embed.set_author(name="Here's a guide to all of the music abbreviations!")
            for song in music:
                embed.add_field(name=song.acronym, value=song.value, inline=True)
            await success_message(ctx, "Album retrieved!", album, embed)
        else:
            await failure_message(ctx, f"Album {album} contains no music.")

    @commands.command()
    async def get(self, ctx, acronym):
        acronym_upper = acronym.upper()
        if await Album.filter(acronym=acronym_upper).exists():
            album = await Album.filter(acronym=acronym_upper).first()
            await self._get_album(ctx, album)
        elif await Music.filter(acronym=acronym_upper).exists():
            music = (
                await Music.filter(acronym=acronym_upper)
                .prefetch_related("album")
                .first()
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
