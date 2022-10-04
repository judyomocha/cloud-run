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

scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
parsed = json.loads(GCP_SA_KEY)
gc = gspread.service_account_from_dict(parsed)
wb = gc.open_by_key(SPREADSHEET_KEY)
ws = wb.sheet1

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)


@client.event
async def on_message(message):  # メッセージを受け取ったときの挙動
    if message.author.bot:  # Botのメッセージは除く
        return
    print(message.content)
    worksheet_list = wb.worksheets()
    #　1つ目のシートのセル(1,1)をDiscordに送ったメッセージ内容で更新
    worksheet_list[0].update_cell(1, 1, message.content)
    await message.channel.send('更新しました')

client.run(TOKEN)
