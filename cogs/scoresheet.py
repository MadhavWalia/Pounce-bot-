import discord
from discord.ext import commands
import asyncio

import os
import pandas as pd

import gspread
from oauth2client.service_account import ServiceAccountCredentials

curr = os.getcwd()
TEAM_MAX = 12

class Scoresheet(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.ques = 0
        self.team_no = 0

    @commands.Cog.listener()
    async def on_ready(self):
        print('Bot is Online')

    async def sendMessage(self, ctx, message: str):
        for i in range(TEAM_MAX+1):
            channel = discord.utils.get(ctx.guild.channels, name=f"team-{i}")
            if channel is not None:
                channel_id = channel.id
                channel = self.client.get_channel(channel_id)
                await channel.send(message)


    @commands.command(name="start") 
    async def count(self,ctx, number :int = None):
        try:
            #If Number isn't assigned
            if number is None:
                number = 15

            if number < 0:
                await ctx.send('How does a negative timer even work!')

            elif number > 300:
                await ctx.send('Bruh just count upto that urself, not my job')

            else:
                message = await ctx.send(f"Pounce window closes in `{str(number)}` seconds")

                #Sending Window Open
                msg = f"Pounce window closes in `{str(number)}` seconds"
                await self.sendMessage(ctx,msg)

                #Countdown
                while number != 0:
                    number -= 1
                    await message.edit(content= f"Pounce window closes in `{str(number)}` seconds")
                    await asyncio.sleep(1)

                #Sending window closed
                msg = "Pounce window closed!"
                await message.edit(content=f":spy: Pounce window closed!  ",delete_after = 5)
                await self.sendMessage(ctx, msg)

        except ValueError:
            await ctx.send('Time was not a number')


    #Authorization
    def authorize(self):
        scope = ['https://spreadsheets.google.com/feeds',
                    'https://www.googleapis.com/auth/drive']

        GOOGLE_KEY_FILE = 'pounce-bot-key.json'

        credentials = ServiceAccountCredentials.from_json_keyfile_name(GOOGLE_KEY_FILE, scope)
        gc = gspread.authorize(credentials)
        return gc


    def make_default(self, worksheet: gspread.worksheet.Worksheet, questions: int, team_number: int):
        teams = [f'Team {n}' for n in range(1,team_number+1)]
        question_list = [f"Question {n}" for n in range(1,questions+1)]
        question_list.append('Total')
        col_val = gspread.utils.rowcol_to_a1(1, questions + 2)[:-1]

        self.ques = questions
        self.team_no = team_number
        
        #for question rows
        cell_list = worksheet.range(f'B1:{col_val}1')
        i=0
        for cell in cell_list:
            cell.value = question_list[i]
            i+=1
        
        worksheet.update_cells(cell_list)

        #for team columns
        cell_list = worksheet.range(f'A2:A{team_number+1}')
        i=0
        for cell in cell_list:
            cell.value = teams[i]
            i+=1
        
        worksheet.update_cells(cell_list)

        #for total column
        cell_list = worksheet.range(f'{col_val}2:{col_val}{team_number+1}')
        i=2
        end = gspread.utils.rowcol_to_a1(1, questions + 1)[:-1]
        for cell in cell_list:
            cell.value = f'=SUM(B{i}:{end}{i})'
            i+=1
        
        worksheet.update_cells(cell_list, value_input_option='USER_ENTERED')


    @commands.command(name="create")
    async def createSheet(self, ctx, questions: int, team_number: int, email: str):

        if questions>0 and team_number>0 and team_number<=TEAM_MAX:

            #Authorization
            gc = self.authorize()

            #Creating ScoreSheet
            workbook = gc.create('Score Sheet')
            scores = workbook.add_worksheet(title="Scores", rows="100", cols="100")
            self.make_default(scores, questions, team_number)
            pounces = workbook.add_worksheet(title="Pounces", rows="100", cols="100")
            self.make_default(pounces, questions, team_number)

            #Sharing ScoreSheet
            try:
                workbook.share(email, perm_type='user', role='writer') 
            except gspread.exceptions.APIError: 
                print("Pls give editor access to everyone for the sheet")

            #Sending Confirmation
            await ctx.send('Scoresheet has been created and sent, as if anyone is going to attend ur mubai style quiz lmao')                   
        
        elif team_number>TEAM_MAX:
            await ctx.send('No More than 12 teams')
        else:
            await ctx.send('Team and Question Numbers cannot be negative you potato brained human')


    @commands.command(name="display")
    async def displayScores(self, ctx):
        #Authorization
        gc = self.authorize()

        #Opening SpreadSheet
        try:
            ScoreSheet = gc.open('Score Sheet')
        except gspread.exceptions.SpreadsheetNotFound:
            await ctx.send("The ScoreSheet does not exist")

        #Displaying Scores
        embed = discord.Embed(
            title = "Scores",
            colour = discord.Colour.blue()
        )

        try:
            scores = ScoreSheet.worksheet("Scores")
        except gspread.exceptions.WorksheetNotFound:
            await ctx.send("Scores sheet is unavailable")

        total = scores.col_values(self.ques + 2)[1:]
        table = [[f"Team{i+1}", j] for i,j in enumerate(total)]

        for team in table:
            embed.add_field(name=team[0], value=team[1], inline=False)

        await ctx.send(embed=embed)


    @commands.command(name="pounce")
    async def pounce(self, ctx, question : int, answer : str):
        #Getting Team Number
        roles = ctx.author.roles
        role = [name.name for name in roles if name.name[:5]=='team-']
        await ctx.send("Your Pounce has been noted, get ready for the negs lmao")

        #Adding Pounce to Sheet
        team_number = int(role[0][-1])

        #Authorization
        gc = self.authorize()

        #Opening SpreadSheet
        try:
            ScoreSheet = gc.open('Score Sheet')
        except gspread.exceptions.SpreadsheetNotFound:
            await ctx.send("The ScoreSheet does not exist")

        #Opening Pounce Sheet
        try:
            pounces = ScoreSheet.worksheet("Pounces")
        except gspread.exceptions.WorksheetNotFound:
            await ctx.send("Pounces sheet is unavailable")

        #Entering Pounce in the Sheet
        pounces.update_cell(team_number + 1, question + 1, answer)
        

def setup(client):
    client.add_cog(Scoresheet(client))
