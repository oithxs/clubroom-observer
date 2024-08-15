# clubroom-observer

# DiscordBot.py
====================

## 各ファイルについて
enter.txt:入室ユーザーID
leave.txt:退出ユーザーID
ClubRecoder.db:入退出履歴
※envファイルで，DiscordBotのトークン，ギルドID，チャンネルID,ロールIDを指定してください．

## DiscordBot.pyを動かすときに追加で必要なライブラリ
このプログラムを動かすために必要なライブラリなので，インストールしてください．
```pip install python-dotenv```
```pip install discord.py```
```pip install pysqlite3```
```pip install pytz```

## 仕様
```python3 DiscordBot0814.py```
起動時に，Discordチャンネルに所属する全ユーザーに対して入室のロールを削除します．
enter.txtに書き込まれているユーザに入室のロールを付与します．
leave.txtに書き込まれているユーザーから入室のロールを削除します．
入退出の履歴は，ClubRecoder.dbに記録されます．
入退室状況の更新は，概ね1分に１回行われます．

## 推奨動作環境
Python3.9.13
