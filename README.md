# clubroom-observer

### クローン後に
```
docker compose build
sh dockUp bot
// プロンプトが紫色になれば成功
sh setup.sh
```
※Linux想定
Windowsの場合は
```
docker compose build
docker compose up -d
docker compose exec bot bash
// プロンプトが紫色になれば成功
sh setup.sh
exit
// プロンプトが元の色に戻る
```
実行前に各コンテナの.envの記述を行う
### 開発時に
```
docker compose bot {コンテナ名}
```
| コンテナ名 | プロンプトの色 | 使用目的 |
| ---- | ---- | ---- |
| mac | 赤 | MACアドレスの取得 |
| bot | 紫 | DiscordBOTの起動 |
| form | 橙 | データベースの書き込み |
###### mac
[ローカル7900番](http://localhost:7900/)の[接続]からパスワードは"secret"でブラウザの動作を確認
ユーザーDBの初期化
```
python init_db
```
###### bot