import enum
from tkinter.messagebox import QUESTION
import discord
from discord.ext import commands
import os
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials


curr = os.getcwd()

class Scoresheet(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.ques = 0
        self.team_no = 0

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


    @commands.Cog.listener()
    async def on_ready(self):
        print('Bot is Online')


    @commands.command(name="create")
    async def createSheet(self, ctx, questions: int, team_number: int, email: str):

        if questions>0 and team_number>0:

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
        
        else:
            await ctx.send('Team and Question Numbers cannot be negative you potato brained human')


    @commands.command(name="display")
    async def displayScores(self, ctx):
        #Authorization
        gc = self.authorize()

        #Opening SpreadSheet
        try:
            Scoresheet = gc.open('Score Sheet')
        except gspread.exceptions.SpreadsheetNotFound:
            await ctx.send("The ScoreSheet does not exist")

        #Displaying Scores
        embed = discord.Embed(
            title = "Scores",
            colour = discord.Colour.blue()
        )

        try:
            scores = Scoresheet.worksheet("Scores")
        except gspread.exceptions.WorksheetNotFound:
            await ctx.send("Scores sheets is unavailable")

        total = scores.col_values(self.ques + 2)[1:]
        table = [[f"Team{i+1}", j] for i,j in enumerate(total)]

        for team in table:
            embed.add_field(name=team[0], value=team[1], inline=False)

        await ctx.send(embed=embed)


def setup(client):
    client.add_cog(Scoresheet(client))
