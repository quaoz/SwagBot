# This Python file uses the following encoding: utf-8

# Imports
import os

from discord.ext import commands, tasks
from dotenv import load_dotenv
from selenium.common.exceptions import ElementNotInteractableException

from cogs.music import Music
from cogs.server import Server
from cogs.words import Words
from util.aternos import adblock
from util.aternos import connect_account, adblock_bypass, refresh_browser

load_dotenv('../../My Discord Bot/.env')

Discord_Token = os.getenv('BOT_KEY')


@tasks.loop(seconds=5.0)
async def adblock_wall():
	try:
		adblock_bypass()
	except ElementNotInteractableException:
		pass


@tasks.loop(hours=1.0)
async def reset_browser():
	refresh_browser()
	if adblock:
		adblock_bypass()


if __name__ == '__main__':
	# Initialises bot, with prefix
	bot = commands.Bot(command_prefix=commands.when_mentioned_or("\\"), description='jesus')

	# Logs connection
	@bot.event
	async def on_ready():
		print('Logged in as {0} ({0.id})'.format(bot.user))
		print('------')

		print('Logging into Aternos')
		connect_account()

		if adblock:
			adblock_wall.start()

		reset_browser.start()


	# Runs bot
	bot.add_cog(Music(bot))
	bot.add_cog(Words(bot))
	bot.add_cog(Server(bot))
	bot.run(Discord_Token)
