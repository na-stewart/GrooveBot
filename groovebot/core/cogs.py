import random

import discord
from discord.ext import commands
from discord.ext.commands import has_permissions

from groovebot.core.models import Album, Music, Abbreviation, Strike
from groovebot.core.utils import (
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
        with open("resources/facts.txt", "r") as f:
            await ctx.send(random.choice(f.readlines()))

    @commands.command()
    async def help(self, ctx):
        with open("resources/help.txt", "r") as f:
            await ctx.send(f.read())

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

    @commands.command()
    async def verify(self, ctx):
        role = ctx.guild.get_role(int(config["GROOVE"]["verified_role_id"]))
        if len(ctx.author.roles) <= 1:
            await ctx.author.add_roles(role)


class ModerationCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @has_permissions(manage_messages=True)
    @commands.command(name="ahelp")
    async def admin_help(self, ctx):
        with open("resources/ahelp.txt", "r") as f:
            await ctx.send(f.read())

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


def setup(bot):
    bot.add_cog(AlbumCog(bot))
    bot.add_cog(MusicCog(bot))
    bot.add_cog(MiscCog(bot))
    bot.add_cog(AbbreviationCog(bot))
    bot.add_cog(ModerationCog(bot))
