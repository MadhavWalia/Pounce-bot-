# Pounce_Bot
To all the quizzers and quizmasters out there. This is the only bot you need to successfully conduct an online quiz. </br>
The features: </br>
-Add/Delete Roles ( Creation of roles with special permissions like QM, Scorekeeper etc.</br>
-Add/Delete Voice and Text Channels( Creation of team specific channels)</br>
-Scoresheet using Google Sheets Integration</br>
-Facts using Reddit API</br>
-Playing music from spotify/YouTube </br>

### Tech Stack:
The bot has been made using discord.py and uses API integrations.

### Commands 
---
!make : Creates channels of QM, Scorekeeper and all teams and gives them required permissions</br>
!deleteChannels : Deletes all team text channels</br>
!deleteVoice  : Deletes all team voice channels</br>
!clear{number of messages/all} : Deletes preceding messages in particular channel</br>
!message {message text} : Sends announcements to all team channels </br>
!play {song link} : Joins the vocie channel and plays relevant song</br>
!q : Shows the songs in queue</br>
!skip : Skips the next song</br>
!leave : Leaves the voice channel</br>
!give{role name, member name} : Gives particular role to particular member</br>
!removerole{role name, member name} : removes particular role from particular member </br>
!deleteAllRoles : Deletes all the team roles</br>
!trivia : Fetches fact from subreddit r/todayilearned</br>
!start{time duration} : Starts a timer for mentioned number of seconds</br>
!create{number of questions, number of teams, email of QM} : Creates a google sheet for scorekeeping of required teams</br>
!scores : fetches the scores of all the teams from Google Sheet</br>
!pounce{question number, answer} : Notes pounce of the given team provided they answer within the window</br>
!open{time duration}: Starts a timer of mentioned time duration </br>

---
