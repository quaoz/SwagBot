import asyncio
import discord
import youtube_dl
from discord.ext import commands

# Shut
youtube_dl.utils.bug_reports_message = lambda: ''

# Options
ytdl_format_options = {
	'format': 'bestaudio/best',
	'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
	'restrictfilenames': True,
	'noplaylist': True,
	'nocheckcertificate': True,
	'ignoreerrors': False,
	'logtostderr': False,
	'quiet': True,
	'no_warnings': True,
	'default_search': 'auto',
	'source_address': '0.0.0.0'
}

ffmpeg_options = {"options": "-vn -loglevel quiet -hide_banner -nostats",
				  "before_options": "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 0 -nostdin"}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)


class YTDLSource(discord.PCMVolumeTransformer):
	def __init__(self, source, *, data, volume=0.5):
		super().__init__(source, volume)

		self.data = data
		self.title = data.get('title')
		self.url = data.get('url')

	@classmethod
	async def from_url(cls, url, *, loop=None, stream=False):
		loop = loop or asyncio.get_event_loop()
		data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

		if 'entries' in data:
			# Takes first item from a playlist
			data = data['entries'][0]

		filename = data['url'] if stream else ytdl.prepare_filename(data)
		return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)


# Cog for music commands and processes
class Music(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	# Join VC
	@commands.command(aliases=["summon", "connect"])
	async def join(self, ctx, *, channel: discord.VoiceChannel):

		if ctx.voice_client is not None:
			return await ctx.voice_client.move_to(channel)

		await channel.connect()

	# Plays local file
	# I gained nothing by adding this
	@commands.command()
	async def local(self, ctx, *, query):

		source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(query))
		ctx.voice_client.play(source, after=lambda e: print('Player error: %s' % e) if e else None)

		await ctx.send('Now playing: {}'.format(query))

	# Plays from url, supports most of the thing youtube_dl supports
	# Play is preferred as it doesnt pre-download
	@commands.command()
	async def yt(self, ctx, *, url):

		# set stream to false to make it actually download
		async with ctx.typing():
			player = await YTDLSource.from_url(url, loop=self.bot.loop, stream=True)
			ctx.voice_client.play(player, after=lambda e: print('Player error: %s' % e) if e else None)

		await ctx.send('Now playing: {}'.format(player.title))

	# Streams from url, same as yt but doesn't pre-download
	@commands.command()
	async def play(self, ctx, *, url):

		async with ctx.typing():
			player = await YTDLSource.from_url(url, loop=self.bot.loop, stream=True)
			ctx.voice_client.play(player, after=lambda e: print('Player error: %s' % e) if e else None)

		await ctx.send('Now playing: {}'.format(player.title))

	# Disconnects voice
	@commands.command(aliases=['shut', 'fuckoff'])
	async def leave(self, ctx):

		await ctx.voice_client.disconnect()

	# Ensures author is connected to VC
	@play.before_invoke
	@local.before_invoke
	async def ensure_voice(self, ctx):
		if ctx.voice_client is None:
			if ctx.author.voice:
				await ctx.author.voice.channel.connect()

			else:
				await ctx.send("You are not connected to a voice channel.")
				raise commands.CommandError("Author not connected to a voice channel.")

		elif ctx.voice_client.is_playing():
			ctx.voice_client.stop()
