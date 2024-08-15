import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import asyncio
#環境変数の用意
load_dotenv() # .envファイルの読み込み
TOKEN = os.getenv("TOKEN")
GUILD_ID = int(os.getenv("GUILD_ID"))
ROLE_ID = int(os.getenv("ROLE_ID"))

# BotのプレフィックスとIntentsを設定
intents = discord.Intents.default()
intents.members = True
client = discord.Client(intents=intents)

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
        print(f"REMOVE_ROLE>>{individual}")
        await individual.remove_roles(role)

    while True:
        try:
            #入室
            with open("enter.txt","r+") as f:
                enter = f.readlines()
                f.truncate(0) #ファイルサイズを0にする
            for username in enter:
                username = username.strip() #空白文字を消す
                for individual in mes:
                    #print(individual.name)
                    if(individual.name==username):
                        role = guild.get_role(ROLE_ID)
                        print(f"ADD_ROLE>>{username}")
                        await individual.add_roles(role)
            
            #退室
            with open("leave.txt","r+") as f:
                enter = f.readlines()
                f.truncate(0) #ファイルサイズを0にする
            for username in enter:
                username = username.strip() #空白文字を消す
                for individual in mes:
                    #print(individual.name)
                    if(individual.name==username):
                        role = guild.get_role(ROLE_ID)
                        print(f"REMOVE_ROLE>>{username}")
                        await individual.remove_roles(role)
                
            
            print("CHECK")
            #time.sleep(60)
            await asyncio.sleep(60)
          
        except Exception as e:
            print(f"error:{e}")
    
# Botを起動
client.run(TOKEN)
