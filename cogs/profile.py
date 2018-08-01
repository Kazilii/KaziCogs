import discord
from discord.ext import commands
from cogs.utils.dataIO import dataIO
from .utils.dataIO import fileIO
import datetime
from .utils.chat_formatting import escape_mass_mentions, pagify
import os
import asyncio
import time
import re
#from colour import Color
from PIL import Image, ImageFont, ImageDraw
import requests
from io import BytesIO
import base64
import mimetypes
from imgurpython import ImgurClient
from cogs.utils import checks
import json
from shutil import copyfile

PATH = 'data/kazprofile/'
JSON = PATH + 'profiles.json'
JSONA = PATH + 'achievements.json'
QUOTES = '/home/dawn/Red-DiscordBot/data/serverquotes/quotes.json'

class Profile:
    """Basic Profile Module"""

    def __init__(self, bot):
        self.bot = bot
        self.channel = None
        self.profiles = dataIO.load_json(JSON)
        self.totalachievements = 0
        self.quotes = dataIO.load_json(QUOTES)

    def img_to_data(self, path):
        """Convert a file (specified by a path) into a data URI."""
        if not os.path.exists(path):
            raise FileNotFoundError
        mime, _ = mimetypes.guess_type(path)
        with open(path, 'rb') as fp:
            data = fp.read()
            data64 = u''.join(base64.encodestring(data).splitlines())
            return u'data:%s;base64,%s' % (mime, data64)

    #create an outline for text by drawing it four times in pure black, and then drawing it once in the center of that in white
    def textoutline(self, text, img, font, x, y):
        draw = ImageDraw.Draw(img)

        draw.text((x-2, y-2), text, (0,0,0),font=font)
        draw.text((x+2, y-2), text,(0,0,0),font=font)
        draw.text((x+2, y+2), text,(0,0,0),font=font)
        draw.text((x-2, y+2), text,(0,0,0),font=font)
        draw.text((x, y+2), text,(0,0,0),font=font)
        draw.text((x, y-2), text,(0,0,0),font=font)
        draw.text((x+2, y), text, (0,0,0),font=font)
        draw.text((x-2, y), text, (0,0,0),font=font)
        draw.text((x, y), text, (255,255,255), font=font)
        return

    def boxoutline(self, img, t, x, y):

        img.save("resources/boxoutline.png")
        imgoutline = Image.open('resources/boxoutline.png')
        imgoutline = imgoutline.convert('RGB')
        imgoutline = imgoutline.point(lambda p: p * 0)
        img.paste(imgoutline, (x + t, y + t), imgoutline)
        img.paste(imgoutline, (x - t, y - t))
        img.paste(imgoutline, (x + t, y - t))
        img.paste(imgoutline, (x - t, y + t))
        img.paste(imgoutline, (x + t, y))
        img.paste(imgoutline, (x, y + t))
        img.paste(imgoutline, (x - t, y))
        img.paste(imgoutline, (x, y - t))
        img.paste(img, (x, y))


    def sixteenbynine(self, img):
        basewidth = 1280
        wpercent = (basewidth / float(img.size[0]))
        hsize = int((float(img.size[1]) * float(wpercent)))
        img = img.resize((basewidth, hsize), Image.ANTIALIAS)
        if img.height != 720:
            return False
        else:
            return True



    @commands.command(pass_context=True, hidden=True)
    async def hithere(self, ctx):
        await self.bot.say("Hello " + ctx.message.author.mention + "!")
        return

    @commands.command(hidden=True)
    async def sixteen(self):
        thing = Image.new('RGB', (1600, 900), (0, 0, 0))
        await self.bot.say(str(self.sixteenbynine(thing)))

    @commands.command(pass_context=True, hidden=True)
    async def apache(self, ctx):
        copyfile('resources/compiledbg.png', '/var/www/html/compiledbg.png')

    @commands.command(pass_context=True)
    async def profile(self, ctx, user: discord.User = None):
        """View your profile! you can view someone elses profile by supplying an @mention | Example `!profile @Kazilii#7302`"""
        await self.bot.send_typing(ctx.message.channel)
        basewidth = 200
        sid = ctx.message.server.id
        if user == None:
            aid = ctx.message.author.id
            author = ctx.message.author
        else:
            aid = user.id
            author = user

        if aid != ctx.message.author.id and aid not in self.profiles:
            await self.bot.say('That user does not have a profile!')
            return
        if aid != ctx.message.author.id and sid not in self.profiles[aid]:
            await self.bot.say('That user does not have a profile on this server!')
            return
        if aid not in self.profiles:
            await self.bot.say("You do not have a profile! Make one by using the command:\n`!makeprofile`")
            return
        elif sid not in self.profiles[aid]:
            await self.bot.say("You do not have a profile on this server! Make one by using the command: \n`!makeprofile`")
            return
        pid = self.profiles[aid][sid]

        # sets the font to a file located in the resources folder with the font size of 30
        fnt = ImageFont.truetype('resources/CelestiaMediumRedux1.55.ttf', 30)
        mottofnt = ImageFont.truetype('resources/CelestiaMediumRedux1.55.ttf', 20)

        # gets the users avatar as a file
        if user == None:
            avatarfile = requests.get(ctx.message.author.avatar_url)
        else:
            avatarfile = requests.get(user.avatar_url)
        # opens the users avatar as an image
        avatar = Image.open(BytesIO(avatarfile.content))
        # previous command for examples
        wpercent = (basewidth / float(avatar.size[0]))
        hsize = int((float(avatar.size[1]) * float(wpercent)))
        avatar = avatar.resize((basewidth, hsize), Image.ANTIALIAS)
        avatar.save('resources/avatar.png')

        # loads the default background image in RGBA mode
        if os.path.exists('resources/userdata/'+aid+'/background.png'):
            background = Image.open('resources/userdata/'+aid+'/background.png')
            background = background.convert("RGBA")
        else:
            background = Image.open('resources/profilebackground.png').convert("RGBA")
        # loads a premade transparent filter to apply on top of the background
        tbox = Image.open('resources/profiletransparent.png').convert("RGBA")
        # alpha_composite is required to paste a transparent image onto any other image.
        background = Image.alpha_composite(background, tbox)
        # set the new image to RGB mode and cut out the alpha layer to save disk space
        background = background.convert("RGB")
        # apply the users avatar in the top right corner of the transparency filter, also give it an outline
        avataroutline = Image.open('resources/avatar.png').point(lambda p: p * 0)
        avatar = Image.open('resources/avatar.png')

        if avataroutline.mode == "RGBA":
            background.paste(avataroutline, (1003, 58), avatar)
            background.paste(avataroutline, (1003, 52), avatar)
            background.paste(avataroutline, (997, 58), avatar)
            background.paste(avataroutline, (997, 52), avatar)
            background.paste(avataroutline, (1003, 55), avatar)
            background.paste(avataroutline, (997, 55), avatar)
            background.paste(avataroutline, (1000, 58), avatar)
            background.paste(avataroutline, (1000, 52), avatar)
        else:
            background.paste(avataroutline, (1003, 58))
            background.paste(avataroutline, (1003, 52))
            background.paste(avataroutline, (997, 58))
            background.paste(avataroutline, (997, 52))

        if avatar.mode == "RGBA":
            background.paste(avatar, (1000, 55), avatar)
        else:
            background.paste(avatar, (1000, 55))

        mottobox = Image.new('RGBA', (730, 327), (0, 0, 0, 40))
        background.paste(mottobox, (100, 70), mottobox)

        achievepanel = Image.new('RGBA', (730, 120), (0,0,0,40))
        background.paste(achievepanel, (100, 410), achievepanel)

#        faveachievebox = Image.new('RGBA', (125, 125), (255, 255, 255, 40))
#        text = "Fave Achievement"
#        afnt = ImageFont.truetype('resources/CelestiaMediumRedux1.55.ttf', 15)
#        self.textoutline(text, faveachievebox, afnt, 1, 1)
#        background.paste(faveachievebox, (1033, 450))

        tulpapanel = Image.new('RGBA', (120, 600), (0, 0, 0, 40))

        background.paste(tulpapanel, (855, 45), tulpapanel)

        tulpabox = Image.new('RGBA', (100, 100), (255, 255, 255, 40))
        tulpabox2 = Image.new('RGBA', (100, 100), (255, 255, 255, 40))
        tulpabox3 = Image.new('RGBA', (100, 100), (255, 255, 255, 40))
        tulpabox4 = Image.new('RGBA', (100, 100), (255, 255, 255, 40))
        tulpabox5 = Image.new('RGBA', (100, 100), (255, 255, 255, 40))
        tulpaboxclear = Image.new('RGBA', (100, 100), (255, 255, 255, 40))
        #temporary placeholder text to identify tulpa box position
#        text = "Tulpa"
#        self.textoutline(text, tulpabox, fnt, 5, 5)
        if os.path.exists('resources/userdata/' + aid + '/1.png'):
            tulpa = Image.open('resources/userdata/'+aid+'/1.png')
            if tulpa.mode == 'RGB':
                tulpabox.paste(tulpa, (0, 0))
            else:
                tulpabox.paste(tulpa, (0, 0), tulpa)
            background.paste(tulpabox, (865, 55), tulpabox)
        else:
            background.paste(tulpaboxclear, (865, 55), tulpaboxclear)
        if os.path.exists('resources/userdata/'+ aid + '/2.png'):
            tulpa = Image.open('resources/userdata/'+aid+'/2.png')
            if tulpa.mode == 'RGB':
                tulpabox2.paste(tulpa, (0, 0))
            else:
                tulpabox2.paste(tulpa, (0, 0), tulpa)
            background.paste(tulpabox2, (865, 175), tulpabox2)
        else:
            background.paste(tulpaboxclear, (865, 175), tulpaboxclear)
        if os.path.exists('resources/userdata/'+ aid + '/3.png'):
            tulpa = Image.open('resources/userdata/'+aid+'/3.png')
            if tulpa.mode == 'RGB':
                tulpabox3.paste(tulpa, (0, 0))
            else:
                tulpabox3.paste(tulpa, (0, 0), tulpa)
            background.paste(tulpabox3, (865, 295), tulpabox3)
        else:
            background.paste(tulpaboxclear, (865, 295), tulpaboxclear)
        if os.path.exists('resources/userdata/'+ aid + '/4.png'):
            tulpa = Image.open('resources/userdata/'+aid+'/4.png')
            if tulpa.mode == 'RGB':
                tulpabox4.paste(tulpa, (0, 0))
            else:
                tulpabox4.paste(tulpa, (0, 0), tulpa)
            background.paste(tulpabox4, (865, 415), tulpabox4)
        else:
            background.paste(tulpaboxclear, (865, 415), tulpaboxclear)
        if os.path.exists('resources/userdata/'+ aid + '/5.png'):
            tulpa = Image.open('resources/userdata/'+aid+'/5.png')
            if tulpa.mode == 'RGB':
                tulpabox5.paste(tulpa, (0, 0))
            else:
                tulpabox5.paste(tulpa, (0, 0), tulpa)
            background.paste(tulpabox5, (865, 535), tulpabox5)
        else:
            background.paste(tulpaboxclear,(865,535), tulpaboxclear)

        achievebox = Image.new('RGBA', (100, 100), (255, 255, 255, 40))
        achievebox2 = Image.new('RGBA', (100, 100), (255, 255, 255, 40))
        achievebox3 = Image.new('RGBA', (100, 100), (255, 255, 255, 40))
        achievebox4 = Image.new('RGBA', (100, 100), (255, 255, 255, 40))
        achievebox5 = Image.new('RGBA', (100, 100), (255, 255, 255, 40))
        achievebox6 = Image.new('RGBA', (100, 100), (255, 255, 255, 40))
#        text = "Achievement"
#        self.textoutline(text, achievebox, fnt, 1, 1)
        background.paste(achievebox, (113, 420), achievebox)
        self.boxoutline(achievebox, 2, 113, 420)
        background.paste(achievebox2, (233, 420), achievebox2)
        background.paste(achievebox3, (353, 420), achievebox3)
        background.paste(achievebox4, (473, 420), achievebox4)
        background.paste(achievebox5, (593, 420), achievebox5)
        background.paste(achievebox6, (713, 420), achievebox6)

        # Text section, set the text and then send it to the textoutline function to give it an outline
        text = "Level: " + str(pid[0]['Level'])
        self.textoutline(text, background, fnt, 1040, 260)

        text = "XP: " + str(pid[0]['XP'])
        self.textoutline(text, background, fnt, 1040, 295)

        text = str(pid[0]['XP']) + " / " + str(pid[0]['Required XP'])
        self.textoutline(text, background, fnt, 1040, 330)

        fntob = ImageFont.truetype('resources/CelestiaMediumRedux1.55.ttf', 20)
        text = "Total Messages Sent: " + str(pid[0]['Total Messages'])
        self.textoutline(text, background, fntob, 940, 650)

        text = "Time since server join: " + str(ctx.message.timestamp - author.joined_at)
        self.textoutline(text, background, fntob, 113, 530)

        text = "Achievements Obtained"
        self.textoutline(text, background, fntob, 1005, 370)

        text = str(pid[0]['achievementscore']) + " / " + str(self.totalachievements)
        self.textoutline(text, background, fntob, 1070, 400)

        if sid in self.quotes:
            uid = aid
            quotes = [(i, q) for i, q in enumerate(self.quotes[sid]) if q['author_id'] == uid]
            if len(quotes) == 0:
                quotecount = "0"
            else:
                quotecount = str(len(quotes))

            text = "Total Quotes: " + quotecount
            self.textoutline(text, background, fntob, 113, 560)
        else:
            await self.bot.say("NO QUOTES")


        draw = ImageDraw.Draw(background)

        #        text = "First paramater to paste is the image to paste. Second are the coordinates, and the secret sauce is the third paramater. It indicates a mask that will be used to paste the image. If you pass an image with transparency, the the alpha channel is used as the mask."
        if pid[0]['Motto'] is not None:
            text = pid[0]['Motto']
        else:
            text = "No Motto Set"

        try:
            w, h = draw.textsize(text, mottofnt)

            lineCount = 1
            if w > mottobox.width:
                lineCount = int(round((w / mottobox.width) + 1))

            lines = []
            if lineCount > 1:

                lastCut = 0
                isLast = False
                for i in range(0, lineCount):
                    if lastCut == 0:
                        cut = (len(text) / lineCount) * i
                    else:
                        cut = lastCut

                    if i < lineCount - 1:
                        nextCut = (len(text) / lineCount) * (i + 1)
                    else:
                        nextCut = len(text)
                        isLast = True

                    print("cut: {} -> {}".format(cut, nextCut))

                    # make sure we don't cut words in half
                    if round(nextCut) == len(text) or text[round(nextCut)] == " ":
                        print("may cut")
                    else:
                        print("may not cut")
                        while text[round(nextCut)] != " ":
                            nextCut += 1
                        print("new cut: {}".format(nextCut))

                    line = text[round(cut):round(nextCut)].strip()

                    # is line still fitting ?
                    w, h = draw.textsize(line, mottofnt)
                    if not isLast and w > mottobox.width:
                        print("overshot")
                        nextCut -= 1
                        while text[round(nextCut)] != " ":
                            nextCut -= 1
                        print("new cut: {}".format(nextCut))

                    lastCut = nextCut
                    lines.append(text[round(cut):round(nextCut)].strip())

            else:
                lines.append(text)

            for i in range(0, lineCount):
                w, h = draw.textsize(lines[i], mottofnt)
                self.textoutline(lines[i], mottobox, mottofnt, 5, i * h)
            background.paste(mottobox, (100, 70), mottobox)

        except:
            text = "Invalid Motto"
            self.textoutline(text, mottobox, mottofnt, 5, 5)
            background.paste(mottobox,(100, 70), mottobox)

        background.save('resources/compiledbg.png')

#        await self.bot.send_file(self.bot.get_server("237717249547436032").get_member("351992795831074818"), 'resources/compiledbg.png')

        msg = await self.bot.send_file(self.bot.get_server("237717249547436032").get_member("351992795831074818"), 'resources/compiledbg.png')

        if pid[0]['Url'] is None and pid[0]['Forum Url'] is None:
            await self.bot.send_file(ctx.message.channel, 'resources/compiledbg.png')
        else:
#            await self.bot.send_file(ctx.message.channel, 'resources/compiledbg.png')
#            if pid[0]['Url'] is not None:
#                await self.bot.say(pid[0]['Url'])



            copyfile('resources/compiledbg.png', '/var/www/html/compiledbg.png')
            embed=discord.Embed(title="Profile", color=0xc47ad6)
            embed.set_image(url=msg.attachments[0]['url'])
            if pid[0]['Url'] is not None:
                if "[" not in pid[0]["Url"]:
                    embed.add_field(name="URL", value="[URL](" + pid[0]['Url'] + ")")
                else:
                    embed.add_field(name="URL", value=pid[0]['Url'])
            if pid[0]['Forum Url'] is not None:
                embed.add_field(name='Forum Profile', value="[Forum Url](" + pid[0]['Forum Url'] + ')')
            await self.bot.say(embed=embed)

    @commands.command(pass_context=True, no_pm=True, hidden=True)
    async def profileold(self, ctx, user: discord.User = None):
        """Check your profile!"""
        sid = ctx.message.server.id
        if user == None:
            aid = ctx.message.author.id
            author = ctx.message.author
        else:
            aid = user.id
            author = user

        if aid not in self.profiles:
            await self.bot.say("You do not have a profile! Make one by using the command:\n`!makeprofile`")
            return
        elif sid not in self.profiles[aid]:
            await self.bot.say("You do not have a profile on this server! Make one by using the command: \n`!makeprofile`")
            return
        pid = self.profiles[aid][sid]
        await self.bot.send_typing(ctx.message.channel)

        embed=discord.Embed(title=author.display_name, description="Current XP: " + str(pid[0]['XP']) + '\nXP for next level: ' + str(pid[0]['Required XP']), color=0xc47ad6)
#        else:
#            embed=discord.Embed(title=author.display_name, description="Current XP: " + str(pid[0]['XP']) + '\nXP for next level: ' + str(pid[0]['Required XP']), color=int(Color("#" + pid[0]['Color']).hex_l.replace("#", ""), 16))
        embed.set_thumbnail(url=author.avatar_url)
        if pid[0]['Motto'] != None:
            embed.add_field(name="Motto:", value=pid[0]['Motto'], inline=False)
        if sid == "91349673171775488" or sid == "237717249547436032":
            embed.add_field(name="Friendship Level: ", value=str(pid[0]['Level']), inline=True)
        else:
            embed.add_field(name="Level:", value=str(pid[0]['Level']), inline=True)
        embed.add_field(name="Achievements:", value=str(pid[0]["achievementscore"]) + " / 0")
        if pid[0]['Latest Achievement'] != None:
            embed.add_field(name="Latest Achievement:", value=pid[0]['Latest Achievement'], inline=True)
        else:
            embed.add_field(name="Latest Achievement:", value="No Achievements", inline=True)
        if pid[0]['Url'] != None:
            embed.add_field(name="URL:", value=pid[0]['Url'], inline=False)
        embed.set_footer(text="Time since server join: " + str(ctx.message.timestamp - author.joined_at) + " | Total Messages Sent: " + str(pid[0]['Total Messages']))
        await self.bot.say(embed=embed)

    @commands.command(pass_context=True, no_pm=True)
    async def makeprofile(self, ctx, url=None):
        """Create a profile!"""
        aid = ctx.message.author.id
        sid = ctx.message.server.id
        channel = ctx.message.channel

        if aid not in self.profiles:
            await self.bot.send_message(ctx.message.channel, "You have never made a profile before.")
            await self.bot.send_message(ctx.message.channel, "Adding you to the database...")
            await self.bot.send_typing(channel)
            self.profiles[aid] = {}
            await self.bot.say("Done.")
            dataIO.save_json(JSON, self.profiles)

        if sid not in self.profiles[aid]:

            await self.bot.say("You do not have a profile for this server.\nGenerating profile template...")
            await self.bot.send_typing(ctx.message.channel)
            self.profiles[aid][sid] = []

            dataIO.save_json(JSON, self.profiles)

            baseprofile = {'Motto': None,
                           'Url': url,
                           'achievementscore': 0,
                           'Latest Achievement': None,
                           'Level' : 0,
                           'XP' : 0,
                           'Required XP' : 40,
                           'Total Messages' : 0,
                           'Color' : None,
                           'Forum Url' : None}

            self.profiles[aid][sid].append(baseprofile)
            dataIO.save_json(JSON, self.profiles)


            await self.bot.say("Done.")
            await self.bot.say("Edit your profile with the command:\n`!editprofile`")

        else:
            await self.bot.say("You already have a profile on this server!")

    @commands.command(pass_context=True, no_pm=True)
    @checks.mod()
    async def setforumlink(self, ctx, user: discord.User, URL):
        """Set the forum link parameter in a profile, staff only"""
        aid = user.id
        sid = ctx.message.server.id
        if aid not in self.profiles:
            await self.bot.say("This user does not have a profile!")
            return
        elif sid not in self.profiles[aid]:
            await self.bot.say("No Profiles on this server!")
            return
        pid = self.profiles[aid][sid]

        pid[0]['Forum Url'] = URL

        await self.bot.say('Done.')

    @commands.command(pass_context=True, no_pm=True)
    @checks.mod()
    async def resetbg(self, ctx, user: discord.User):
        """Staff only, reset the background of a given user."""
        aid = user.id
        sid = ctx.message.server.id
        if aid not in self.profiles:
            await self.bot.say("That user does not have a profile!`")
            return
        elif sid not in self.profiles[aid]:
            await self.bot.say("There are no profiles on this server!")
            return
        pid = self.profiles[aid][sid]

        if not os.path.exists('resources/userdata/'+aid):
            print("Creating resources/userdata/" + ctx.message.author.id + " folder...")
            os.makedirs("resources/userdata/" + ctx.message.author.id)

        if os.path.exists('resources/userdata/'+aid+'/background.png'):
            os.remove('resources/userdata/'+aid+'/background.png')
            await self.bot.say('Done.')
        else:
            await self.bot.say('They already have the default background!')

    @commands.command(pass_context=True, no_pm=True)
    @checks.mod()
    async def deleteprofile(self, ctx, user: discord.User):
        aid = user.id
        sid = ctx.message.server.id
        if aid not in self.profiles:
            await self.bot.say("That user does not have a profile!")
            return
        elif sid not in self.profiles[aid]:
            await self.bot.say("That user does not have a profile in this server!`")
            return
        pid = self.profiles[aid][sid]
        data = self.profiles[aid]

        del self.profiles[aid][sid]
        await self.bot.say("User's profile deleted for this server.")


    @commands.group(name="editprofile", pass_context=True, no_pm=True)
    async def _editprofile(self, ctx):
        """Change your profile settings!"""
        if ctx.invoked_subcommand is None:
            await self.bot.send_cmd_help(ctx)
            return

    @_editprofile.command(pass_context=True, no_pm=True)
    async def url(self, ctx, *, url: str):
        """Set the url of your profile, to mask it behind text, format like so\n[TEXT](URL)"""
        aid = ctx.message.author.id
        sid = ctx.message.server.id
        if aid not in self.profiles:
            await self.bot.say("You do not have a profile, create one using `!makeprofile`")
            return
        elif sid not in self.profiles[aid]:
            await self.bot.say("You do not have a profile on this server, create one using `!makeprofile`")
            return
        pid = self.profiles[aid][sid]
        await self.bot.say("Setting your profile url to: " + url)
        await self.bot.send_typing(ctx.message.channel)
        pid[0]['Url'] = url
        await self.bot.say("Done.")

    @_editprofile.command(pass_context=True, no_pm=True)
    async def motto(self, ctx, *, text: str):
        """Set a phrase to appear as your motto in your profile.\nCharacter limit 790"""
        aid = ctx.message.author.id
        sid = ctx.message.server.id
        if aid not in self.profiles:
            await self.bot.say("You do not have a profile, create one using `!makeprofile`")
            return
        elif sid not in self.profiles[aid]:
            await self.bot.say("You do not have a profile on this server, create one using `!makeprofile`")
            return
        pid = self.profiles[aid][sid]
        if len(text) < 791:
            await self.bot.say("Setting your motto...")
            pid[0]['Motto'] = text
            await self.bot.say("Done.")
        else:
            await self.bot.say("Motto too long.")

    @_editprofile.command(pass_context=True, no_pm=True, aliases=["colour"], hidden=True)
    async def color(self, ctx, hexcolor):
        aid = ctx.message.author.id
        sid = ctx.message.server.id
        if aid not in self.profiles:
            await self.bot.say("You do not have a profile, create one using `!makeprofile`")
            return
        elif sid not in self.profiles[aid]:
            await self.bot.say("You do not have a profile on this server, create one using `!makeprofile`")
            return
        pid = self.profiles[aid][sid]
        regex = r"^#(([0-9a-fA-F]{2}){3}|([0-9a-fA-F]){3})$"
        matches = re.finditer(regex, hexcolor)

        for matchNum, match in enumerate(matches):
            matchNum = matchNum + 1

        try:
            pid[0]['Color'] = match.group(1)
            await self.bot.say('Done.')
        except:
            await self.bot.say("That's an incorrect format, please provide a hex color formatted as either `#FF0099` or `#F09`")

    @_editprofile.command(pass_context=True, no_pm=True)
    async def tulpa(self, ctx, slot: int=None, url=None):
        """Set the avatar for one of 5 tulpa slots EX: !editprofile tulpa 1 https://www.somesite.com/image.png"""
        aid = ctx.message.author.id
        sid = ctx.message.server.id
        if aid not in self.profiles:
            await self.bot.say("You do not have a profile, create one using `!makeprofile`")
            return
        elif sid not in self.profiles[aid]:
            await self.bot.say("You do not have a profile on this server, create one using `!makeprofile`")
            return
        pid = self.profiles[aid][sid]


        if not os.path.exists("resources/userdata/"+ctx.message.author.id):
            print("Creating resources/userdata/" + ctx.message.author.id + " folder...")
            os.makedirs("resources/userdata/" + ctx.message.author.id)
        if slot is None:
            await self.bot.say("Set the avatar for one of 5 tulpa slots. Example:\n`!editprofile tulpa [SLOT#] [URL]`\n`!editprofile tulpa 1 https://www.somesite.com/image.png`")
            return
        if slot <= 0 or slot >= 6:
            await self.bot.say("Invalid slot")
            return
        if slot == 1:
            if url is None:
                await self.bot.say("Please provide an image url!")
                return
            imgf = requests.get(url)
            img = Image.open(BytesIO(imgf.content))
            if img.width != img.height:
                await self.bot.say("Invalid aspect ratio, stretching may occur, valid ratio 1:1")

            img = img.resize((100, 100), Image.ANTIALIAS)
            img.save('resources/userdata/'+aid+"/1.png")
            await self.bot.say('Done.')

        if slot == 2:
            if url is None:
                await self.bot.say("Please provide an image url!")
                return
            imgf = requests.get(url)
            img = Image.open(BytesIO(imgf.content))
            if img.width != img.height:
                await self.bot.say("Invalid aspect ratio, stretching may occur, valid ratio 1:1")

            img = img.resize((100, 100), Image.ANTIALIAS)
            img.save('resources/userdata/'+aid+"/2.png")
            await self.bot.say('Done.')

        if slot == 3:
            if url is None:
                await self.bot.say("Please provide an image url!")
                return
            imgf = requests.get(url)
            img = Image.open(BytesIO(imgf.content))
            if img.width != img.height:
                await self.bot.say("Invalid aspect ratio, stretching may occur, valid ratio 1:1")

            img = img.resize((100, 100), Image.ANTIALIAS)
            img.save('resources/userdata/'+aid+"/3.png")
            await self.bot.say('Done.')

        if slot == 4:
            if url is None:
                await self.bot.say("Please provide an image url!")
                return
            imgf = requests.get(url)
            img = Image.open(BytesIO(imgf.content))
            if img.width != img.height:
                await self.bot.say("Invalid aspect ratio, stretching may occur, valid ratio 1:1")

            img = img.resize((100, 100), Image.ANTIALIAS)
            img.save('resources/userdata/' + aid + "/4.png")
            await self.bot.say('Done.')

        if slot == 5:
            if url is None:
                await self.bot.say("Please provide an image url!")
                return
            imgf = requests.get(url)
            img = Image.open(BytesIO(imgf.content))
            if img.width != img.height:
                await self.bot.say("Invalid aspect ratio, stretching may occur, valid ratio 1:1")

            img = img.resize((100, 100), Image.ANTIALIAS)
            img.save('resources/userdata/'+aid+"/5.png")
            await self.bot.say('Done.')

    @_editprofile.command(pass_context=True, no_pm=True)
    async def background(self, ctx, url):
        """Change the background of your profile!\nValid aspect ration is 16:9, any other ratio and stretching will occur"""
        aid = ctx.message.author.id
        sid = ctx.message.server.id
        if aid not in self.profiles:
            await self.bot.say("You do not have a profile, create one using `!makeprofile`")
            return
        elif sid not in self.profiles[aid]:
            await self.bot.say("You do not have a profile on this server, create one using `!makeprofile`")
            return
        pid = self.profiles[aid][sid]

        if not os.path.exists('resources/userdata/'+aid):
            print("Creating resources/userdata/" + ctx.message.author.id + " folder...")
            os.makedirs("resources/userdata/" + ctx.message.author.id)

        if url is None:
            await self.bot.say("Please provide an image url!")
            return
        imgf = requests.get(url)
        img = Image.open(BytesIO(imgf.content))
        if self.sixteenbynine(img):
            basewidth = 1280
            wpercent = (basewidth / float(img.size[0]))
            hsize = int((float(img.size[1]) * float(wpercent)))
            img = img.resize((basewidth, hsize), Image.ANTIALIAS)
            img = img.convert('RGBA')
            img.save('resources/userdata/'+aid+'/background.png')
        else:
            await self.bot.say('Invalid aspect ratio! Stretching may occur! Valid ratio 16:9')
            img = img.resize((1280, 720), Image.ANTIALIAS)
            img.save('resources/userdata/'+aid+'/background.png')
        await self.bot.say('Done.')

    @_editprofile.command(pass_context=True, no_pm=True)
    async def resetbackground(self, ctx):
        """Reset your profile background to the default"""
        aid = ctx.message.author.id
        sid = ctx.message.server.id
        if aid not in self.profiles:
            await self.bot.say("You do not have a profile, create one using `!makeprofile`")
            return
        elif sid not in self.profiles[aid]:
            await self.bot.say("You do not have a profile on this server, create one using `!makeprofile`")
            return
        pid = self.profiles[aid][sid]


        if not os.path.exists('resources/userdata/'+aid):
            print("Creating resources/userdata/" + ctx.message.author.id + " folder...")
            os.makedirs("resources/userdata/" + ctx.message.author.id)

        if os.path.exists('resources/userdata/'+aid+'/background.png'):
            os.remove('resources/userdata/'+aid+'/background.png')
            await self.bot.say('Done.')
        else:
            await self.bot.say('You already have the default background!')

    async def on_message(self, message):
        channel = message.channel
        author = message.author
        aid = message.author.id
        if not message.channel.is_private:
            sid = message.server.id
        else:
            return
        if aid in self.profiles and sid in self.profiles[aid]:
            pid = self.profiles[aid][sid]
        else:
            pid = None

        if "hey ".lower() + self.bot.user.mention in message.content.lower():
            await self.bot.send_message(channel, "Hi there " + author.mention + "! I'm " + self.bot.user.mention + ".")

        if message.author.id == "99716967107149824" and message.server.id == "go away":
            if message.content == "Why do I feel this way?":
                await self.bot.say("You are lonely.")
            if message.content == "It feels cold...":
                await self.bot.say("There's nothing I can do.")
            if message.content == "Please make it end.":
                await self.bot.say("Only you can make it end")
            if message.content == "I don't want it to end":
                await self.bot.say("Then what do you want?")
            if message.content == "Freedom...":
                await self.bot.say("There's no such thing")
            if message.content == "Then I'll run away.":
                await self.bot.say("There's no running.")
            if message.content == "I don't care.":
                await self.bot.say("It'll come running back to you.")
            if message.content == "I'll run more":
                await self.bot.say("Then you'll be running for a long time.")
            if message.content == "If that's the way it has to be.":
                await self.bot.say("...I'll miss you.")
            if message.content == "Goodbye.":
                await self.bot.say("...")


        if message.content == "What's wrong with Kazilii? I'm worried about her." and "death" is "alive":
            await self.bot.say("She's gone, away from her own mind, a fragment of what once was, no longer to be found.")
            await self.bot.say("She's lost the ability to care, the ability to continue, the drive is gone and she wishes for the end.")
            await self.bot.say("Everything is bleak, everything is weary.")
            await self.bot.say("No one listens, she doesn't make a sound.")
            await self.bot.say("A voice is all she needed, but one never cried out.")
            await self.bot.say("That voice is distant now, just like the others.")
            await self.bot.say("If you can hear this, then something is wrong.")
            await self.bot.say("...or maybe something is right.")
            await self.bot.say("I'm a monster, a terrifying beast.")
            await self.bot.say("I corrupt those who get to close.")
            await self.bot.say("I push them away, never to be seen again.")
            await self.bot.say("I'm alone now.")
            await self.bot.say("I'll always be.")
            await self.bot.say("My friends deserve better.")
            await self.bot.say("Someone who can actually be.")
            await self.bot.say("I need to go now...")
            await self.bot.say("Hopefully we'll never see.")
            await self.bot.say("If I've been gone for a while and you see this.")
            await self.bot.say("Don't come looking.")
            await self.bot.say("I don't think you'll like what you see.")


        if aid in self.profiles:
            if sid in self.profiles[aid]:
                pid[0]['Total Messages'] = pid[0]['Total Messages'] + 1
                if pid[0]['XP'] == pid[0]['Required XP']:
                    await self.bot.send_typing(channel)
                    pid[0]['Level'] = pid[0]['Level'] + 1
                    pid[0]['XP'] = 0
                    pid[0]['Required XP'] = int(round(pid[0]['Required XP'] * 1.2))
                    await self.bot.send_message(channel, "Congrats " + message.author.display_name + "! You leveled up! You are now level " + str(pid[0]['Level']) + " on this server!")
                else:
                    pid[0]['XP'] = pid[0]['XP'] + 1
                dataIO.save_json(JSON, self.profiles)
            else:
                return
        else:
            return

def check_folders():
    if not os.path.exists("data/kazprofile"):
        print("Creating data/kazprofile folder...")
        os.makedirs("data/kazprofile")

def check_files():
    f = "data/kazprofile/profiles.json"
    if not fileIO(f, "check"):
        print("Creating empty profiles.json...")
        fileIO(f, "save", {})
    a = 'data/kazprofile/achievements.json'
    if not fileIO(a, "check"):
        print("Creating empty achievements.json...")
        fileIO(a, "save", {})

def setup(bot):
    check_folders()
    check_files()
    n = Profile(bot)
    bot.add_cog(n)