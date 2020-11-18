import os

import discord
from discord.ext import commands
from discord.ext.commands import has_permissions
from tortoise.exceptions import IntegrityError

from groovebot.core.models import Album, Music, YTDLSource, Abbreviation
from groovebot.core.utils import read_file, send_failure_message, send_success_message


class MusicCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def _attempt_voice_connect(self, channel):
        try:
            await channel.connect()
        except discord.ClientException:
            pass

    async def play_music(self, ctx, music):
        try:
            channel = ctx.author.voice.channel
            await self._attempt_voice_connect(channel)
            for client in self.bot.voice_clients:
                if client.channel is channel:
                    filename, player = await YTDLSource.from_url(music.url)
                    client.play(player, after=lambda e: os.remove(filename))
        except AttributeError:
            pass

    @commands.command()
    async def getalbums(self, ctx):
        albums = await Album().all()
        if albums:
            embed = discord.Embed(colour=discord.Colour.purple())
            embed.set_author(name='Here\'s a guide to all of the album abbreviations!')
            for album in albums:
                embed.add_field(name=album.acronym, value=album.value, inline=True)
            await send_success_message(ctx, 'Albums retrieved!', embed=embed)
        else:
            await send_failure_message(ctx, 'No albums have been created.')

    @commands.command()
    async def getalbum(self, ctx, acronym):
        album = await Album().filter(acronym=acronym).first()
        if album:
            music = await Music().filter(parent_uid=album.uid).all()
            embed = None
            if music:
                embed = discord.Embed(colour=discord.Colour.blue())
                embed.set_author(name='Here\'s a guide to all of the music abbreviations!')
                for song in music:
                    embed.add_field(name=song.acronym, value=song.value, inline=True)
            await send_success_message(ctx, 'Album retrieved!', album, embed)
        else:
            await send_failure_message(ctx, 'No album with passed acronym exists.')

    @commands.command()
    async def getmusic(self, ctx, acronym):
        music = await Music().filter(acronym=acronym).first()
        if music:
            await send_success_message(ctx, 'Music retrieved, join a voice channel to play!', str(music))
            await self.play_music(ctx, music)
        else:
            await send_failure_message(ctx, 'No music with passed acronym exists.')

    @has_permissions(administrator=True)
    @commands.command()
    async def createalbum(self, ctx, acronym, title, description):
        try:
            album = await Album().create(acronym=acronym, value=title, description=description)
            await send_success_message(ctx, 'Album added to database.', album)
        except IntegrityError:
            await send_failure_message(ctx, 'Album with passed acronym exists or too many characters.')

    @has_permissions(administrator=True)
    @commands.command()
    async def deletealbum(self, ctx, acronym):
        if await Album().filter(acronym=acronym).delete() > 0:
            await send_success_message(ctx, 'Album deleted from database!')
        else:
            await send_failure_message(ctx, 'No album or music with passed acronym exists.')

    @has_permissions(administrator=True)
    @commands.command()
    async def createmusic(self, ctx, album_acronym, acronym, title, url):
        album = await Album().filter(acronym=album_acronym).first()
        if album:
            try:
                music = await Music().create(parent_uid=album.uid, acronym=acronym, value=title,
                                             url=url)
                await send_success_message(ctx, 'Music added to database!', music)
            except IntegrityError:
                await send_failure_message(ctx, 'Music with passed acronym exists or too many characters.')
        else:
            await send_failure_message(ctx, 'No album with passed acronym exists.')

    @has_permissions(administrator=True)
    @commands.command()
    async def deletemusic(self, ctx, acronym):
        if await Music().filter(acronym=acronym).delete() > 0:
            await send_success_message(ctx, 'Music successfully deleted from database.')
        else:
            await send_failure_message(ctx, 'No music with this acronym could be found.')


class AbbreviationCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @has_permissions(administrator=True)
    @commands.command()
    async def createabbreviation(self, ctx, acronym, description):
        try:
            abbreviation = await Abbreviation().create(acronym=acronym, value=description)
            await send_success_message(ctx, 'Abbreviation added to database!', abbreviation)
        except IntegrityError:
            await send_failure_message(ctx, 'Abbreviation with passed acronym exists or too many characters.')

    @has_permissions(administrator=True)
    @commands.command()
    async def deleteabbreviation(self, ctx, acronym):
        if await Abbreviation().filter(acronym=acronym).delete() > 0:
            await send_success_message(ctx, 'Abbreviation deleted from database!')
        else:
            await send_failure_message(ctx, 'No abbreviation with passed acronym exists.')

    @commands.command()
    async def getabbreviations(self, ctx):
        abbreviations = await Abbreviation.all()
        if abbreviations:
            embed = discord.Embed(colour=discord.Colour.red())
            embed.set_author(name='Here\'s a guide to all of the server\'s abbreviations!')
            for abbreviation in abbreviations:
                embed.add_field(name=abbreviation.acronym, value=abbreviation.value, inline=True)
            await send_success_message(ctx, 'Abbreviations retrieved!', embed=embed)
        else:
            await send_failure_message(ctx, 'No abbreviations have been created.')


class EasterEggCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def pee(self, ctx):
        await ctx.send('poo')

    @commands.command(aliases=['pd3sg'])
    async def pd3(self, ctx):
        await ctx.send('https://docs.google.com/document/d/18pU0sbrRfMq3bqw-WYSVNHmGMCRqZuT0KJZHtStWA58/edit')


class UtilsCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def help(self, ctx):
        await ctx.send(await read_file('help.txt'))

    @has_permissions(administrator=True)
    @commands.command()
    async def adminhelp(self, ctx):
        await ctx.send(await read_file('adminhelp.txt'))

    @commands.command()
    async def stop(self, ctx):
        for client in self.bot.voice_clients:
            if client.channel is ctx.author.voice.channel:
                client.stop()

    @commands.command()
    async def leave(self, ctx):
        await self.stop(ctx)
        for client in self.bot.voice_clients:
            if client.channel is ctx.author.voice.channel:
                await client.disconnect()
