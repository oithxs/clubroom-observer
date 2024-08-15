# clubroom-observer

### 開発時に
クローンした時に
```
docker compose build
```
Dockerの起動
```
sh dockUp
```
赤色のBashが起動したら成功
※Seleniumの追加で起動に5分くらいかかる...
ブラウザから[ローカルの7900](http://localhost:7900/)でseleniumの画面を確認できる[接続]からパスワードは"secret"
実行する時は
```
python main.py
```
./Mac/.envに環境変数を書き込み
実行前にTABLE_URLとTABLE_PASSを書き入れてから

