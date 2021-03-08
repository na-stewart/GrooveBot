import random

import discord
from discord.ext import commands
from discord.ext.commands import has_permissions
from tortoise.exceptions import IntegrityError

from groovebot.core.config import config
from groovebot.core.models import Album, Music, Abbreviation
from groovebot.core.utils import read_file, failure_message, success_message


class MusicCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='getmusic')
    async def get_music(self, ctx, acronym):
        music = await Music().filter(acronym=acronym).first()
        if music:
            await success_message(ctx, 'Music retrieved!', str(music))
        else:
            await failure_message(ctx, 'No music with passed acronym exists. Perhaps you should try '
                                       '.getabbreviation?')

    @has_permissions(administrator=True)
    @commands.command(name='createmusic')
    async def create_music(self, ctx, album_acronym, acronym, title, url):
        album = await Album().filter(acronym=album_acronym).first()
        if album:
            try:
                music = await Music().create(parent_uid=album.uid, acronym=acronym, value=title,
                                             url=url)
                await success_message(ctx, 'Music added to database!', music)
            except IntegrityError:
                await failure_message(ctx, 'Music with passed acronym exists or too many characters.')
        else:
            await failure_message(ctx, 'No album with passed acronym exists.')

    @has_permissions(administrator=True)
    @commands.command(name='deletemusic')
    async def delete_music(self, ctx, acronym):
        if await Music().filter(acronym=acronym).delete() == 1:
            await success_message(ctx, 'Music successfully deleted from database.')
        else:
            await failure_message(ctx, 'Music has not been deleted successfully.')


class AlbumCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='getalbums')
    async def get_albums(self, ctx):
        albums = await Album().all()
        if albums:
            embed = discord.Embed(colour=discord.Colour.purple())
            embed.set_author(name='Here\'s a guide to all of the album abbreviations!')
            for album in albums:
                embed.add_field(name=album.acronym, value=album.value, inline=True)
            await success_message(ctx, 'Albums retrieved! Use **getalbum** to retrieve album content.',
                                  embed=embed)
        else:
            await failure_message(ctx, 'No albums have been created.')

    @commands.command(name='getalbum')
    async def get_album(self, ctx, acronym):
        album = await Album().filter(acronym=acronym).first()
        if album:
            music = await Music().filter(parent_uid=album.uid).all()
            if music:
                embed = discord.Embed(colour=discord.Colour.blue())
                embed.set_author(name='Here\'s a guide to all of the music abbreviations!')
                for song in music:
                    embed.add_field(name=song.acronym, value=song.value, inline=True)
                await success_message(ctx, 'Album retrieved! Use **getmusic** to retrieve music content.', album, embed)
            else:
                await failure_message(ctx, 'This album contains no music.')
        else:
            await failure_message(ctx, 'No album with passed acronym exists. Perhaps you should try '
                                       '.getabbreviation?')

    @has_permissions(administrator=True)
    @commands.command(name='createalbum')
    async def create_album(self, ctx, acronym, title, description):
        try:
            album = await Album().create(acronym=acronym, value=title, description=description)
            await success_message(ctx, 'Album added to database.', album)
        except IntegrityError:
            await failure_message(ctx, 'Album with passed acronym exists or too many characters.')

    @has_permissions(administrator=True)
    @commands.command(name='deletealbum')
    async def delete_album(self, ctx, acronym):
        if await Album().filter(acronym=acronym).delete() > 0:
            await success_message(ctx, 'Album deleted from database!')
        else:
            await failure_message(ctx, 'No album with passed acronym exists.')


class AbbreviationCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @has_permissions(administrator=True)
    @commands.command(name='createabbreviation')
    async def create_abbreviation(self, ctx, acronym, description):
        try:
            abbreviation = await Abbreviation().create(acronym=acronym, value=description)
            await success_message(ctx, 'Abbreviation added to database!', abbreviation)
        except IntegrityError:
            await failure_message(ctx, 'Abbreviation with passed acronym exists or too many characters.')

    @has_permissions(administrator=True)
    @commands.command(name='deleteabbreviation')
    async def delete_abbreviation(self, ctx, acronym):
        if await Abbreviation().filter(acronym=acronym).delete() > 0:
            await success_message(ctx, 'Abbreviation deleted from database!')
        else:
            await failure_message(ctx, 'No abbreviation with passed acronym exists.')

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

    @commands.command(name='getabbreviation')
    async def get_abbreviation(self, ctx, acronym):
        abbreviation = await Abbreviation().filter(acronym=acronym).first()
        if abbreviation:
            await success_message(ctx, 'Abbreviation retrieved!', str(abbreviation))
        else:
            await failure_message(ctx, 'No abbreviation with passed acronym exists. Perhaps you should try '
                                       '.getmusic or .getalbum?')


class HelpCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def help(self, ctx):
        await ctx.send(read_file('help.txt'))

    @has_permissions(administrator=True)
    @commands.command(name='adminhelp')
    async def admin_help(self, ctx):
        await ctx.send(read_file('adminhelp.txt'))


class ExtrasCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def fact(self, ctx):
        await ctx.send(random.choice(read_file('facts.txt', True)))


class ModerationCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @has_permissions(administrator=True)
    @commands.command()
    async def suspend(self, ctx, user: discord.Member):
        try:
            await user.add_roles(ctx.guild.get_role(int(config['GROOVE']['suspended_id'])))
            await user.remove_roles(ctx.guild.get_role(int(config['GROOVE']['verified_id'])))
            await user.send('You are temporarily suspended from the Animusic Discord server. '
                            'Please await further information from the staff.')
            await success_message(ctx, 'Member has been suspended!')
        except AttributeError:
            await failure_message(ctx, 'Could not suspend! Either your suspended role or verified role id in the '
                                       'config is incorrect!')

    @has_permissions(administrator=True)
    @commands.command()
    async def pardon(self, ctx, user: discord.Member):
        try:
            await user.add_roles(ctx.guild.get_role(int(config['GROOVE']['verified_id'])))
            await user.remove_roles(ctx.guild.get_role(int(config['GROOVE']['suspended_id'])))
            await user.send('You are no longer suspended and your access to the Animusic Discord server has '
                            'been reinstated. Please follow the rules!')
            await success_message(ctx, 'Member has been pardoned!')
        except AttributeError:
            await failure_message(ctx, 'Could not suspend! Either your suspended role or verified role id in the '
                                       'config is incorrect!')
