import discord
from discord.ext import commands

import asyncio

from dm_assist.config import config

from . import advanced_shuffle


class VoiceEntry:
    def __init__(self, message, player):
        self.requester = message.author
        self.channel = message.channel
        self.player = player

    def __str__(self):
        fmt = '*{0.title}* uploaded by {0.uploader} and requested by {1.display_name}'
        duration = self.player.duration
        if duration:
            fmt = fmt + ' [length: {0[0]}m {0[1]}s]'.format(divmod(duration, 60))
        return fmt.format(self.player, self.requester)


class VoiceState:
    def __init__(self, bot):
        self.current = None
        self.voice = None
        self.bot = bot
        self.play_next_song = asyncio.Event()
        self.songs = asyncio.Queue()
        self.skip_votes = set() # a set of user_ids that voted
        self.audio_player = self.bot.loop.create_task(self.audio_player_task())
        self.loop = False

        self._volume = config.config.voice.default_volume / 100
        
        self.backgrounds = config.music

        self.current_theme = None
        self.current_theme_message = None

    def is_playing(self):
        if self.voice is None or self.current is None:
            return False

        player = self.current.player
        return not player.is_done()

    @property
    def player(self):
        return self.current.player

    def skip(self):
        self.skip_votes.clear()
        if self.is_playing():
            self.player.stop()

    def toggle_next(self):
        self.bot.loop.call_soon_threadsafe(self.play_next_song.set)
    
    async def queue(self, song, message):
        opts = {
            'default_search': 'auto',
            'quiet': True,
        }
        print('queueing ' + song)
        try:
            player = await self.voice.create_ytdl_player(song, ytdl_options=opts, after=self.toggle_next)
        except Exception as e:
            fmt = 'An error occurred while processing this request: ```py\n{}: {}\n```'
            await self.bot.send_message(self.current.channel, fmt.format(type(e).__name__, e))
            return False
        else:
            entry = VoiceEntry(message, player)
            await self.songs.put(entry)
            return entry

    async def play_background(self, background, message, stop_music=True):
        if background in self.backgrounds:
            self.current_theme = advanced_shuffle.Shuffle(self.backgrounds[background])
            self.current_theme_message = message
            if self.is_playing():
                self.skip()
            return await self.queue(self.current_theme.get_next_item(), message)
        else:
            return False
    
    def stop_background(self, stop_music=True):
        self.current_theme = None
        self.current_theme_message = None

        if stop_music:
            self.skip()

    async def audio_player_task(self):
        while True:
            self.play_next_song.clear()
            if self.loop == False:
                # Add a song to the queue if there is no song currently on the queue, and there is a theme playing
                if self.current_theme is not None and self.songs.empty():
                    await self.queue(self.current_theme.get_next_item(), self.current_theme_message)
                self.current = await self.songs.get()
            else:
                self.current = self.current
            await self.bot.send_message(self.current.channel, 'Now playing ' + str(self.current))
            self.current.player.volume = self.volume
            self.current.player.start()
            await self.play_next_song.wait()
    
    @property
    def volume(self):
        return self._volume
    
    @volume.setter
    def volume(self, value):
        if self.is_playing():
            self.current.player.volume = value
        self._volume = value

class Music:
    """Voice related commands.
    Works in multiple servers at once.
    """
    def __init__(self, bot):
        self.bot = bot
        self.voice_states = {}

    def get_voice_state(self, server):
        state = self.voice_states.get(server.id)
        if state is None:
            state = VoiceState(self.bot)
            self.voice_states[server.id] = state

        return state

    async def create_voice_client(self, channel):
        voice = await self.bot.join_voice_channel(channel)
        state = self.get_voice_state(channel.server)
        state.voice = voice

    def __unload(self):
        for state in self.voice_states.values():
            try:
                state.audio_player.cancel()
                if state.voice:
                    self.bot.loop.create_task(state.voice.disconnect())
            except:
                pass

    #@commands.command(pass_context=True, no_pm=True)
    #async def loop(self, ctx):
    #    """Toggles looping the current song.
    #    Off by default."""
    #    if self.loop == True:
    #        self.loop = False
    #    else:
    #        self.loop = True

    @commands.command(pass_context=True, no_pm=True)
    async def join(self, ctx, *, channel = None):
        """Joins a voice channel."""
        if channel is None:
            await ctx.invoke(self.summon)
            return
        
        # Find the channel the user is referring to
        channel = discord.utils.find(lambda c: c.name == channel, ctx.message.server.channels)

        try:
            await self.create_voice_client(channel)
        except discord.InvalidArgument:
            await self.bot.say('This is not a voice channel...')
        except discord.ClientException:
            await self.bot.say('Already in a voice channel...')
        else:
            await self.bot.say('Ready to play audio in ' + channel.name)

    @commands.command(pass_context=True, no_pm=True)
    async def summon(self, ctx):
        """Summons the bot to join your voice channel."""
        summoned_channel = ctx.message.author.voice_channel
        if summoned_channel is None:
            await self.bot.say('You are not in a voice channel.')
            return False

        state = self.get_voice_state(ctx.message.server)
        if state.voice is None:
            state.voice = await self.bot.join_voice_channel(summoned_channel)
            await self.bot.say('Ready to play audio in ' + summoned_channel.name)
        else:
            await state.voice.move_to(summoned_channel)

        return True

    @commands.command(pass_context=True, no_pm=True)
    async def play(self, ctx, *, song : str):
        """Plays a song.
        If there is a song currently in the queue, then it is
        queued until the next song is done playing.
        This command automatically searches as well from YouTube.
        The list of supported sites can be found here:
        https://rg3.github.io/youtube-dl/supportedsites.html
        """
        state = self.get_voice_state(ctx.message.server)

        if state.voice is None:
            success = await ctx.invoke(self.summon)
            if not success:
                return

        result = await state.queue(song, ctx.message)

        if result is not False:
            await self.bot.say('Enqueued ' + str(result))
    
    @commands.command(pass_context=True, no_pm=True)
    async def background(self, ctx, *, theme=None):
        """Plays a list of background music.
        If there is a song currently in the queue, then it is
        queued until the next song is done playing.
        This command plays random songs based on the theme in the config.yaml
        """

        state = self.get_voice_state(ctx.message.server)

        async def print_help():
            message = 'The possible themes are:\n```\n{}```'.format(
                '\n'.join([theme.capitalize() for theme in state.backgrounds.keys()])
            )
            await self.bot.say(message)

        if theme is None:
            await print_help()
            return

        theme = theme.lower()

        if state.voice is None:
            success = await ctx.invoke(self.summon)
            if not success:
                return
        
        result = await state.play_background(theme, ctx.message)

        if result is not False:
            await self.bot.say('Queued {} music'.format(theme.capitalize()))
        else:
            await print_help()

    @commands.command(pass_context=True, no_pm=True)
    async def stopbackground(self, ctx):
        """
        Stops the current background music.

        The current song will however not be stopped.
        """

        state = self.get_voice_state(ctx.message.server)

        state.stop_background()

        await self.bot.say('Stopped the background music.')

    @commands.command(pass_context=True, no_pm=True)
    async def volume(self, ctx, value=None):
        """Sets the volume of the currently playing song."""

        state = self.get_voice_state(ctx.message.server)

        if value is None:
            await self.bot.say('The current volume is {:.0%}'.format(state.volume))
            return

        try:
            state.volume = int(value) / 100
        except ValueError:
            await self.bot.say('{} is not a valid volume'.format(value))
        else:
            await self.bot.say('Set the volume to {:.0%}'.format(state.volume))

    @commands.command(pass_context=True, no_pm=True)
    async def pause(self, ctx):
        """Pauses the currently played song."""
        state = self.get_voice_state(ctx.message.server)
        if state.is_playing():
            player = state.player
            player.pause()

    @commands.command(pass_context=True, no_pm=True)
    async def resume(self, ctx):
        """Resumes the currently played song."""
        state = self.get_voice_state(ctx.message.server)
        if state.is_playing():
            player = state.player
            player.resume()

    @commands.command(pass_context=True, no_pm=True)
    async def stop(self, ctx):
        """Stops playing audio and leaves the voice channel.
        This also clears the queue.
        """
        server = ctx.message.server
        state = self.get_voice_state(server)

        if state.is_playing():
            player = state.player
            player.stop()

        try:
            state.audio_player.cancel()
            del self.voice_states[server.id]
            await state.voice.disconnect()
        except:
            pass

    @commands.command(pass_context=True, no_pm=True)
    async def skip(self, ctx):
        """Vote to skip a song. The song requester can automatically skip.
        3 skip votes are needed for the song to be skipped.
        """

        state = self.get_voice_state(ctx.message.server)
        if not state.is_playing():
            await self.bot.say('Not playing any music right now...')
            return

        voter = ctx.message.author
        if voter == state.current.requester:
            await self.bot.say('Requester requested skipping song...')
            state.skip()
        elif voter.id not in state.skip_votes:
            state.skip_votes.add(voter.id)
            total_votes = len(state.skip_votes)
            if total_votes >= 3:
                await self.bot.say('Skip vote passed, skipping song...')
                state.skip()
            else:
                await self.bot.say('Skip vote added, currently at [{}/3]'.format(total_votes))
        else:
            await self.bot.say('You have already voted to skip this song.')

    @commands.command(pass_context=True, no_pm=True)
    async def playing(self, ctx):
        """Shows info about the currently played song."""

        state = self.get_voice_state(ctx.message.server)
        if state.current is None:
            await self.bot.say('Not playing anything.')
        else:
            skip_count = len(state.skip_votes)
            await self.bot.say('Now playing {} [skips: {}/3]'.format(state.current, skip_count))