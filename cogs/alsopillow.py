import discord
from discord.ext import commands
from cogs.utils import checks
from cogs.utils.dataIO import dataIO
import asyncio
from PIL import Image, ImageFont, ImageDraw
import requests
from io import BytesIO


class AlsoPillow:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def heck(self, ctx, user: discord.User):
        user1 = user
        user2 = ctx.message.author
        background = Image.open('appleheck.png')
        background = background.convert('RGBA')
        avatarfile = requests.get(user1.avatar_url)
        avatar = Image.open(BytesIO(avatarfile.content))
        avatar = avatar.convert('RGBA')
        avatar = avatar.resize((120, 120), Image.ANTIALIAS)
        background.paste(avatar, (85, 70), avatar)
        background.paste(avatar, (70, 320), avatar)
        avatar = avatar.resize((130, 130), Image.ANTIALIAS)
        background.paste(avatar, (50, 650), avatar)
        avatar = avatar.resize((180, 180), Image.ANTIALIAS)
        background.paste(avatar, (50, 1010), avatar)
        avatar = avatar.resize((210, 210), Image.ANTIALIAS)
        background.paste(avatar, (1, 1480), avatar)
        oavatarfile = requests.get(user2.avatar_url)
        oavatar = Image.open(BytesIO(oavatarfile.content))
        oavatar = oavatar.convert('RGBA')
        oavatar = oavatar.resize((150, 150), Image.ANTIALIAS)
        background.paste(oavatar, (170, 570), oavatar)
        oavatar = oavatar.resize((200,200), Image.ANTIALIAS)
        background.paste(oavatar, (210, 960), oavatar)
        oavatar = oavatar.resize((240, 240), Image.ANTIALIAS)
        background.paste(oavatar, (170, 1440), oavatar)
        background.save('hecked.png')
        await self.bot.send_file(ctx.message.channel, 'hecked.png')

def setup(bot):
    n = AlsoPillow(bot)
    bot.add_cog(n)