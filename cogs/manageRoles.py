import discord
import os
import asyncio
from discord.ext import commands
from discord.ext.commands.core import command
from discord.utils import get

class ManageRoles(commands.Cog):
    
    def __init__(self, client):
        self.client = client


    @commands.command(name="give")
    async def giverole(self,ctx, teamNum: str ,members: commands.Greedy[discord.Member]):
        knownrole = discord.utils.get(ctx.guild.roles, name=teamNum)
        for member in members:
            await ctx.send(f"{member} has been assigned team number {teamNum}")
            await member.add_roles(knownrole)
    

    @commands.command(name="removerole")
    @commands.has_role('QM')
    async def mute(self,ctx, teamNum: str, users: commands.Greedy[discord.Member]):
        role = discord.utils.get(ctx.guild.roles, name=teamNum)
        for user in users:
            if user.has_role(role):
                await user.remove_roles(role)
                await ctx.send(f'{user.name} has been removed from role {teamNum}')
            else :
                await ctx.send(f':{user.name} does not have the mentioned role {teamNum}')


    @commands.command(name="deleteAllRoles")
    async def delete_role(self,ctx):
        role_object = discord.utils.get(ctx.message.guild.roles, name="QM")
        await role_object.delete()
        for i in range(1,13): 
            role_object = discord.utils.get(ctx.message.guild.roles, name=str(i))
            if role_object is not None:
                await role_object.delete()
        await ctx.send("All roles removed")


def setup(client):
    client.add_cog(ManageRoles(client))