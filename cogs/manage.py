import discord
import os
import asyncio
from discord.ext import commands
from discord.ext.commands.core import command
from discord.utils import get

colors = ["caf0f8","94d2bd","f77f00","ffadad","fdffb6","caffbf","a0c4ff","bdb2ff","ffc6ff","fffffc","006d77","d9ed92"]

class Manage(commands.Cog):

    def __init__(self, client):
        self.client = client
    
    @commands.command(name="make") 
    @commands.has_permissions(manage_roles=True)
    async def create (self, ctx, number: int):
        if (number > 12):
            await ctx.send("Sorry can't have more than 12 teams, enter a number less than 12 again")
        else:
            QMRole = discord.utils.get(ctx.guild.roles,name="QM")
            perms = {'read_messages': True,'send_messages': True}
            cat = discord.utils.get(ctx.guild.categories, name = "Text Channels")
            if cat is None:
                await ctx.guild.create_category("Text Channels")
                cat = discord.utils.get(ctx.guild.categories, name = "Text Channels")
            cat2 = discord.utils.get(ctx.guild.categories, name = "Voice Channels")
            if cat2 is None:
                await ctx.guild.create_category("Voice Channels")
                cat2 = discord.utils.get(ctx.guild.categories, name = "Voice Channels")

            if get(ctx.guild.roles, name="QM"):
                await ctx.send("Role QM already exists")
            else:
                await ctx.guild.create_role(name = "QM", color  = int("f72585", 16),hoist = True)

            for  i in range(1,number + 1):
                if get(ctx.guild.roles, name = str(i)):
                    await ctx.send(f"Role {i} already exists")
                else:
                    await ctx.guild.create_role(name = str(i), color = int(colors[i-1], 16),hoist = True)

            for i in range (1,number+1): #need to check if the channel name already exists 
                teamRole = discord.utils.get(ctx.guild.roles,name=str(i))

                await ctx.guild.create_text_channel(f"Team {i}",
                                                    overwrites = {teamRole: discord.PermissionOverwrite(**perms), 
                                                        QMRole:discord.PermissionOverwrite(**perms),
                                                        ctx.guild.default_role: discord.PermissionOverwrite(read_messages=False),
                                                        ctx.guild.me: discord.PermissionOverwrite(read_messages=True, send_messages=True) 
                                                        },
                                                    category = cat)

                await ctx.guild.create_voice_channel(f"Team {i}",
                                                    overwrites = {teamRole: discord.PermissionOverwrite(**perms), 
                                                        QMRole:discord.PermissionOverwrite(**perms),
                                                        ctx.guild.default_role: discord.PermissionOverwrite(read_messages=False),
                                                        ctx.guild.me: discord.PermissionOverwrite(read_messages=True, send_messages=True) 
                                                    },
                                                    category = cat2)
            await ctx.guild.create_text_channel(f"Announcements",overwrites = {QMRole:discord.PermissionOverwrite(**perms),
                                                                            ctx.guild.default_role: discord.PermissionOverwrite(read_messages=True),
                                                                            ctx.guild.me: discord.PermissionOverwrite(read_messages=True, send_messages=False)},
                                                                            category = cat)
    

    @commands.command(name="deleteChannels")
    @commands.has_permissions(manage_roles = True)
    async def delete_Channels(self,ctx):
        for i in range(1,13): 
            channel_object = discord.utils.get(ctx.guild.channels, name=f"team-{str(i)}")
            if channel_object is not None:
                await channel_object.delete()



    @commands.command(name="deleteVoice")
    @commands.has_permissions(manage_roles = True)
    async def delete_VChannels(self,ctx):
        for i in range(1,13): 
            channel_object = discord.utils.get(ctx.guild.voice_channels, name=f"Team {str(i)}")
            if channel_object is not None:
                await channel_object.delete()

def setup(client):
    client.add_cog(Manage(client))