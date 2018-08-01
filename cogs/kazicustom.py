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
import aiohttp
import asyncio
from collections import defaultdict
import threading
import random
import urllib.request



class KaziCustom:
	"""Commands by Kazilii"""

	def __init__(self, bot):
		self.bot = bot
		mayo  = False
		start_time = None
		joined = True
		joined_time = None
		nodupes = False
		self.session = aiohttp.ClientSession(loop=self.bot.loop)


	@commands.command(name='changelog', pass_context=True)
	async def changelog(self, ctx):
		await self.bot.say("")

	@commands.command(name="barrel", aliases=["Barrel"], pass_context=True)
	async def barrel(self, ctx, user : discord.Member=None):
		"""Have SweetieBot dig through Kazilii's mysterious barrel! Who knows what you could get?
Usage! ^barrel will give you (the author) an item. supply a username via @mention will give that user the item (Ex: ^barrel @Sweetie Bot
		"""
		author = ctx.message.author
		if user != None:#Use on someone else
			await self.bot.say(randchoice(["*digs through Kazilii's barrel and pulls out another barrel* Uh... right well, here you go {}! Have fun!".format(user.mention),
			"*rummages around in Kazilii's barrel and whips out a katana* Oh my, that looks sharp! Don't hurt yourself {}!".format(user.mention),
			"*searches through Kazilii's barrel and finds a kazoo* Oh! Oh! Play us a tune {}!".format(user.mention),
			"*rummages around in Kazilii's barrel and takes out a warm plate of spaghetti* Hope you're hungry {}!".format(user.mention),
			"*digs through Kazilii's barrel and finds a miniature robotic dog* Awww, how adorable! Take care of them {}!".format(user.mention),
			"*pokes around in Kazilii's barrel and finds a miniaturized avali mech* This can't possibly be dangerous, have fun {}!".format(user.mention),
			"*digs through Kazilii's barrel and pulls out {}* Here you go {}!".format(author.mention,user.mention),
			"*rummages around through Kazilii's barrel and pulls out a plush version of {}* Neato! Here you go {}!".format(author.mention,user.mention),
			"*rummages around through Kazilii's barrel and pulls out a plush version of {}* Neato! Here you go {}!".format(user.mention,author.mention),
			"*digs through Kazilii's barrel and finds a medpack* Oh sweet! here you go {}!".format(user.mention)]))
		else:#Use on self
			await self.bot.say(randchoice(["*digs through Kazilii's barrel and pulls out another barrel* Uh... right well, here you go {}! Have fun!".format(author.mention),
			"*rummages around in Kazilii's barrel and whips out a katana* Oh my, that looks sharp! Don't hurt yourself {}!".format(author.mention),
			"*searches through Kazilii's barrel and finds a kazoo* Oh! Oh! Play us a tune {}!".format(author.mention),
			"*rummages around in Kazilii's barrel and takes out a warm plate of spaghetti* Hope you're hungry {}!".format(author.mention),
			"*digs through Kazilii's barrel and finds a miniature robotic dog* Awww, how adorable! Take care of them {}!".format(author.mention),
			"*pokes around in Kazilii's barrel and finds a miniaturized avali mech* This can't possibly be dangerous, have fun {}!".format(author.mention),
			"*digs around in Kazilii's barrel and produces a plush version of {}* Ooooh! That's a cool one! Here you go {}!".format(author.mention,author.mention),
			"*digs through Kazilii's barrel and finds a medpack* Oh sweet! here you go {}!".format(author.mention)]))

	@commands.command(name="boop", pass_context=True, hidden=True)
	async def boop(self, ctx, user :discord.Member=None):
		"""Boops someone!"""
		author = ctx.message.author
		if user == self.bot.user:
			url = "https://i.imgur.com/vdNjLhM.png"
			async with self.session.get(url) as r:
				data = await r.read()
			await self.bot.edit_profile(self.bot.settings.password, avatar=data)
			await self.bot.say("*boops @Sweetie Bo-* \n...\nHey wait a second!")
		elif user != None:
			#Code for booping someone else
			await self.bot.say("*boops {}*".format(user.mention))
		else:
			#Code for booping the user
			await self.bot.say("*boops {}*".format(author.mention))

	@commands.command(name="use", pass_context=True)
	async def use(self, ctx, move, on, *, user :discord.Member=None):
		"""Have SweetieBot use a super awesome move on someone!

Example: ^use heal on @Kazilii"""
		author = ctx.message.author
		if move.lower() == "heal":
			if on != None:
				if user != None:
					await self.bot.say(randchoice(["*Channels some magic to heal {}*".format(user.mention), "*Passes a medkit to {}* Here take this!".format(user.mention), "*Puts a bandaid on {}'s knee* There you go!".format(user.mention)]))
				else:
					await self.bot.say("Please specify someone to use this move on!")
			else:
				await self.bot.say("Please specify someone to use this move on!")

		elif move.lower() == "burn":
			if on != None:
				if user != None:
					await self.bot.say(randchoice(["*Strikes a match and throws it at {}*".format(user.mention), "*Uses magic to set the air near {} on fire*".format(user.mention), "*Pulls out a flamethrower and points towards {}* Hast la vista! *starts shooting water from the flamethrower*".format(user.mention)]))
				else:
					await self.bot.say("Please specify someone to use this move on!")
			else:
				await self.bot.say("Please specify someone to use this move on!")

		elif move.lower() == "hug":
			if on != None:
				if user != None:
					await self.bot.say(randchoice(["*Pulls {} for a big warm hug*".format(user.mention),"*Grabs {} and {} for a nice group hug*".format(author.mention,user.mention),"*Hugs {}*".format(user.mention)]))
				else:
					await self.bot.say("Please specify someone to use this move on!")
			else:
				await self.bot.say("Please specify someone to use this move on!")

		elif move.lower() == "butt":
			if on != None:
				if user != None:
					await self.bot.say(randchoice(["*Uses magic to turn {} into a butt!*".format(user.mention), "*Attempts to turn {} into a butt, but the spell backfires and hits {} instead!*".format(user.mention,author.mention), "***BUTTS {}!***".format(user.mention)]))
				else:
					await self.bot.say("Please specify someone to use this move on!")
			else:
				await self.bot.say("Please specify someone to use this move on!")

		elif move.lower() == "kite" or move.lower() == "kites" or move.lower() == "kiting":
			if on != None:
				if user != None:
					await self.bot.say(randchoice(["*Assembles a kite for {}*, Come one, let's go fly a kite!".format(user.mention),"*Rummages through Kazilii's barrel and pulls out a kite,* Let's go have some fun {}!".format(user.mention)]))
				else:
					await self.bot.say("Please specify someone to use this move on!")
			else:
				await self.bot.say("Please specify someone to use this move on!")

		elif move.lower() == 'sleep' or move.lower() == 'rest':
			if on != None:
				if user != None:
					await self.bot.say(randchoice(["*Takes some sleeping powder and throws it in {}'s face*".format(user.mention),"*Casts a sleep spell on {}*".format(user.mention)]))

		else:
			await self.bot.say("I don't know that move!")

	@commands.command(pass_context=True, aliases=["movelist"])
	async def uselist(self):
		await self.bot.say("These are the moves I currently know!\n```\nheal\nburn\nhug\nbutt\nkite | kites | kiting```")

	@commands.command(hidden=True, pass_context=True)
	async def mapletest(self, ctx):
		await self.bot.add_reaction(ctx.message, "\U0001F341")
		await self.bot.say(":maple_leaf:")

#	@commands.command(hidden=True)
#	async def maplemojitest(self):
#		await self.bot.add_reaction(U0001F341)

	@commands.command(pass_context=True, no_pm=True, hidden=True)
	@checks.mod()
	async def say(self, ctx, channel: discord.Channel, *, text):
		"""Say something in the specified channel, great for pranks!"""
		await self.bot.send_message(channel, text)

	@commands.command(hidden=True)
	async def channelidtest(self, ID):
			await self.bot.say(str(self.bot.get_channel(ID)))

	async def member_join(self, member: discord.Member):

		d = {"352094748078637056":"363910077264166912","331583527244267520":"331583527244267520","237717249547436032":"237717249547436032","278934922679549952":"278934922679549952","345604953794150400":"356460005232345089","91349673171775488":"325685266109169664"}

		c = d.get(member.server.id, None)

		if c is not None:
			if c == "325685266109169664":
				print("")
				self.joined = True
				self.joined_time = time.time()
				while self.joined == True:
					if time.time() - self.joined_time > 20:
						channel = self.bot.get_channel("325685266109169664") #This is Lobby on ES
						await self.bot.send_message(channel,"Hi there {}! Welcome to Equestrian Souls! Please register an account on https://www.equestriansouls.com/ and post your profile link here, you'll then need to run the following command: `!makeprofile`, afterwords a staff member will come around to verify your account and give you access to the rest of the discord! If it's taking a while for the staff to reply, don't be afraid to ping them with `@Staff`".format(member.mention))
						self.joined_time = None
						self.joined = False

			if c == "356460005232345089":
				self.joined = True
				self.joined_time = time.time()
				while self.joined == True:
					if time.time() - self.joined_time > 20:
						channel = self.bot.get_channel("356460005232345089") #This is Lobby on HtH
						await self.bot.send_message(channel,"Hi there {}! Welcome to Help to Harmony! To become a member and be able to post, please ping a staff member with `@Staff`. You MUST be a member of Equestrian Souls. Link: https://discord.gg/79Jj4na".format(member.mention))
						self.joined_time = None
						self.joined = False

			else:

				await self.bot.send_message(discord.Object(id=c), "Welcome, {}!".format(member))


#		if member in self.bot.get_server("352094748078637056").members: # Group House Plans Server
#			self.nodupes = True

#		if member in self.bot.get_server("331583527244267520").members: # Starlights server
#			self.nodupes = True

#		if member in self.bot.get_server("237717249547436032").members: # Private Test Server
#			self.nodupes = True

#		if member in self.bot.get_server("278934922679549952").members: # Public Test Server
#			self.nodupes = True

#		if member in self.bot.get_server("345604953794150400").members: # Help to Harmony
#			self.nodupes = True

#		if member in self.bot.get_server("91349673171775488").members and self.nodupes == False: # Equestrian Souls

#		if member.server.id == "91349673171775488":
#			self.joined = True
#			self.joined_time = time.time()
#			while self.joined == True:
#				if time.time() - self.joined_time > 5:
#					channel = self.bot.get_channel("325685266109169664") #This is Lobby on ES
#					await self.bot.send_message(channel,"Hi there {}! Welcome to Equestrian Souls! Please register an account on https://www.equestriansouls.com/ and post your profile link here to gain access to the rest of the discord! If it's taking a while for the staff to reply, don't be afraid to ping them with `@Staff`".format(member.mention))
#					self.joined_time = None
#					self.joined = False
#			self.nodupes = True

#		if self.nodupes == True:
#			self.nodupes = False

	@commands.command()
	async def channeltest(self, member):
#		channel = self.bot.get_channel("278413632142966787")
		channel = self.bot.get_channel("325685266109169664")
#		await self.bot.send_message(channel, text)
		await self.member_join(member)

	@commands.command()
	async def lentest(self, *, text):
		await self.bot.say("Your message was {} long!".format(len(text)))
		if len(text) > 20:
			await self.bot.say("My! That's pretty long!")

#Techie-Request, "Is mayonaise an instrument?"

	def timestop():
		self.mayo = False

	async def on_message(self, message):
		channel = message.channel
		author = message.author
		testyes = message.content.startswith
		mayoyes = 'is mayonnaise an instrument'
		mayoyesalt = 'is mayo an instrument'
		triggerwords = ("cheese pony test",
		"musical pone",
		"musical pony",
		"im a smart pone",
		"im a smart pony",
		"i am a smart pone",
		"i am a smart pony",
		"i'm a smart pone",
		"i'm a smart pony",
		"shy pone",
		"shy pony",
		"fun pone",
		"fun pony",
		"awesome pone",
		"awesome pony",
		"reliable pone",
		"reliable pony",
		"proud pone",
		"proud pony",
		"revert back",
		"revert to normal",
		"valiant pone",
		"valiant pony",
		"brave crusader",
		"fabulous pone",
		"fabulous pony",
		"earthbound classical mare",
		"earthbound classical pony",
		"earthbound classical pone",
		"classical pone",
		"classical pony",
		"for friends i fight",
		"for friends you fight",
		"friends i fight",
		"friends you fight",
		"equestrian mail mare",
		"dare to be you, daring do",
		"my pet little pony",
		"my pet little pone",
		"its time to be my pet",
		"it's time to be my pet",
		"it is time to be my pet",
		"slave time for you",
		"slave time",
		"p0ny",
		"pzerony",
		"p[zero]ny",
		"p'zero'ny",
		"p\"zero\"ny",
		"p'0'ny",
		"p\"0\"ny")
#		emoji = U0001F341
#		t=threading.Timer(3,timestop)
#		t = Timer(5, timestop)

		if message.server is None:
			return

		if author == self.bot.user:
			return

		if not self.bot.user_allowed(message):
			return

		if message.content.casefold().startswith(mayoyes.casefold()) or message.content.casefold().startswith(mayoyesalt.casefold()):
			self.mayo = True
			self.start_time = time.time()
			await self.bot.send_message(channel, "No {}, Mayonnaise is not an instrument.".format(author.mention))

		if message.content.lower().startswith('raises') and self.mayo == True or message.content.lower().startswith('_raises') and self.mayo == True or message.content.lower().startswith('*raises') and self.mayo == True:
#			msg = await bot.wait_for_message(author=message.author, content='raises')
			if time.time() - self.start_time < 30:
				self.mayo = False
				self.start_time = None
				await self.bot.send_message(channel, "Horseradish is not an instrument either.")
			else:
				self.start_time = None

		if 'redacted' in message.content.lower():
			await self.bot.send_message(channel, '[REDACTED]')

		if 'ftg signing in' in message.content.lower():
			await self.bot.send_message(channel, 'Welcome Operative.')

		if message.content.lower().endswith(' eh?') or message.content.lower().endswith('eh!') or message.content.lower().endswith('eh!~~') or message.content.lower().endswith(' eh?~~') or 'canada'.lower() in message.content.lower() or 'canadia' in message.content.lower() or 'canadian' in message.content.lower() or 'bags of milk' in message.content.lower() or 'tim hortons' in message.content.lower():
			chance = random.randint(1,100)
			if chance < 10:
				await self.bot.add_reaction(message, ':timhortons:365313496872779776')
			else:
				await self.bot.add_reaction(message, "\U0001F341")

		if message.content.lower().endswith('why not?'):
			await self.bot.add_reaction(message, ":wynaut:364952371593478144")

		if ' ok ' in message.content.lower() or message.content.lower().endswith(' ok') or message.content.lower() == "ok":
			await self.bot.add_reaction(message, "🆗")

		if 'moo.'.lower() in message.content.lower() or 'moo ' in message.content.lower() or 'moo!' in message.content.lower() or 'moo?' in message.content.lower():
			await self.bot.add_reaction(message, '🐮')

		if 'kite'.lower() in message.content.lower() or 'kites' in message.content.lower() or 'kiting' in message.content.lower():
			if 'hate kite' in message.content.lower() or 'hate kiting' in message.content.lower():
				await self.bot.add_reaction(message, ':youremessingwithme:338371314345574410')
			else:
				await self.bot.add_reaction(message, ':slhappy:365889375927795733')

		if '***'.lower() in message.content and 'joel'.lower() in message.content.lower() or 'are you downloading boobies again' in message.content.lower():
			await self.bot.add_reaction(message, ':KermitSub:384954961588387840')

		if 'books!' in message.content.lower():
			await self.bot.add_reaction(message, ':twilightblush:264457324003852298')

		if 'sleeping accomodation' in message.content.lower() or 'sleeping accommodation' in message.content.lower():
			await self.bot.add_reaction(message, '🛌')

		if '{🐰}' in message.content and message.author.id == '182210174969184257':
			await self.bot.add_reaction(message, ':Wilbert:381919204313661441')

		if 'fluffy space raptor' in message.content.lower() or 'floofy space raptor' in message.content.lower() or 'FSR' in message.content:
			await self.bot.add_reaction(message, ':Kazilii:278464671919505409')

		if 'Twizilii' in message.content:
			await self.bot.add_reaction(message, ':twizilii:385299098263224320')

		if 'kazilii' in message.content.lower() and ' happy' in message.content.lower() and 'is' in message.content.lower():
			await self.bot.add_reaction(message, ':kaziliihappy:385303405767426048')

		if 'kazilii' in message.content.lower() and ' happy' in message.content.lower() and 'seems' in message.content.lower():
			await self.bot.add_reaction(message, ':kaziliihappy:385303405767426048')

		if 'twizilii' in message.content.lower() and ' happy' in message.content.lower() and 'is' in message.content.lower():
			await self.bot.add_reaction(message, ':kaziliihappy:385303405767426048')

		if 'twizilii' in message.content.lower() and ' happy' in message.content.lower() and 'seems' in message.content.lower():
			await self.bot.add_reaction(message, ':kaziliihappy:385303405767426048')

		if 'mango' in message.content.lower() and 'screee' in message.content.lower():
			await self.bot.add_reaction(message, ':mango:385617852583116831')

		if message.author.id == '99716967107149824' and 'I' in message.content and 'happy' in message.content.lower():
			await self.bot.add_reaction(message, ':kaziliihappy:385303405767426048')

		if message.author.id == '91352495766380544' and 'techdisk' in message.content.lower():
			await self.bot.add_reaction(message, ':techdisk:387399073973665792')

		if message.content.lower() == 'kek' or ' kek ' in message.content.lower() or message.content.lower().endswith(' kek'):
			await self.bot.add_reaction(message, ':kek:353028401579425802')

		if 'keknut' in message.content.lower():
			await self.bot.add_reaction(message, '❤')

		if 'stereo' in message.content.lower() and 'bucket' in message.content.lower():
			await self.bot.add_reaction(message, ':StereoBucket:389292074048159745')

		if 'autocorrect' in message.content.lower() or 'autocarrot' in message.content.lower():
			await self.bot.add_reaction(message, '🥕')

		if 'barrel' in message.content.lower():
			await self.bot.add_reaction(message, 'a:KaziliiBarrel:393813226636181515')

		if 'snek' in message.content.lower():
			await self.bot.add_reaction(message, ':snek:391164987789410306')

		if 'Lad' in message.content:
			await self.bot.add_reaction(message, ':lad:345761117311598603')

		if 'hate' in message.content.lower() and 'marshmallow' in message.content.lower():
			await self.bot.add_reaction(message, ':SBMessingWithMe:441869197988069378')

		if 'marshmallow' in message.content.lower() and not 'hate' in message.content.lower():
			await self.bot.add_reaction(message, ':SBHappyMarshmallow:441872688374349824')

		if 'ooM' in message.content():
			await self.bot.add_reaction(message, ':ooM:443624048015048724')

#		if 'think' in message.content:
#			await self.bot.add_reaction(message, randchoice([':kathinkYaranaikaThinking:431171437165019149', ':kathinkThonkWhite:431171032703827968', ':kathinkThonkery:431173287050084353', ':kathinkthinkxel:431175034493730836', ':kathinkThinkupsidedown:431171104191676434', ':kathinkThinkSweat:431172252793307136', ':kathinkThinkSpinner:431174774350151691', ':kathinkThinkling:431172170803052576', ':kathinkThinkingLoaf:431173600956121100', ':kathinkASTHETHINK:431173019126333455', ':kathinkAmicableThink:431174680221712385', ':kathink3DThink:431171965525557249', ':kathinkGreen_Thinking_Emoji:431171261985456129', ':kathinkgay_thinking:431173659416330260', ':kathinkfeelsthinkingman:431171636683735040', ':kathinkEggThink:431171297930641439', ':kathinkderp_thinking:431171918075396098', ':kathinkclassyblobthink:431175312647258122', ':kathinkbigeyethink:431172606008492033', ':kathinkoutagethink:431174940755099668', ':kathinknope:431170673298112523', ':kathinkmsnthink:431171848626110475', ':kathinkmariothink:431172695145578536', ':kathinkkys:431170135672487956', ':kathinkHyperThink:431172538647969793', ':kathinkThinkingGrape:431173071747940353', ':kathinkThinkingGlobal:431173540960665601', ':kathinkThinkingFast:431173698645393429', ':kathinkThinkingEarthChan:431172042725916672', ':kathinkThinkingB:431172341666676756', ':kathinkthinkhappy:431172440413044757', ':kathinkThinkfused:431174389254586368', ':kathinkthinkery:431171771513962506', ':kathinkthinker:431172376433000469', ':kathinkthinkcat:431172126901534730', ':kathinkthinkBaguette:431174853706514434', ':kathinkThink_Big:431171510796025866', 'a:kathinkspinthink:431172753375232001', 'a:kathinkspinthink:431172753375232001', ':kathinkoverthinking:431172087424483329']))

		if any(message.content.lower().find(s)>=0 for s in triggerwords):
			if channel in self.bot.get_server("91349673171775488").channels:
				await self.bot.send_message(self.bot.get_channel("362732246018555904"), "{} Said `\"{}\"` in {}.".format(author.mention,message.content,channel.mention))
				await self.bot.delete_message(message)
				await self.bot.send_message(channel, "Hey {}! You said a trigger, so I had to remove your message, sorry!".format(author.mention))

			if channel in self.bot.get_server("345604953794150400").channels:
				await self.bot.send_message(self.bot.get_channel("364869870464270337"), "{} Said `\"{}\"` in {}.".format(author.mention,message.content,channel.mention))
				await self.bot.delete_message(message)
				await self.bot.send_message(channel, "Hey {}! You said a trigger, so I had to remove your message, sorry!".format(author.mention))
		else:
			return

	@commands.command(pass_context=True)
	async def sleep(self, ctx, user : discord.Member=None):
		s = str(ctx.message.author.nick)
		n = str(ctx.message.author.name)
		if user == None:
			if ctx.message.author.nick == None:
				await self.bot.say(randchoice(["***NO {}! WHAT ARE YOU DOING!? GO TO SLEEP! GOSH!***".format(n.upper()),
				"***NO {} GO TO SLEEP JEEZ WHY ARE YOU STILL UP!?***".format(n.upper())]))
			else:
				await self.bot.say(randchoice(["***NO {}! WHAT ARE YOU DOING!? GO TO SLEEP! GOSH!***".format(s.upper()),
				"***NO {} GO TO SLEEP JEEZ WHY ARE YOU STILL UP!?***".format(s.upper())]))
		else:
			if user.nick == None:
				await self.bot.say(randchoice(["***NO {}! WHAT ARE YOU DOING!? GO TO SLEEP! GOSH!***".format(user.name.upper()),
				"***NO {} GO TO SLEEP JEEZ WHY ARE YOU STILL UP!?***".format(user.name.upper())]))
			else:
				await self.bot.say(randchoice(["***NO {}! WHAT ARE YOU DOING!? GO TO SLEEP! GOSH!***".format(user.nick.upper()),
				"***NO {} GO TO SLEEP JEEZ WHY ARE YOU STILL UP!?***".format(user.nick.upper())]))

	@commands.command()
	async def kazoo(self):
		await self.bot.say(randchoice(["https://www.youtube.com/watch?v=euWD-rRnxM0","https://www.youtube.com/watch?v=FWupBjVn9ZM","https://www.youtube.com/watch?v=ASaP1NAzm0o","https://www.youtube.com/watch?v=UMl7HAXVtmQ","https://www.youtube.com/watch?v=96RyuJG_Dq4","https://www.youtube.com/watch?v=ya5NdNGCh60","https://www.youtube.com/watch?v=vtnGNqWayXw","https://www.youtube.com/watch?v=EargV582PBE","https://www.youtube.com/watch?v=ycOkAzXaxM4","https://www.youtube.com/watch?v=8rUYOUe-YAg","https://www.youtube.com/watch?v=8ADQRXqZbnA","https://www.youtube.com/watch?v=Aq95HHAwh0g","https://www.youtube.com/watch?v=HFHLPj8RA8E","https://www.youtube.com/watch?v=zRNwdSJDzbA","https://www.youtube.com/watch?v=XuX1fdLk89E","https://www.youtube.com/watch?v=2B8lYWtxjOI","https://www.youtube.com/watch?v=7OBZN1rL9gc","https://www.youtube.com/watch?v=hPMh9jVJUZE","https://www.youtube.com/watch?v=v-aWMAvw6NQ","https://www.youtube.com/watch?v=qvwo-Fz4_xs","https://www.youtube.com/watch?v=ATLJ0CFnsoE","https://www.youtube.com/watch?v=PpKgHVPJ5ps","https://www.youtube.com/watch?v=K1z7TSXZerM","https://www.youtube.com/watch?v=6j7MVMg-kgs","https://www.youtube.com/watch?v=uSjktGVGF_0","https://www.youtube.com/watch?v=wW9laDfNqUY","https://www.youtube.com/watch?v=8TE2XHWvTPk","https://www.youtube.com/watch?v=N1oD9p227Fo","https://www.youtube.com/watch?v=o4jLq_rPhRQ","https://www.youtube.com/watch?v=bUs76qp1djo","https://www.youtube.com/watch?v=qj32t4JTjF8","https://www.youtube.com/watch?v=hIuSAg3wIBo","https://www.youtube.com/watch?v=BJ1dYRS4BsA","https://www.youtube.com/watch?v=4sGgWDQjuGA","https://www.youtube.com/watch?v=vp-E75UU3Rk","https://www.youtube.com/watch?v=YZPPTJzXw2s","https://www.youtube.com/watch?v=RvGc79960wQ","https://www.youtube.com/watch?v=-Sb1GtrajwQ","https://www.youtube.com/watch?v=KaK80iDPe_k","https://www.youtube.com/watch?v=wMyqQWcAuKM","https://www.youtube.com/watch?v=PiayNKpsAdQ","https://www.youtube.com/watch?v=_JSg3izBC3w","https://www.youtube.com/watch?v=rkEdB92X-14"]))

	@commands.command(pass_context=True)
	async def kazilii(self, ctx):
		await self.bot.say(ctx.message.server.get_member('99716967107149824').avatar_url)
	
	@commands.command(hidden=True)
	@checks.mod()
	async def replacetest(self, text):
		await self.bot.say(str(text).replace('cheese', '`BUYSOMEAPPLES`'))

	@commands.command(hidden=True, pass_context=True)
	async def cutepone(self, ctx):
		try:
			starlight = ctx.message.server.get_member('167798987078762497')
			await self.bot.say(starlight.avatar_url)
		except:
			await self.bot.say('Cute Pone isn\'t here!')

	@commands.command(hidden=True)
	@checks.mod()
	async def replacetestemote(self, text):
		await self.bot.say(str(text).replace('cheese', ':maple_leaf:'))

	@commands.command(hidden=True, pass_context=True)
	async def rolestester(self, ctx, user : discord.Member):
		if str(user.top_role) == 'Tek':
			await self.bot.say('{} is a Tek'.format(user.name))
		else:
			await self.bot.say('{} is not a Tek'.format(user.name))

	@commands.command(hidden=True, pass_context=True)
	async def toproledisplay(self, ctx, user : discord.Member):
		await self.bot.say(user.top_role)
		
	@commands.command(hidden=True, pass_context=True)
	async def botavatartest(self, ctx, url):
		urllib.request.urlretrieve(url, "BOTAVATARSWAP.jpg")
		with open("BOTAVATARSWAP.jpg", "rb") as imageFile:
			f = imageFile.read()
			b = bytearray(f)
		await self.bot.edit_profile(avatar=b)

def setup(bot):
	n = KaziCustom(bot)
	bot.add_listener(n.member_join, "on_member_join")
	bot.add_cog(n)
