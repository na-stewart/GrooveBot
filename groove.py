import discord
from discord import default_permissions
from discord.ext.commands import has_permissions

from groovebot.core.utils import config

bot = discord.Bot()


@bot.event
async def on_ready():
    print(f"{bot.user} is ready and online!")


@bot.slash_command(name="hello", description="Say hello to the bot")
@default_permissions(manage_messages=True)
async def hello(ctx):
    await ctx.respond("Hey!")


if __name__ == "__main__":
    bot.run(config["GROOVE"]["token"])
