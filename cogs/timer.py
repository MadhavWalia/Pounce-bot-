import discord
import os
import asyncio
from discord.ext import commands
from discord.ext.commands.core import Command, command
from discord.utils import get

class Timer(commands.Cog):
    
    def __init__(self, client):
        self.client = client

    # @commands.command()
    # async def sendmessage(self,ctx, message: str):
    #     for i in range(13):
    #         channel = discord.utils.get(ctx.guild.channels, name=f"team-{i}")
    #         if channel is not None:
    #             channel_id = channel.id
    #             channel = self.client.get_channel(channel_id)
    #             await channel.send(message)

    @commands.command(name="open") 
    async def count(self,ctx, number:int = None):
        try:
            if number is None:
                number = 15
            if number < 0:
                await ctx.send('number cant be a negative')
            elif number > 300:
                await ctx.send('number must be under 300')
            else:
                # msg = f"Pounce window closes in `{str(number)}` seconds"
                # self.sendmessage(ctx,msg)
                message = await ctx.send(f"Pounce window closes in `{str(number)}` seconds")
                for i in range(13):
                    channel = discord.utils.get(ctx.guild.channels, name=f"team-{i}")
                    if channel is not None:
                        channel_id = channel.id
                        channel = self.client.get_channel(channel_id)
                        await channel.send(f"Pounce window closes in `{str(number)}` seconds")
                while number != 0:
                    number -= 1
                    await message.edit(content= f"Pounce window closes in `{str(number)}` seconds")
                    await asyncio.sleep(1)
                msg = "Pounce window closed!"
                # self.sendmessage(ctx,msg)
                await message.edit(content=f":spy: Pounce window closed!  ",delete_after = 5)
                for i in range(13):
                    channel = discord.utils.get(ctx.guild.channels, name=f"team-{i}")
                    if channel is not None:
                        channel_id = channel.id
                        channel = self.client.get_channel(channel_id)
                        await channel.send(f":spy: Pounce window closed!  ",delete_after = 5)

        except ValueError:
            await ctx.send('time was not a number')
    

    

def setup(client):
    client.add_cog(Timer(client))