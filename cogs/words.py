import os
import random
from time import sleep
import typing

import discord
from PyDictionary import PyDictionary
from discord.ext import commands
from discord.ext.commands import Cog
from dotenv import load_dotenv
from googletrans import constants, Translator

import lyricsgenius

load_dotenv('.env')

Genius_Token = os.getenv('GENIUS_KEY')

# Lyrics time
genius = lyricsgenius.Genius(Genius_Token)

# Dictionary time
dictionary = PyDictionary()

# Translator time
translator = Translator()

# Initialises client
client = discord.Client()

# Separates the language names and codes for the translator
language_codes = list(constants.LANGUAGES.keys())
language_names = list(constants.LANGUAGES.values())


# Cog for text based commands, e.g: define or translate
class Words(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	# Gets the lyrics of a song
	@commands.command(aliases=["l", "lyric"])
	async def lyrics(self, ctx, *, title):

		async with ctx.typing():
			# Searches for the lyrics
			song = genius.search_song(title)
			lyrics = song.lyrics

			# Checks if the lyrics are over the discord maximum character limit
			# If they are it separates them into chucks which it sends individually
			if len(lyrics) >= 2000:
				for i in range(0, int(len(lyrics) / 2000)):
					lyrics_split = lyrics[i * 2000: i * 2000 + 1999]
					await ctx.send(lyrics_split)

			else:
				await ctx.send(lyrics)

	# Defines a word
	@commands.command(aliases=['def', 'd', 'meaning'])
	async def define(self, ctx, *, words):

		# Separates the words
		items = words.split()
		message = ''

		# Defines the words and formats the response
		async with ctx.typing():
			for word in items:
				definition = dictionary.meaning(word)
				message += word.capitalize() + ':\n'

				for key in definition.keys():
					message += '- ' + key + ':\n'

					for values in definition[key]:
						message += '	- ' + values.capitalize() + '\n'

					message += '\n'

			# Checks if the definition(s) are over the discord maximum character limit
			# If they are it separates them into chucks which it sends individually
			if len(message) >= 2000:
				for i in range(0, int(len(message) / 2000)):
					message_split = message[i * 2000: i * 2000 + 1999]
					await ctx.send(message_split)

			else:
				await ctx.send(message)

	# Translator
	@commands.command(aliases=['translate', 't'])
	async def trans(self, ctx, target_language, *, text=''):

		valid_language = False

		# Converts the language name to the language code
		if target_language in language_names:
			target_language = language_codes[language_names.index(target_language)]
			valid_language = True

		elif target_language in language_codes:
			valid_language = True

		# If the target language isn't specified it will try to translate to english
		if not valid_language:
			text = target_language + ' ' + text
			target_language = 'en'

		try:
			source_language = translator.detect(text)
			source_language = source_language.lang

		except Exception as e:
			print(e)
			sleep(0.5)

		else:
			# Translates the text
			translation = translator.translate(text, src=source_language, dest=target_language)

			async with ctx.typing():
				if not valid_language:
					await ctx.send('Target language not specified or unknown, translating to english.')

				await ctx.send(
					f'"{translation.origin}" translated from {constants.LANGUAGES[source_language]} ({translation.src}) '
					f'to {constants.LANGUAGES[target_language]} ({translation.dest}) is "{translation.text}"')

	# Random number generator
	@commands.command(aliases=['r', 'rand'])
	async def random(self, ctx, upper_bound, lower_bound: typing.Optional[int] = 0):
		async with ctx.typing():
			if upper_bound > lower_bound:
				await ctx.send(random.randint(int(lower_bound), int(upper_bound)))
			else:
				await ctx.send(random.randint(int(upper_bound), int(lower_bound)))

	# Non-command messages
	@Cog.listener()
	async def on_message(self, message):
		if message.author == client.user:
			return
