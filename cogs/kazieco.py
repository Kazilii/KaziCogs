import discord
from discord.ext import commands
from .utils.chat_formatting import *
from random import randint
from random import choice as randchoice
from random import choice as choice
from random import random, randrange
from cogs.utils import checks
from cogs.utils.dataIO import dataIO
import datetime
import time
import random
import asyncio

PROFILE = '/home/dawn/PYCHARMTEST/Red-DiscordBot/data/kazprofile/profiles.json'

class KaziEco:

    def __init__(self, bot):
        self.bot = bot
        self.bank = self.bot.get_cog('Economy').bank
        self.minbet=120
        self.profile = dataIO.load_json(PROFILE)

    @checks.is_owner()
    @commands.command(pass_context=True, hidden=True)
    async def createbankaccount(self, ctx, user: discord.User):
        self.bank.create_account(user=user, msg=ctx.message)

    @commands.command(pass_context=True, no_pm=True)
    async def coinflip(self, ctx, amount:int):
        """Tired of the same old slot machine gambling? Well look no further! Coinflip is here to spice things up a bit!\nCoinflip works by, as you can guess, flipping a coin! if it lands on your chosen side, you win, doubling your bet! Otherwise, you lose your bet money!"""
        aid = ctx.message.author.id
        sid = ctx.message.server.id
        pid = self.profile[aid][sid][0]
        message = ctx.message
        user = None
        if user == None:
            user = ctx.message.author
            user2 = None
        else:
            user2 = ctx.message.author

        if user2 is not None:
            await self.bot.say("This feature is in development and will be added later.")
        elif amount < self.minbet:
            await self.bot.say("You gotta step up your game! Bet at least 120 or more!")
        else:
            if self.bank.account_exists(user):
                if self.bank.can_spend(user, amount):
                    msg = await self.bot.say("Choose a side!")
                    await self.bot.add_reaction(msg, '🔵')
                    await self.bot.add_reaction(msg, '🔴')
                    side = await self.bot.wait_for_reaction(emoji=['🔵', '🔴'], user=user, message=msg)
                    if side.reaction.emoji == '🔵':
                        playerside = 1
                    elif side.reaction.emoji == '🔴':
                        playerside = 2
                    r = randrange(1, 10)
                    looped = 0
                    self.bank.withdraw_credits(user, amount)
                    coinside = await self.bot.say(str(side.reaction.emoji) + " | Starting Side")
                    await self.bot.delete_message(msg)
                    while looped < r:
                        if looped % 2 == 0:
                            result = 1
                        else:
                            result = 2
                        looped = looped + 1
                        if result == 1:
                            resultside = '🔵'
                        else:
                            resultside = '🔴'
                        await self.bot.edit_message(coinside, str(resultside) + " | Flip Number: " + str(looped))
                        await asyncio.sleep(1)
                    if int(result) == int(playerside):
                        finalresult = await self.bot.say(str(resultside) + " | Final Result")
                        await self.bot.say('You won! You got a net gain of ' + str(amount) + '!')
                        self.bank.deposit_credits(user, (amount * 2))
                        await self.bot.say("You're new balance is: " + str(self.bank.get_balance(user)))
                        await self.bot.delete_message(coinside)
                        await asyncio.sleep(3)
                        await self.bot.delete_message(finalresult)
                        try:
                            if aid in self.profile:
                                if 'flips' not in pid:
                                    pid['flips'] = 1
                                    dataIO.save_json(PROFILE, self.profile)
                                else:
                                    pid['flips'] = pid['flips'] + 1
                                    dataIO.save_json(PROFILE, self.profile)
                        except:
                            return
                    elif int(result) != int(playerside):
                        finalresult = await self.bot.say(str(resultside) + " | Final Result")
                        await self.bot.say("You lost! You're down " + str(amount) + "!")
                        await self.bot.say("You're new balance is: " + str(self.bank.get_balance(user)))
                        if self.bank.account_exists(user=self.bot.user, msg=message):
                            self.bank.deposit_credits(user=self.bot.user, amount=amount, msg=message)
                        else:
                            self.bank.create_account(user=self.bot.user, initial_balance=amount, msg=message)
                        await self.bot.delete_message(coinside)
                        await asyncio.sleep(3)
                        await self.bot.delete_message(finalresult)
                        try:
                            if aid in self.profile:
                                if 'flips' not in pid:
                                    pid['flips'] = 1
                                    dataIO.save_json(PROFILE, self.profile)
                                else:
                                    pid['flips'] = pid['flips'] + 1
                                    dataIO.save_json(PROFILE, self.profile)
                        except:
                            return
                else:
                    await self.bot.say("You don't have enough money for that flip! You only have: " + str(self.bank.get_balance(user)) + ". You can always get more money by using `^payday`")
            else:
                await self.bot.say("You don't have a bank account! Make one by using the `^bank register` command!")

    @commands.command(pass_context=True, hidden=True)
    async def timetest(self, ctx):
        await self.interest(ctx.message)

    async def interest(self, message):
        ctime = time.time()
        if ctime < time.time():
            print('test')
        await self.bot.say(time.time())
        await time.sleep(5)
        await self.bot.say(time.time())


    async def on_message(self, message):
        aid = message.author.id
        sid = message.server.id
        author = message.author
        if self.bank.account_exists(author):
            self.bank.deposit_credits(user=author, amount=1)

def setup(bot):
    n = KaziEco(bot)
    bot.add_cog(n)