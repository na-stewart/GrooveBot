import os
import random

import discord
from discord.ext import commands

from discord.ext.commands import has_permissions
from tortoise.exceptions import IntegrityError

from groovebot.core.models import Album, Music, YTDLSource, Abbreviation
from groovebot.core.utils import read_file, send_success_message, send_failure_message


class MusicCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def play_music(self, ctx, music):
        channel = ctx.author.voice.channel
        try:
            await channel.connect()
        except discord.ClientException:
            pass
        for client in self.bot.voice_clients:
            if client.channel is channel:
                filename, player = await YTDLSource.from_url(music.url)
                client.play(player, after=lambda e: os.remove(filename))

    @commands.command()
    async def getalbums(self, ctx):
        albums = await Album().all()
        if albums:
            embed = discord.Embed(colour=discord.Colour.purple())
            embed.set_author(name='Here\'s a guide to all of the album abbreviations!')
            for album in albums:
                embed.add_field(name=album.acronym, value=album.description, inline=True)
            await ctx.send(embed=embed)
        else:
            await send_failure_message(ctx, 'No albums have been created.')

    @commands.command()
    async def getalbum(self, ctx, acronym):
        album = await Album().filter(acronym=acronym).first()
        if album:
            music = await Music().filter(parent_uid=album.uid).all()
            embed = discord.Embed(colour=discord.Colour.blue())
            embed.set_author(name='Here\'s a guide to all of the music abbreviations!')
            for song in music:
                embed.add_field(name=song.acronym, value=song.description, inline=True)
            await ctx.send(embed=embed)
        else:
            await send_failure_message(ctx, 'No album with passed acronym exists.')

    @commands.command()
    async def getmusic(self, ctx, acronym):
        music = await Music().filter(acronym=acronym).first()
        if music:
            success_message = music.url + '\nI can play music too! Simply join a voice channel.'
            await send_success_message(ctx, success_message)
            await self.play_music(ctx, music)
        else:
            await send_failure_message(ctx, 'No album or music with passed acronym exists.')

    @has_permissions(administrator=True)
    @commands.command()
    async def createalbum(self, ctx, acronym, name):
        try:
            album = await Album().create(acronym=acronym, name=name)
            await send_success_message(ctx, album.description + ' added to database.')
        except IntegrityError:
            await send_failure_message(ctx, 'Album with passed acronym exists.')

    @has_permissions(administrator=True)
    @commands.command()
    async def deletealbum(self, ctx, acronym):
        try:
            await Album().filter(acronym=acronym).delete()
        except IntegrityError:
            await send_failure_message(ctx, 'This album could not be deleted due to an error.')

    @has_permissions(administrator=True)
    @commands.command()
    async def createmusic(self, ctx, album_acronym, acronym, name, url):
        album = await Album().filter(acronym=album_acronym).first()
        if album:
            try:
                music = await Music().create(parent_uid=album.uid, acronym=acronym, name=name, url=url)
                await send_success_message(ctx, music.description + ' added to database.')
            except IntegrityError:
                await send_failure_message(ctx, 'Music with passed acronym exists.')
        else:
            await send_failure_message(ctx, 'No album with passed acronym exists.')

    @has_permissions(administrator=True)
    @commands.command()
    async def deletemusic(self, ctx, acronym):
        try:
            await Music().filter(acronym=acronym).delete()
        except IntegrityError:
            raise send_failure_message(ctx, 'Music could not be deleted due to an error.')


class AbbreviationCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @has_permissions(administrator=True)
    @commands.command()
    async def createabbreviation(self, ctx, acronym, name):
        try:
            abbreviation = await Abbreviation().create(acronym=acronym, name=name)
            await send_success_message(ctx, abbreviation.description + ' added to database.')
        except IntegrityError:
            await send_failure_message(ctx, 'Abbreviation with passed acronym exists.')

    @has_permissions(administrator=True)
    @commands.command()
    async def deleteabbreviation(self, ctx, acronym):
        try:
            await Abbreviation().filter(acronym=acronym).delete()
        except IntegrityError:
            raise send_failure_message(ctx, 'Abbreviation could not be deleted due to an error.')

    @commands.command()
    async def getabbreviations(self, ctx):
        abbreviations = await Abbreviation.filter().all()
        if abbreviations:
            embed = discord.Embed(colour=discord.Colour.red())
            embed.set_author(name='Here\'s a guide to all of the server\'s abbreviations!')
            for abbreviation in abbreviations:
                embed.add_field(name=abbreviation.acronym, value=abbreviation.description, inline=True)
            await ctx.send(embed=embed)
        else:
            await send_failure_message(ctx, 'No abbreviations with passed acronym exists.')


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
