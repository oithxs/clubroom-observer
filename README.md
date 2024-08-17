# clubroom-observer

### 開発時に
クローンした時に
```
docker compose build
```
Dockerの起動
```
sh dockUp {入りたいコンテナ名[mac,bot,form]の3種類}
```
mac　赤色のbash
bot　紫色のbash
form　橙色のbash
ブラウザから[ローカルの7900](http://localhost:7900/)でseleniumの画面を確認できる[接続]からパスワードは"secret"

実行する時は
```
sh start.sh
```
getMac.pyをバックで起動し、Discord.pyをフロントで起動する

### 環境変数を書き込み
- SELENIUM_URL
- TABLE_URL
- TABLE_PASS
- TOKEN
- GUILD_ID
- CHANNEL_ID
- ROLE_ID