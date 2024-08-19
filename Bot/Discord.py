import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import asyncio
import sqlite3
import datetime
import pytz

#環境変数の用意
load_dotenv() # .envファイルの読み込み
TOKEN = os.getenv("TOKEN")
GUILD_ID = int(os.getenv("GUILD_ID"))
ROLE_ID = int(os.getenv("ROLE_ID"))

ENTER_URL = os.getenv("ENTER_TXT_URL")
LEAVE_URL = os.getenv("LEAVE_TXT_URL")
DB_NAME = os.getenv("LOG_DB")

# BotのプレフィックスとIntentsを設定
intents = discord.Intents.default()
intents.members = True
client = discord.Client(intents=intents)

#SQLLiteデータベース関連の情報

jst = pytz.timezone('Asia/Tokyo')

# ClubRecoder.dbを作成する
# すでに存在していれば、それにアスセスする。
# dbname = 'ClubRecoder.db'

#ログの書き込み
async def db_log_insert(name, status):
    conn = sqlite3.connect(DB_NAME)
    # sqliteを操作するカーソルオブジェクトを作成
    cur = conn.cursor()
    now = datetime.datetime.now(jst)
    str_now = now.strftime('%Y-%m-%d %H:%M:%S')
    cur.execute("INSERT INTO Log(Name, Status, Date) values(?, ?, ?);", (name, status, str_now))
    # データベースへコミット。これで変更が反映される。
    conn.commit()
    # データベースへのコネクションを閉じる。(必須)
    conn.close()

# Botの起動時に実行される処理
@client.event
async def on_ready():
    print(f'Logged in as {client.user.name}')
    guild = client.get_guild(GUILD_ID)
    mes = guild.members
    #全員にロール削除
    for individual in mes:
        #print(individual.name)
        role = guild.get_role(ROLE_ID)
        print(f"REMOVE_ROLE>>{individual.nick}")
        await individual.remove_roles(role)

    while True:
        try:
            #入室
            with open(ENTER_URL,"r+") as f:
                enter = f.readlines()
                f.truncate(0) #ファイルサイズを0にする
            for username in enter:
                username = username.strip() #空白文字を消す
                for individual in mes:
                    #print(individual.name)
                    if(individual.name==username):
                        role = guild.get_role(ROLE_ID)
                        print(f"ADD_ROLE>>{individual.nick}")
                        await db_log_insert(individual.nick,"入室")
                        await individual.add_roles(role)
            
            #退室
            with open(LEAVE_URL,"r+") as f:
                enter = f.readlines()
                f.truncate(0) #ファイルサイズを0にする
            for username in enter:
                username = username.strip() #空白文字を消す
                for individual in mes:
                    #print(individual.name)
                    if(individual.name==username):
                        role = guild.get_role(ROLE_ID)
                        print(f"REMOVE_ROLE>>{individual.nick}")
                        await db_log_insert(individual.nick,"退出")
                        await individual.remove_roles(role)
                
            
            print("CHECK")
            #time.sleep(60)
            # 本番環境は60
            await asyncio.sleep(20)
          
        except Exception as e:
            print(f"error:{e}")
    
# Botを起動
client.run(TOKEN)