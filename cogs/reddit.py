import discord
from discord.ext import commands

import asyncpraw
import os
from random import choice


curr = os.getcwd()
TEAM_MAX = 12

reddit = asyncpraw.Reddit(client_id = "DXzQidnkA78l9H7uC00QAg",
                     client_secret = "0uGfWgWjJC9W4kHXy_fLOhlRi0vwNQ",
                     username = "Pounce_bot",
                     password = "bot_pounce",
                     user_agent = "PounceBot")


class Reddit(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(name="trivia") 
    async def count(self, ctx):
        subreddit = await reddit.subreddit("todayilearned")
        all_posts = []

        posts = subreddit.hot(limit=50)
        async for post in posts:
            all_posts.append(post)

        random_post = choice(all_posts)
        fact = random_post.title[4:]
        url = random_post.url
        print(url)
        embed = discord.Embed(
            title = "Trivia",
            description = fact,
            url = url,
            colour = discord.Colour.blue()
        )

        await ctx.send(embed=embed)
    
def setup(client):
    client.add_cog(Reddit(client))
