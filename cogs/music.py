import discord
from discord.ext import commands

from youtube_dl import YoutubeDL




class Music(commands.Cog):
    def __init__(self, client):
        self.client = client

        self.isPlaying = False

        self.music_queue = []
        self.YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist': 'True'}
        self.FFMPEG_OPTIONS = {'before_options': ' -reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}

        self.vc = ""

    def search_yt (self, item):
        with YoutubeDL(self.YDL_OPTIONS) as ydl:
            try:
                info = ydl.extract_info("ytsearch:%s" % item, download=False)['entries'][0]
            except Exception:
                return False

        return {'source':info['formats'][0]['url'], 'title': info['title']} #can store extra stuff here as well

    
    def play_next(self):
        if len(self.music_queue) > 0:
            self.isPlaying = True
            music_url = self.music_queue[0][0]['source']
            self.music_queue.pop(0)


            self.vc.play(discord.FFmpegPCMAudio(music_url, **self.FFMPEG_OPTIONS), after = lambda e: self.play_next())
        else:
            self.isPlaying = False

    async def play_music(self):
        if len(self.music_queue) > 0:
            self.isPlaying = True
            music_url = self.music_queue[0][0]['source']

            if self.vc == "" or not not self.vc.is_connected():
                # for opus_lib in opus_libs:
                #     try:
                #         opus.load_opus(opus_lib)
                #         return
                #     except OSError:
                #         pass
                self.vc = await self.music_queue[0][1].connect()
            else:
                self.vc = await self.client.move_to(self.music_queue[0][1])

            self.music_queue.pop(0)

            self.vc.play(discord.FFmpegPCMAudio( music_url, **self.FFMPEG_OPTIONS), executable="C:\FFmpeg\bin\ffmpeg.exe",after = lambda e: self.play_next())
        else:
            self.isPlaying = False

    @commands.command(name ="play")
    async def p(self,ctx,* args):
        query = " ".join(args)
        try:
            voice_channel = ctx.author.voice.channel
        except:
            await ctx.send("Connect to a voice channel gaandu bsdk!")
        # if voice_channel is None:
        #     await ctx.send("Connect to a voice channel gaandu bsdk!")
        else:
            song = self.search_yt(query)
            if type(song) == type(True):
                await ctx.send("Could not download the song")
            else:
                await ctx.send("Song added to queue")
                self.music_queue.append([song,voice_channel])

                if self.isPlaying == False:
                    await self.play_music()

    
    @commands.command(name ="q" )
    async def q(self,ctx):
        retVal = ""
        for i in range(0,len(self.music_queue)):
            retVal += self.music_queue[i][0]['title'] + "\n"
        
        print (retVal)

        if retVal != "":
            await ctx.send(retVal)
        else:
            await ctx.send("No music in the queue")

    @commands.command(name = "skip")
    async def skip(self,ctx):
        if self.vc != "":
            self.vc.stop()
            await self.play_music()

    
def setup(client):
    client.add_cog(Music(client))