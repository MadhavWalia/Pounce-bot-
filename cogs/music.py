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

        return {'source':info['formats'][0]['url'], 'title': info['title'], 'thumbnail' : info['thumbnail']} #can store extra stuff here as well

    
    def play_next(self):
        if len(self.music_queue) > 0:
            self.isPlaying = True
            music_url = self.music_queue[0][0]['source']
            self.music_queue.pop(0)


            self.vc.play(discord.FFmpegPCMAudio(music_url, **self.FFMPEG_OPTIONS), after = lambda e: self.play_next())
        else:
            self.isPlaying = False

    async def play_music(self,ctx):
        if len(self.music_queue) > 0:
            self.isPlaying = True
            music_url = self.music_queue[0][0]['source']
            music_thumbnail = self.music_queue[0][0]['thumbnail']
            music_title = self.music_queue[0][0]['title']

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
            
            embed=discord.Embed(title="Now playing", 
                description=music_title, color=0xFF5733)
            # embed.set_image(music_thumbnail)
            await ctx.send(embed = embed)
            self.vc.play(discord.FFmpegPCMAudio( music_url, **self.FFMPEG_OPTIONS),after = lambda e: self.play_next())

            
        else:
            self.isPlaying = False

    @commands.command(name ="play")
    async def p(self,ctx,* args):
        query = " ".join(args)
        try:
            voice_channel = ctx.author.voice.channel
        except:
            await ctx.send("Connect to a voice channel")
        if voice_channel is None:
            await ctx.send("Connect to a voice channel ")
        else:
            song = self.search_yt(query)
            if type(song) == type(True):
                await ctx.send("Could not download the song")
            else:
                embed=discord.Embed(description="Song has succesfully been added to the queue", 
                                    color=0xFF5733)
                await ctx.send(embed=embed)
                # await ctx.send("Song added to queue")
                self.music_queue.append([song,voice_channel])

                if self.isPlaying == False:
                    await self.play_music(ctx)

    
    @commands.command(name ="q" )
    async def q(self,ctx):
        retVal = ""
        embed=discord.Embed(title="Music Queue", 
                description="Songs in the queue", color=0xFF5733)
        for i in range(0,len(self.music_queue)):
            retVal += self.music_queue[i][0]['title'] + "\n"
            embed.add_field(name= str(i+1) + ") " + self.music_queue[i][0]['title'],value = "Need to add duration or URL here",inline=False)
        
        print (retVal)

        if retVal != "":
            await ctx.send(embed = embed)
            await ctx.send(retVal)
        else:
            embed1=discord.Embed(description="No songs in the queue", 
                                color=0xFF5733)
            await ctx.send(embed = embed1)
            # await ctx.send("No music in the queue")

    @commands.command(name = "next")
    async def skip(self,ctx):
        if self.vc != "":
            self.vc.stop()
            embed=discord.Embed(description="Playing the next song in the queue", 
                                color=0xFF5733)
            await ctx.send(embed=embed)
            await self.play_music(ctx)

    @commands.command(name="leave")
    async def leave(self,ctx):
        try :
            server = ctx.message.guild.voice_client
            embed=discord.Embed(description="Bot has been disconnected", 
                                color=0xFF5733)
            await ctx.send(embed=embed)
            await server.disconnect()
        except AttributeError:
            await ctx.send("Not in a voice channel ")

    
    @commands.command(name="pause")
    async def pause(self,ctx):
        voiceClient = ctx.message.guild.voice_client
        if voiceClient.is_playing():
            await voiceClient.pause()
        else:
            await ctx.send("The bot is not playing anything at the moment")

    
    @commands.command(name="resume")
    async def resume(self,ctx):
        voiceClient = ctx.message.guild.voice_client
        if voiceClient.is_paused():
            await voiceClient.resume()
        else:
            await ctx.send("The bot was not playing anything before this command, use play")
    
def setup(client):
    client.add_cog(Music(client))