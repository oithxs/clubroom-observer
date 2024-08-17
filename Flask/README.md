# REGISTER_SYSTEM

## 変更
2024/08/18:送信完了ページの文字サイズ変更（スマホへの対応のため），閉じるボタンの削除（動作不可能のため）

## pip
```pip install Flask```

```pip install scapy```

```pip install pysqlite3```

## 仕様
Linux環境で動作します．（Windows非推奨）
このプログラムを動かすときに権限が必要なので，以下のコマンドを実行する．
```sudo setcap cap_net_raw=eip $(readlink -f $(which python3))```

サーバーの起動
```python3 REGISTER_FLASK.py```
URL：http://localhost:5000/

アクセスすると登録画面が表示される．
Discordのユーザー名を入力し，送信すると，データベースにユーザーのMACアドレスとDiscordのユーザー名が記録される．