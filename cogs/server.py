import asyncio
import os
import socket

from discord.ext import commands
from dotenv import load_dotenv
from mcstatus import MinecraftServer

from util.aternos import get_status, get_server_info, stop_server
from util.aternos import start_server

load_dotenv('.env')

Default_Server = os.getenv('DEFAULT_MC_SERVER')


class Server(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	# Gets info about a minecraft
	@commands.command(aliases=['status', 'server'])
	async def info(self, ctx, override_server=''):
		async with ctx.typing():
			# restart
			# hard restart
			# stop

			if override_server == '':
				server = MinecraftServer.lookup(Default_Server)
				ping = server.ping()
				host, status, players, software, version, tps, ram = get_server_info()

				if status == 'Offline':
					await ctx.send(
						f'The server {host} is {str(status).lower()}, it is a {software} server running minecraft '
						f'{version}, it has {ping}ms ping')
				else:
					await ctx.send(
						f'The server {host} is {str(status).lower()}, it is a {software} server running minecraft '
						f'{version}, it has {ping}ms ping, {tps} tps, {ram}MB of ram and {players} players online')
			else:
				server = MinecraftServer.lookup(override_server)
				try:
					max_players = server.status().players.max
				except socket.timeout:
					await ctx.send('That doesn\'t appear to be a minecraft server (it returned an invalid response)')
					return

				players = server.status().players.online
				version = server.status().version.name
				host = server.host

				try:
					ping = server.ping()
				except IOError:
					if server.status().version.protocol.real == 46:
						await ctx.send(f'The server {host} is offline, (unknown ping)')
					else:
						await ctx.send(
							f'The server {host} is online, it is running minecraft \'{version}\', it has '
							f'{players}/{max_players} online players (unknown ping)')
					return

				if server.status().version.protocol.real == 46:
					await ctx.send(f'The server {host} is offline, it has {ping}ms ping')
				else:
					await ctx.send(
						f'The server {host} is online, it is running minecraft \'{version}\', it has {ping}ms ping and '
						f'{players}/{max_players} players online')

	@commands.command(aliases=['start'])
	async def launch(self, ctx):
		""" Launches the Minecraft Server"""
		server_status = get_status()

		if server_status == "Offline":
			await ctx.send("Starting the server...")
			await start_server()

			# If pinging a person, server will ping them when launching else ping the the user who sent the command on launch
			if len(ctx.message.mentions) == 0:
				author = ctx.author
			else:
				author = ctx.message.mentions[0]

			# Loops until server has started and pings person who launched
			while True:
				await asyncio.sleep(3)
				if get_status() == "Online":
					await ctx.send(f"{author.mention}, the server has started!")
					break

		elif server_status == "Online":
			await ctx.send("The server is already Online.")

		elif server_status == "Starting ..." or server_status == "Loading ...":
			await ctx.send("The server is already starting...")

		elif server_status == "Stopping ..." or server_status == "Saving ...":
			await ctx.send("The server is stopping. Please wait.")

		else:
			text = "An error occurred. Either the status server is not responding or you didn't set the server name " \
				   "correctly.\n\nTrying to launch the server anyways."
			await ctx.send(text)
			await start_server()

	@commands.command(aliases=['terminate'])
	async def stop(self, ctx):
		server_status = get_status()

		if server_status != 'Stopping ...' and server_status != 'Saving ...' and server_status != 'Offline' and \
				server_status != 'Loading ...':
			await ctx.send("Stopping the server...")
			await stop_server()

		elif server_status == 'Loading ...':
			await ctx.send(f"The server is currently loading. Please try again later.")

		else:
			await ctx.send("The server is already Offline.")
