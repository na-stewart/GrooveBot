import asyncio
from colorsys import hsv_to_rgb
from configparser import ConfigParser

from PIL import ImageDraw, ImageFont, Image

config = ConfigParser()
config.read("./groove.ini")


async def text_to_neuropol(message, color=None, file="neuropol.png"):
    if len(message) > 35:
        raise ValueError("Message cannot be over 35 characters.")
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
                tuple(round(map_range * 255) for map_range in hsv_to_rgb(map_range, 1, 1))
            )
            image_draw.text(
                (10 + spacing, 0), text=message[i], fill=rgb_values[i], font=font
            )
            spacing += font.getbbox(message[i])[2]
    else:
        ImageDraw.Draw(img).text((10, 5), message, fill=color, font=font)
    await asyncio.get_running_loop().run_in_executor(None, img.save, file)


async def response(ctx, message, success=True):
    await ctx.send(f":white_check_mark: ** {message}**" if success else f":x: **{message}**")
