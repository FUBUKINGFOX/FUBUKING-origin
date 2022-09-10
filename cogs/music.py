﻿#== encoding utf-8 ==
import discord
from discord.ext import commands
import asyncio
import itertools
import sys
import traceback
from async_timeout import timeout
from functools import partial
import youtube_dl
from youtube_dl import YoutubeDL
#===============
from bin import file_loader, ctt, ctc, source
from bin.net import YouTobe_playlist_exploer
enable_special_playchannel = bool(file_loader.setting["enable_special_playchannel"])
playchannel = file_loader.playchannel
owner_id = [794890107563671553]
#===============
# Suppress noise about console usage from errors
youtube_dl.utils.bug_reports_message = lambda: ''

ytdlopts = {
    'format': 'bestaudio/best',
    'outtmpl': 'downloads/%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0'  # ipv6 addresses cause issues sometimes
}

ffmpegopts = {
    'before_options': '-nostdin',
    'options': '-vn'
}

ytdl = YoutubeDL(ytdlopts)


class VoiceConnectionError(commands.CommandError):
    """Custom Exception class for connection errors."""


class InvalidVoiceChannel(VoiceConnectionError):
    """Exception for cases of invalid Voice Channels."""


class YTDLSource(discord.PCMVolumeTransformer):

    def __init__(self, source, *, data, requester):
        super().__init__(source)
        self.requester = requester

        self.title = data.get('title')
        self.web_url = data.get('webpage_url')
        self.duration = data.get('duration')
        self.thumbnail = data.get('thumbnail')
        self.uploader = data.get('uploader')
        self.uploader_url = data.get('uploader_url')

        # YTDL info dicts (data) have other useful information you might want
        # https://github.com/rg3/youtube-dl/blob/master/README.md

    def __getitem__(self, item: str):
        """Allows us to access attributes similar to a dict.
        This is only useful when you are NOT downloading.
        """
        return self.__getattribute__(item)

    @classmethod
    async def create_source(cls, ctx, search: str, *, loop, download=False, creat_Queued_message: bool):
        loop = loop or asyncio.get_event_loop()

        to_run = partial(ytdl.extract_info, url=search, download=download)
        data = await loop.run_in_executor(None, to_run)

        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]

        if creat_Queued_message == True :
            embed = discord.Embed(title="", description=f"Queued [{data['title']}]({data['webpage_url']}) [{ctx.author.mention}]", color=0x73bbff)
            await ctx.send(embed=embed)

        if download:
            source = ytdl.prepare_filename(data)
        else:
            return {'webpage_url': data['webpage_url'], 'requester': ctx.author, 'title': data['title']}

        return cls(discord.FFmpegPCMAudio(source), data=data, requester=ctx.author)

    @classmethod
    async def regather_stream(cls, data, *, loop):
        """Used for preparing a stream, instead of downloading.
        Since Youtube Streaming links expire."""
        loop = loop or asyncio.get_event_loop()
        requester = data['requester']

        to_run = partial(ytdl.extract_info, url=data['webpage_url'], download=False)
        data = await loop.run_in_executor(None, to_run)

        return cls(discord.FFmpegPCMAudio(data['url']), data=data, requester=requester)

class MusicPlayer:
    """A class which is assigned to each guild using the bot for Music.
    This class implements a queue and loop, which allows for different guilds to listen to different playlists
    simultaneously.
    When the bot disconnects from the Voice it's instance will be destroyed.
    """

    __slots__ = ('bot', '_guild', '_channel', '_cog', 'queue', 'next', 'current', 'np', 'volume')

    def __init__(self, ctx):
        self.bot = ctx.bot
        self._guild = ctx.guild
        self._channel = ctx.channel
        self._cog = ctx.cog

        self.queue = asyncio.Queue()
        self.next = asyncio.Event()

        self.np = None  # Now playing message
        self.volume = .5
        self.current = None

        ctx.bot.loop.create_task(self.player_loop())

    async def player_loop(self):
        """Our main player loop."""
        await self.bot.wait_until_ready()

        while not self.bot.is_closed():
            self.next.clear()

            try:
                # Wait for the next song. If we timeout cancel the player and disconnect...
                async with timeout(300):  # 5 minutes...
                    source = await self.queue.get()
            except asyncio.TimeoutError:
                return self.destroy(self._guild)

            if not isinstance(source, YTDLSource):
                # Source was probably a stream (not downloaded)
                # So we should regather to prevent stream expiration
                try:
                    source = await YTDLSource.regather_stream(source, loop=self.bot.loop)
                except Exception as e:
                    await self._channel.send(f'There was an error processing your song.\n'
                                             f'```css\n[{e}]\n```')
                    continue


        

            seconds = int(source.duration) % (24 * 3600) 
            hour = seconds // 3600
            seconds %= 3600
            minutes = seconds // 60
            seconds %= 60
            if hour > 0:
                duration = "%dhours, %dminutes, %dseconds" % (hour, minutes, seconds)
            else:
                duration = "%dminutes, %dseconds" % (minutes, seconds)

            self._guild.voice_client.play(source, after=lambda _: self.bot.loop.call_soon_threadsafe(self.next.set))

            embed = (discord.Embed(title='Now playing',
                               description=f'```css\n{source.title}\n```',
                               color=0x73d7ff)
                 .add_field(name='Duration', value=duration)
                 .add_field(name='Requested by', value=source.requester.mention)
                 .add_field(name='Uploader', value=f'[{source.uploader}]({source.uploader_url})')
                 .add_field(name='URL', value=f'[Click]({source.web_url})')
                 .set_thumbnail(url=source.thumbnail))
            self.np = await self._channel.send(embed=embed)
            await self.next.wait()

            # Make sure the FFmpeg process is cleaned up.
            source.cleanup()
            self.current = None

    def destroy(self, guild):
        """Disconnect and cleanup the player."""
        return self.bot.loop.create_task(self._cog.cleanup(guild))


class Music(commands.Cog):
    """Music related commands."""

    __slots__ = ('bot', 'players')

    def __init__(self, bot):
        self.bot = bot
        self.players = {}
        self.totalvotes = []

    async def cleanup(self, guild):
        try:
            await guild.voice_client.disconnect()
        except AttributeError:
            pass

        try:
            del self.players[guild.id]
        except KeyError:
            pass

    async def __local_check(self, ctx):
        """A local check which applies to all commands in this cog."""
        if not ctx.guild:
            raise commands.NoPrivateMessage
        return True

    async def __error(self, ctx, error):
        """A local error handler for all errors arising from commands in this cog."""
        if isinstance(error, commands.NoPrivateMessage):
            try:
                return await ctx.send('This command can not be used in Private Messages.')
            except discord.HTTPException:
                pass
        elif isinstance(error, InvalidVoiceChannel):
            await ctx.send('Error connecting to Voice Channel. '
                           'Please make sure you are in a valid channel or provide me with one')

        print('Ignoring exception in command {}:'.format(ctx.command), file=sys.stderr)
        traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)

    def get_player(self, ctx):
        """Retrieve the guild player, or generate one."""
        try:
            player = self.players[ctx.guild.id]
        except KeyError:
            player = MusicPlayer(ctx)
            self.players[ctx.guild.id] = player

        return player

    @commands.command(name='connect', aliases=['join','c'], description="connects to voice channel")
    async def connect_(self, ctx, *, channel: discord.VoiceChannel=None):
        """Connect to voice.
        Parameters
        ------------
        channel: discord.VoiceChannel [Optional]
            The channel to connect to. If a channel is not specified, an attempt to join the voice channel you are in
            will be made.
        This command also handles moving the bot to different channels.
        """
        if not channel:
            try:
                channel = ctx.author.voice.channel
            except AttributeError:
                embed = discord.Embed(title="", description="No channel to connect. Please call `/connect` from a voice channel.", color=0xff0000)
                await ctx.send(embed=embed)
                raise InvalidVoiceChannel('No channel to connect. Please either specify a valid channel or connect one.')

        vc = ctx.voice_client

        if vc:
            if vc.channel.id == channel.id:
                return
            try:
                await vc.move_to(channel)
            except asyncio.TimeoutError:
                raise VoiceConnectionError(f'Moving to channel: <{channel}> timed out.')
        else:
            try:
                await channel.connect()
            except asyncio.TimeoutError:
                raise VoiceConnectionError(f'Connecting to channel: <{channel}> timed out.')
         
        embed = discord.Embed(title=f"connectting to `{channel}` voice_channel...",color=0x73bbff)
        await ctx.send(embed=embed)

    @commands.command(name='play', aliases=['p','PLAY','P'], description="streams music")
    async def play_(self, ctx, *, search: str):
        """Request a song and add it to the queue.
        This command attempts to join a valid voice channel if the bot is not already in one.
        Uses YTDL to automatically search and retrieve a song.
        Parameters
        ------------
        search: str [Required]
            The song to search and retrieve using YTDL. This could be a simple search, an ID or URL.
        """
        if (ctx.channel.id in playchannel) or enable_special_playchannel == False :

            await ctx.trigger_typing()

            vc = ctx.voice_client

            if not vc:
                await ctx.invoke(self.connect_)

            player = self.get_player(ctx)

            # If download is False, source will be a dict which will be used later to regather the stream.
            # If download is True, source will be a discord.FFmpegPCMAudio with a VolumeTransformer.
            if "https://youtube.com/playlist?list=" in search :
                songs = YouTobe_playlist_exploer.search(search)
                for song in songs :
                    source = await YTDLSource.create_source(ctx, song, loop=self.bot.loop, download=False, creat_Queued_message=False)
                    await player.queue.put(source)
                embed = discord.Embed(title="", description=f"已從歌單載入{len(songs)}首歌!", color=0xf6ff00)
                await ctx.send(embed=embed)
                await ctx.invoke(self.queue_info)
            else :
                source = await YTDLSource.create_source(ctx, search, loop=self.bot.loop, download=False, creat_Queued_message=True)

            await player.queue.put(source)
        else :
            embed = discord.Embed(title="", description="Please request a song on the designated channel.", color=0xf6ff00)
            await ctx.send(embed=embed)

    @commands.command(name='pause', aliases=['stop'], description="pauses music")
    async def pause_(self, ctx):
        """Pause the currently playing song."""
        vc = ctx.voice_client

        if not vc or not vc.is_playing():
            embed = discord.Embed(title="", description="I am currently not playing anything", color=0xf6ff00)
            return await ctx.send(embed=embed)
        elif vc.is_paused():
            return

        vc.pause()
        await ctx.message.add_reaction('⏸️')
        await ctx.send("Paused")

    @commands.command(name='resume', description="resumes music")
    async def resume_(self, ctx):
        """Resume the currently paused song."""
        vc = ctx.voice_client

        if not vc or not vc.is_connected():
            embed = discord.Embed(title="", description="I'm not connected to a voice channel", color=0xff0000)
            return await ctx.send(embed=embed)
        elif not vc.is_paused():
            return

        vc.resume()
        await ctx.message.add_reaction('⏯️')
        await ctx.send("Resuming")

    @commands.command(name='skip', description="skips to next song in queue")
    async def skip_(self, ctx):
        """Skip the song."""
        vc = ctx.voice_client
        voter = ctx.message.author

        if not vc or not vc.is_connected():
            embed = discord.Embed(title="", description="I'm not connected to a voice channel", color=0xff0000)
            return await ctx.send(embed=embed)

        if not vc or not vc.is_playing():
            embed = discord.Embed(title="", description="I am currently not playing anything", color=0xf6ff00)
            return await ctx.send(embed=embed)

        if vc.is_paused():
            pass
        elif not vc.is_playing():
            return

        if voter == vc.source.requester :
            await ctx.message.add_reaction('⏭')
            self.totalvotes.clear()
            vc.stop()

        elif ctx.message.author.id in owner_id :
            await ctx.message.add_reaction('⏭')
            self.totalvotes.clear()
            vc.stop()
            await ctx.send("執行身分:#[系統管理員]")
            await ctx.send(file=discord.File(source.adminpic))

        elif voter not in self.totalvotes :
            self.totalvotes.append(voter)
            total_votes = len(self.totalvotes)

            if total_votes >= 3:
                await ctx.message.add_reaction('⏭')
                self.totalvotes.clear()
                vc.stop()
            else:
                await ctx.send('Skip vote added, currently at **{}/3**'.format(total_votes))

        else:
            await ctx.send('You have already voted to skip this song.')

    
    @commands.command(name='remove', aliases=['rm'], description="removes specified song from queue")
    async def remove_(self, ctx, pos : int=None):
        """Removes specified song from queue"""

        vc = ctx.voice_client

        if not vc or not vc.is_connected():
            embed = discord.Embed(title="", description="I'm not connected to a voice channel", color=0xff0000)
            return await ctx.send(embed=embed)

        player = self.get_player(ctx)
        if pos == None:
            player.queue._queue.pop()
        else:
            try:
                s = player.queue._queue[pos-1]
                del player.queue._queue[pos-1]
                embed = discord.Embed(title="", description=f"Removed [{s['title']}]({s['webpage_url']}) [{s['requester'].mention}]", color=0xf200ff)
                await ctx.send(embed=embed)
            except:
                embed = discord.Embed(title="", description=f'Could not find a track for "{pos}"', color=0xff0000)
                await ctx.send(embed=embed)
    
    @commands.command(name='clear', aliases=['clr','fs','FS'], description="clears entire queue")
    async def clear_(self, ctx):
        """Deletes entire queue of upcoming songs."""

        vc = ctx.voice_client

        if not vc or not vc.is_connected():
            embed = discord.Embed(title="", description="I'm not connected to a voice channel", color=0xff0000)
            return await ctx.send(embed=embed)

        player = self.get_player(ctx)
        player.queue._queue.clear()
        await ctx.message.add_reaction('💣')
        await ctx.send('**Cleared**')

    @commands.command(name='queue', aliases=['q', 'playlist', 'que'], description="shows the queue")
    async def queue_info(self, ctx):
        """Retrieve a basic queue of upcoming songs."""
        vc = ctx.voice_client

        if not vc or not vc.is_connected():
            embed = discord.Embed(title="", description="I'm not connected to a voice channel", color=0xff0000)
            return await ctx.send(embed=embed)

        player = self.get_player(ctx)
        if player.queue.empty():
            embed = discord.Embed(title="", description="queue is empty", color=0xf6ff00)
            return await ctx.send(embed=embed)

        seconds = vc.source.duration % (24 * 3600) 
        hour = seconds // 3600
        seconds %= 3600
        minutes = seconds // 60
        seconds %= 60
        if hour > 0:
            duration = "%dh %02dm %02ds" % (hour, minutes, seconds)
        else:
            duration = "%02dm %02ds" % (minutes, seconds)

        # Grabs the songs in the queue...
        upcoming = list(itertools.islice(player.queue._queue, 0, int(len(player.queue._queue))))
        fmt = '\n'.join(f"`{(upcoming.index(_)) + 1}.` [{_['title']}]({_['webpage_url']}) | ` {duration} Requested by: {_['requester']}`\n" for _ in upcoming)
        fmt = f"\n__Now Playing__:\n[{vc.source.title}]({vc.source.web_url}) | ` {duration} Requested by: {vc.source.requester}`\n\n__Up Next:__\n" + fmt + f"\n**{len(upcoming)} songs in queue**"
        embed = discord.Embed(title=f'Queue for {ctx.guild.name}', description=fmt, color=0x00ff33)
        embed.set_footer(text=f"{ctx.author.display_name}", icon_url=ctx.author.avatar_url)

        await ctx.send(embed=embed)

    @commands.command(name='nowplaying', aliases=['playing'], description="shows the current playing song")
    async def now_playing_(self, ctx):
        """Display information about the currently playing song."""
        vc = ctx.voice_client

        if not vc or not vc.is_connected():
            embed = discord.Embed(title="", description="I'm not connected to a voice channel", color=0xff0000)
            return await ctx.send(embed=embed)

        player = self.get_player(ctx)

        if not vc or not vc.is_playing():
            embed = discord.Embed(title="", description="I am currently not playing anything", color=0xf6ff00)
            return await ctx.send(embed=embed)
        
        seconds = vc.source.duration % (24 * 3600) 
        hour = seconds // 3600
        seconds %= 3600
        minutes = seconds // 60
        seconds %= 60
        if hour > 0:
            duration = "%dhours, %dminutes, %dseconds" % (hour, minutes, seconds)
        else:
            duration = "%dminutes, %dseconds" % (minutes, seconds)

        embed = (discord.Embed(title='Now playing',
                               description=f'```css\n{vc.source.title}\n```',
                               color=0x73d7ff)
                 .add_field(name='Duration', value=duration)
                 .add_field(name='Requested by', value=vc.source.requester.mention)
                 .add_field(name='Uploader', value=f'[{vc.source.uploader}]({vc.source.uploader_url})')
                 .add_field(name='URL', value=f'[Click]({vc.source.web_url})')
                 .set_thumbnail(url=vc.source.thumbnail))
        embed.set_author(icon_url=self.bot.user.avatar_url, name=f"CORN Studio _Music")
        await ctx.send(embed=embed)

    @commands.command(name='volume', aliases=['vol', 'v'], description="changes Kermit's volume")
    async def change_volume(self, ctx, *, vol: float=None):
        """Change the player volume.
        Parameters
        ------------
        volume: float or int [Required]
            The volume to set the player to in percentage. This must be between 1 and 100.
        """
        vc = ctx.voice_client

        if not vc or not vc.is_connected():
            embed = discord.Embed(title="", description="I am not currently connected to voice channel", color=0xff0000)
            return await ctx.send(embed=embed)
        
        if not vol:
            embed = discord.Embed(title="", description=f"🔊 **{(vc.source.volume)*100}%**", color=0x00ff00)
            return await ctx.send(embed=embed)

        if not 0 < vol < 101:
            embed = discord.Embed(title="", description="Please enter a value between 1 and 100", color=0xf6ff00)
            return await ctx.send(embed=embed)

        player = self.get_player(ctx)

        if vc.source:
            vc.source.volume = vol / 100

        player.volume = vol / 100
        embed = discord.Embed(title="", description=f'**`{ctx.author}`** set the volume to **{vol}%**', color=0x00ff00)
        await ctx.send(embed=embed)

    @commands.command(name='disconnect', aliases=["d", "leave"], description="stops music and disconnects from voice")
    async def leave_(self, ctx):
        """Stop the currently playing song and destroy the player.
        !Warning!
            This will destroy the player assigned to your guild, also deleting any queued songs and settings.
        """
        vc = ctx.voice_client

        if not vc or not vc.is_connected():
            embed = discord.Embed(title="", description="I'm not connected to a voice channel", color=0xff0000)
            return await ctx.send(embed=embed)

        embed = discord.Embed(title="disconnect...",color=0x232323)
        await ctx.send(embed=embed)
        await self.cleanup(ctx.guild)

    @commands.command(name='loop', description="loop now playing song.")
    async def loop_(self, ctx):

        vc = ctx.voice_client

        if not vc or not vc.is_connected():
            embed = discord.Embed(title="", description="I'm not connected to a voice channel", color=0xff0000)
            return await ctx.send(embed=embed)

        if not vc or not vc.is_playing():
            embed = discord.Embed(title="", description="I am currently not playing anything", color=0xf6ff00)
            return await ctx.send(embed=embed)

    

    @commands.command(name='break', description="break play loop.")
    async def break_(self, ctx):

        vc = ctx.voice_client

        if not vc or not vc.is_connected():
            embed = discord.Embed(title="", description="I'm not connected to a voice channel", color=0xff0000)
            return await ctx.send(embed=embed)

        if not vc or not vc.is_playing():
            embed = discord.Embed(title="", description="I am currently not playing anything", color=0xf6ff00)
            return await ctx.send(embed=embed)
    

def setup(bot):
    bot.add_cog(Music(bot))
