from google.oauth2.service_account import Credentials
import gspread
import discord
import json
import os
from dotenv import load_dotenv
# .envファイルの内容を読み込見込む
load_dotenv()
TOKEN = os.environ['TOKEN']
GUILD_ID = os.environ['GUILD_ID']
CHANNEL_ID = os.environ['CHANNEL_ID']
SPREADSHEET_KEY = os.environ['SPREADSHEET_KEY']
GCP_SA_KEY = os.environ['GCP_SA_KEY']
SHEET_NAME = os.environ['SHEET_NAME']

scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
parsed = json.loads(GCP_SA_KEY)
gc = gspread.service_account_from_dict(parsed)
sh = gc.open_by_key(SPREADSHEET_KEY)
ws = sh.worksheet(SHEET_NAME)
list_of_lists = ws.get_all_values()
i = len(list_of_lists[0])

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.channel.id != int(CHANNEL_ID):
        return

    if message.channel.id == int(CHANNEL_ID):
        ws.update_cell(i+1,1,message.content )
        print(f'更新します @{message.author}!') 
        await message.channel.send(f'更新します {message.author}!') 

client.run(TOKEN)
