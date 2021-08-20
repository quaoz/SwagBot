import random

import discord
from discord.ext import commands
from discord.ext.commands import Cog

from util.grid import draw_grid, has_won

client = discord.Client()


class Games(commands.Cog):
	def __init__(self, bot):
		self.pending_connect_four_game = False
		self.active_connect_four_game = False
		self.challenged_player = None
		self.challenging_player = None
		self.current_player = None
		self.grid = [[' ' for _ in range(9)] for _ in range(6)]
		self.bot = bot

	@commands.command(aliases=['c4', 'connect4', 'connectfour', 'connect-four'])
	async def connect_four(self, ctx):
		if self.active_connect_four_game:
			return await ctx.send('There is already an active game')
		else:
			self.challenging_player = ctx.author
			self.challenged_player = ctx.message.mentions[0]

			await ctx.send(
				f'{self.challenging_player.nick} challenges {self.challenged_player.nick} to a game of connect four, type '
				f'\'accept\' to accept the challenge')
			self.pending_connect_four_game = True

	@Cog.listener()
	async def on_message(self, message):
		if message.author == client.user:
			return

		if self.pending_connect_four_game:
			if message.content.lower() == 'accept' and message.author == self.challenged_player:
				self.active_connect_four_game = True
				self.pending_connect_four_game = False

				await message.channel.send(f'{message.author.nick} accepts the challenge')

				embed = draw_grid(self.grid)
				self.current_player = random.choice([self.challenging_player, self.challenged_player])

				await message.channel.send(f'{self.current_player} goes first, pick the column you want to play in')
				await message.channel.send(embed=embed)

		if self.active_connect_four_game:
			if message.author == self.current_player and message.content.isnumeric():
				col = int(message.content) - 1
				if 0 <= col <= len(self.grid[0]) - 1:
					for i in range(5, 0, -1):
						if self.grid[i][col] == ' ':
							if self.current_player == self.challenged_player:
								token = 'X'
								self.current_player = self.challenging_player
							else:
								self.current_player = self.challenged_player
								token = 'O'

							self.grid[i][col] = token
							print(self.grid)
							embed = draw_grid(self.grid)
							await message.channel.send(embed=embed)

							if has_won(self.grid, token):
								await message.channel.send(f'{self.current_player.nick} loses')
								self.current_player = None
								self.challenging_player = None
								self.challenged_player = None
								self.active_connect_four_game = False
								self.grid = [[' ' for _ in range(9)] for _ in range(6)]
							return
					return await message.channel.send('Invalid column, pick again')
