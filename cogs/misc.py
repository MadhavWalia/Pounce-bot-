import discord
import os
import asyncio
from discord.ext import commands
from discord.ext.commands.core import command
from discord.utils import get

class Misc(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(name="clear")
    async def clear(self,ctx, amount=None):
        if amount is None:
            await ctx.channel.purge(limit=5)
            await ctx.send(f":spy: Default `5` messages deleted",delete_after = 5)

        elif amount == "all":
            await ctx.channel.purge()
            await ctx.send(":spy: All messages deleted",delete_after = 2)
        else:
            await ctx.channel.purge(limit=int(amount)+1)
            await ctx.send(f":spy: I have deleted `{amount}` messages !",delete_after = 5)


    @commands.command(name="message")
    async def message(self, ctx, msg : str):
            message = await ctx.send(msg)
            if msg is not None:
                for i in range(13):
                    channel = discord.utils.get(ctx.guild.channels, name=f"team-{i}")
                    if channel is not None:
                        channel_id = channel.id
                        channel = self.client.get_channel(channel_id)
                        await channel.send(msg)
            else :
                await ctx.send("Enter message to be sent")

def setup(client):
    client.add_cog(Misc(client))