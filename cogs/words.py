import os
import random
from time import sleep
import typing

import discord
from PyDictionary import PyDictionary
from discord import Embed
from discord.ext import commands
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

	@commands.command()
	async def help(self, ctx):
		embed = Embed(title='Help', description='You can view the list of available commands and their syntax [here]('
												'https://github.com/quaoz/GaymerBot#readme)')
		await ctx.send(embed=embed)

	@commands.command(aliases=['license'])
	async def source(self, ctx):
		embed = Embed(title='Source code', description='My source code is available [here]('
												'https://github.com/quaoz/GaymerBot), I\'m licensed under [LGLPv3]('
												'https://github.com/quaoz/GaymerBot/blob/main/LICENSE)')
		await ctx.send(embed=embed)

	# Gets the lyrics of a song
	@commands.command(aliases=["l", "lyric"])
	async def lyrics(self, ctx, *, title):

		async with ctx.typing():
			# Searches for the lyrics
			song = genius.search_song(title)
			lyrics = song.lyrics

			lyrics_split = lyrics.split('\n')
			lyrics_batch = ''
			counter = 1

			# Checks if the lyrics are over the discord maximum character limit
			# If they are it separates them into chunks which it sends individually
			if len(lyrics) >= 2000:
				for line in lyrics_split:
					if len(lyrics_batch) + len(line) >= 2000:
						embed = Embed(title=f'Lyrics for {song.full_title}, pt{counter}', description=lyrics_batch)
						embed.set_thumbnail(url=song.header_image_thumbnail_url)
						await ctx.send(embed=embed)
						counter += 1
						lyrics_batch = ''
					else:
						lyrics_batch += line + '\n'
				embed = Embed(title=f'Lyrics for {song.full_title}, pt{counter}', description=lyrics_batch)
				embed.set_thumbnail(url=song.header_image_thumbnail_url)
				await ctx.send(embed=embed)
			else:
				embed = Embed(title=f'Lyrics for {song.full_title}', description=lyrics)
				embed.set_thumbnail(url=song.header_image_thumbnail_url)
				await ctx.send(embed=embed)

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

			message_split = message.split('\n')
			message_batch = ''
			counter = 1

			if len(message) >= 2000:
				for line in message_split:
					if len(message_batch) + len(line) >= 2000:
						embed = Embed(title=f'Definition pt{counter}', description=message_batch)
						await ctx.send(embed=embed)
						counter += 1
						message_batch = ''
					else:
						message_batch += line + '\n'
				embed = Embed(title=f'Definition pt{counter}', description=message_batch)
				await ctx.send(embed=embed)
			else:
				embed = Embed(title=f'Definition', description=message)
				await ctx.send(embed=embed)

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

				embed = Embed(title='Translation',
							  description=f'"{translation.origin}" translated from {constants.LANGUAGES[source_language]} '
										  f'({translation.src}) to {constants.LANGUAGES[target_language]} ({translation.dest}) is '
										  f'"{translation.text}"')
				await ctx.send(embed=embed)

	# Random number generator
	@commands.command(aliases=['r', 'rand'])
	async def random(self, ctx, upper_bound, lower_bound: typing.Optional[int] = 0):
		async with ctx.typing():
			if upper_bound.isnumeric():
				if int(upper_bound) > lower_bound:
					embed = Embed(title=f'{random.randint(int(lower_bound), int(upper_bound))}',
								  description=f'Random number from {upper_bound} to {lower_bound}')
				else:
					embed = Embed(title=f'{random.randint(int(upper_bound), int(lower_bound))}',
								  description=f'Random number from {lower_bound} to {upper_bound}')
				await ctx.send(embed=embed)
