import asyncio
import random

import aiofiles.os
import discord
from PIL import ImageFont, Image, ImageDraw
from discord.ext import commands
from discord.ext.commands import has_permissions

from groovebot.core.models import Album, Music, Abbreviation, Strike
from groovebot.core.utils import read_file, failure_message, success_message, config


class MusicCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @has_permissions(manage_messages=True)
    @commands.command(name='createmusic')
    async def create_music(self, ctx, album_acronym, acronym, title, url):
        album = await Album.filter(acronym=album_acronym.upper()).first()
        if album:
            music = await Music.create(album=album, acronym=acronym.upper(), value=title,
                                       url=url)
            await success_message(ctx, 'Music added to database!', music)
        else:
            await failure_message(ctx, 'No album with passed acronym exists.')

    @has_permissions(manage_messages=True)
    @commands.command(name='deletemusic')
    async def delete_music(self, ctx, acronym):
        if await Music.filter(acronym=acronym.upper()).delete() == 1:
            await success_message(ctx, 'Music successfully deleted from database.')
        else:
            await failure_message(ctx, 'Music has not been deleted successfully.')


class AlbumCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='getalbums')
    async def get_albums(self, ctx):
        albums = await Album.all()
        if albums:
            embed = discord.Embed(colour=discord.Colour.purple())
            embed.set_author(name='Here\'s a guide to all of the album abbreviations!')
            for album in albums:
                embed.add_field(name=album.acronym, value=album.value, inline=True)
            await success_message(ctx, 'Albums retrieved!', embed=embed)
        else:
            await failure_message(ctx, 'No albums have been created.')

    @has_permissions(manage_messages=True)
    @commands.command(name='createalbum')
    async def create_album(self, ctx, acronym, title, description):
        album = await Album.create(acronym=acronym.upper(), value=title, description=description)
        await success_message(ctx, 'Album added to database.', album)

    @has_permissions(manage_messages=True)
    @commands.command(name='deletealbum')
    async def delete_album(self, ctx, acronym):
        if await Album.filter(acronym=acronym.upper()).delete() == 1:
            album = await Album.filter(acronym=acronym.upper()).first()
            await Music.filter(album=album).delete()
            await success_message(ctx, 'Album deleted from database!')
        else:
            await failure_message(ctx, 'No album with passed acronym exists.')


class AbbreviationCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='getabbreviations')
    async def get_abbreviations(self, ctx):
        abbreviations = await Abbreviation.all()
        if abbreviations:
            embed = discord.Embed(colour=discord.Colour.red())
            embed.set_author(name='Here\'s a guide to some of the server\'s abbreviations!')
            for abbreviation in abbreviations:
                embed.add_field(name=abbreviation.acronym, value=abbreviation.value, inline=True)
            await success_message(ctx, 'Abbreviations retrieved!', embed=embed)
        else:
            await failure_message(ctx, 'No abbreviations have been created.')

    @has_permissions(manage_messages=True)
    @commands.command(name='createabbreviation')
    async def create_abbreviation(self, ctx, acronym, description):
        abbreviation = await Abbreviation.create(acronym=acronym.upper(), value=description)
        await success_message(ctx, 'Abbreviation added to database!', abbreviation)

    @has_permissions(manage_messages=True)
    @commands.command(name='deleteabbreviation')
    async def delete_abbreviation(self, ctx, acronym):
        if await Abbreviation.filter(acronym=acronym.upper()).delete() == 1:
            await success_message(ctx, 'Abbreviation deleted from database!')
        else:
            await failure_message(ctx, 'No abbreviation with passed acronym exists.')


class MiscCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def fact(self, ctx):
        await ctx.send(random.choice(await read_file('facts.txt', True)))

    @commands.command()
    async def verify(self, ctx):
        if ctx.guild.get_role(int(config['GROOVE']['suspended_role_id'])) not in ctx.author.roles:
            role = ctx.guild.get_role(int(config['GROOVE']['verified_role_id']))
            await ctx.author.add_roles(role)

    @commands.command()
    async def help(self, ctx):
        await ctx.send(await read_file('help.txt'))

    async def text_to_neuropol(self, message):
        font = ImageFont.truetype("./resources/NEUROPOL.ttf", 35)
        loop = asyncio.get_running_loop()
        file = message + '.png'
        img = Image.new('RGBA', (400, 40), (255, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        draw.text((0, 0), message, (255, 255, 255), font=font)
        await loop.run_in_executor(None, img.save, file)
        return file

    @commands.command()
    async def neuropol(self, ctx, *args):
        message = "{}".format(" ".join(args)).upper()
        if len(message) < 18 and message:
            neuropol_img = await self.text_to_neuropol(message)
            await ctx.send(file=discord.File(neuropol_img))
            await aiofiles.os.remove(neuropol_img)
        else:
            await failure_message(ctx, 'Could not parse text to neuropol!')

    @has_permissions(manage_messages=True)
    @commands.command(name='modhelp')
    async def mod_help(self, ctx):
        await ctx.send(await read_file('modhelp.txt'))

    @has_permissions(manage_messages=True)
    @commands.command(name='welcometest')
    async def welcome_test(self, ctx):
        await ctx.send(await read_file('welcome.txt'))


class ModerationCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def get_member_role(self, ctx, suspend):
        return ctx.guild.get_role(int(config['GROOVE']['suspended_role_id'])) if suspend \
            else ctx.guild.get_role(int(config['GROOVE']['verified_role_id']))

    async def handle_member_roles(self, ctx, member, suspend):
        await member.add_roles(self.get_member_role(ctx, suspend))
        await member.remove_roles(self.get_member_role(ctx, not suspend))

    @has_permissions(manage_messages=True)
    @commands.command()
    async def suspend(self, ctx, member: discord.Member):
        await self.handle_member_roles(ctx, member, True)
        await member.send('You are temporarily suspended from the Animusic Discord server. '
                          'Please await further information from the staff.')
        await success_message(ctx, f'{member.mention} has been suspended!')

    @has_permissions(manage_messages=True)
    @commands.command()
    async def pardon(self, ctx, member: discord.Member):
        await self.handle_member_roles(ctx, member, False)
        await member.send('You are no longer suspended and your access to the Animusic Discord server has '
                          'been reinstated. Please follow the rules!')
        await success_message(ctx, f'{member.mention} has been pardoned!')

    @has_permissions(manage_messages=True)
    @commands.command()
    async def strike(self, ctx, member: discord.Member, reason, proof="`Not provided.`"):
        strike = await Strike.create(member_id=member.id, reason=reason, proof=proof)
        await success_message(ctx, f'Strike against {member.mention} added to database!', strike)

    @has_permissions(manage_messages=True)
    @commands.command(name='getstrikes')
    async def get_strikes(self, ctx, member: discord.Member):
        strikes = await Strike.filter(member_id=member.id).all()
        if strikes:
            embed = discord.Embed(colour=discord.Colour.red())
            embed.set_author(name='Here\'s a list of all of the strikes against this member!')
            for strike in strikes:
                embed.add_field(name=strike.id, value=strike.reason, inline=True)
            await success_message(ctx, 'Strikes retrieved!', embed=embed)
        else:
            await failure_message(ctx, 'No strikes associated with this member could be found!')

    @has_permissions(manage_messages=True)
    @commands.command(name='deletestrike')
    async def delete_strike(self, ctx, id):
        if await Strike.filter(id=id).delete() == 1:
            await success_message(ctx, 'Strike deleted from database!')
        else:
            await failure_message(ctx, 'Could not find strike with id.')


class RetrievalCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def _get_album(self, ctx, album):
        music = await Music.filter(album=album).all()
        if music:
            embed = discord.Embed(colour=discord.Colour.blue())
            embed.set_author(name='Here\'s a guide to all of the music abbreviations!')
            for song in music:
                embed.add_field(name=song.acronym, value=song.value, inline=True)
            await success_message(ctx, 'Album retrieved!', album, embed)
        else:
            await failure_message(ctx, 'This album contains no music.')

    @commands.command()
    async def get(self, ctx, acronym):
        acronym_upper = acronym.upper()
        if await Album.filter(acronym=acronym_upper).exists():
            album = await Album.filter(acronym=acronym_upper).first()
            await self._get_album(ctx, album)
        elif await Music.filter(acronym=acronym_upper).exists():
            music = await Music.filter(acronym=acronym_upper).prefetch_related('album').first()
            await success_message(ctx, 'Music retrieved!', music)
        elif await Abbreviation.filter(acronym=acronym_upper).exists():
            abbreviation = await Abbreviation.filter(acronym=acronym_upper).first()
            await success_message(ctx, 'Abbreviation retrieved!', abbreviation)
        elif ctx.channel.permissions_for(ctx.author).manage_messages and acronym.isdigit() and await Strike.filter(id=acronym).exists():
            strike = await Strike.filter(id=acronym).first()
            await success_message(ctx, 'Strike retrieved!', strike)
        else:
            await failure_message(ctx, 'Could not find what you were looking for! Please try again with a different '
                                       'acronym.')
