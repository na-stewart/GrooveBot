import asyncio
import uuid

import discord
import youtube_dl as youtube_dl
from tortoise import Model, fields


class BaseModel(Model):
    id = fields.IntField(pk=True)
    uid = fields.UUIDField(default=uuid.uuid1, max_length=36)
    parent_uid = fields.UUIDField(null=True, max_length=36)
    date_created = fields.DatetimeField(auto_now_add=True)
    date_updated = fields.DatetimeField(auto_now=True)

    class Meta:
        abstract = True


class Fact(BaseModel):
    content = fields.CharField(max_length=255)


class Abbreviation(BaseModel):
    acronym = fields.CharField(max_length=12, unique=True)
    value = fields.CharField(max_length=45)

    def __str__(self):
        return f"***Acronym:*** `{self.acronym}`\n***Value:*** `{self.value}`"


class Album(Abbreviation):
    description = fields.CharField(max_length=255)

    def __str__(self):
        return f"***Acronym:*** `{self.acronym}`\n***Title:*** `{self.value}`\n***Description:*** `{self.description}`"


class Music(Abbreviation):
    url = fields.CharField(max_length=45)

    def __str__(self):
        return f"***Acronym:*** `{self.acronym}`\n***Title:*** `{self.value}`\n***URL:*** {self.url}"


class YTDLSource(discord.PCMVolumeTransformer):
    youtube_dl.utils.bug_reports_message = lambda: ''

    ytdl_format_options = {
        'format': 'best',
        'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
        'restrictfilenames': True,
        'noplaylist': True,
        'nocheckcertificate': True,
        'ignoreerrors': False,
        'logtostderr': False,
        'quiet': True,
        'no_warnings': True
    }

    ffmpeg_options = {
        'options': '-vn -vf scale=320:240 -b:a 320k'
    }

    ytdl = youtube_dl.YoutubeDL(ytdl_format_options)

    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)
        self.data = data
        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url, *, loop=None):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: cls.ytdl.extract_info(url, download=True))
        if 'entries' in data:
            data = data['entries'][0]
        filename = cls.ytdl.prepare_filename(data)
        return filename, cls(discord.FFmpegPCMAudio(filename, **cls.ffmpeg_options), data=data)
