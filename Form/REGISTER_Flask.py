from flask import Flask, request, render_template, url_for
import sqlite3
from scapy.all import ARP, Ether, srp
import os
from dotenv import load_dotenv
from authlib.integrations.flask_client import OAuth

app = Flask(__name__)

#SQLLiteデータベース関連の情報
# USERTABLE.dbを作成する
# すでに存在していれば、それにアクセスする。
load_dotenv()
dbname = os.getenv("USER_DB")
app.secret_key = os.getenv("FLASK_SECRET_KEY", "dev-secret")

# OAuth 設定（Discord）
oauth = OAuth(app)
DISCORD_CLIENT_ID = os.getenv("DISCORD_CLIENT_ID")
DISCORD_CLIENT_SECRET = os.getenv("DISCORD_CLIENT_SECRET")

oauth.register(
    name="discord",
    client_id=DISCORD_CLIENT_ID,
    client_secret=DISCORD_CLIENT_SECRET,
    access_token_url="https://discord.com/api/oauth2/token",
    authorize_url="https://discord.com/api/oauth2/authorize",
    api_base_url="https://discord.com/api/",
    client_kwargs={"scope": "identify"},
)

#MACアドレスがデータベースに存在するかどうかをTuleかFalseで返す。
def Check_Mac_address(mac):
    conn = sqlite3.connect(dbname)
    cur = conn.cursor()

    cur.execute("SELECT COUNT(*) FROM userdata WHERE MAC_ADDRESS = ?",(mac,))
    result = cur.fetchone()[0]
    
    conn.close()

    if result>0:
        return True
    else:
        return False       

#MACアドレスに変換
def IPtoMACAddress(IPAddress):
    # ARPリクエストパケットを作成
    arp = ARP(pdst=IPAddress)
    ether = Ether(dst="ff:ff:ff:ff:ff:ff")
    packet = ether/arp
    
    # ARPリクエストを送信し、レスポンスを受信
    result = srp(packet, timeout=2, verbose=False)[0]
    
    # レスポンスからMACアドレスを抽出
    for sent, received in result:
        return received.hwsrc
    
    return None

#書き込み
def db_insert(DiscordUserID,MACAddress):
    conn = sqlite3.connect(dbname)
    # sqliteを操作するカーソルオブジェクトを作成
    cur = conn.cursor()
    cur.execute("INSERT INTO userdata(MAC_ADDRESS,discord_user_ID) values(?, ?);", (MACAddress,DiscordUserID))
    # データベースへコミット。これで変更が反映される。
    conn.commit()
    # データベースへのコネクションを閉じる。(必須)
    conn.close()

#Topページ
@app.route("/")
def top():
    return render_template("index.html")


# Discord OAuth にリダイレクトしてログインさせる
@app.route("/login")
def login():
    redirect_uri = url_for("callback", _external=True)
    return oauth.discord.authorize_redirect(redirect_uri)


# OAuth コールバック
@app.route("/callback")
def callback():
    token = oauth.discord.authorize_access_token()
    if token is None:
        return render_template("error.html", error="OAuth トークンが取得できませんでした")

    resp = oauth.discord.get("users/@me")
    user = resp.json()
    # Discord の表示名 (ユーザ名#discriminator) とIDを用意
    display_name = user.get("username")
    discrim = user.get("discriminator")
    if discrim:
        display_name = f"{display_name}#{discrim}"

    discord_id = user.get("id")

    # クライアントIPとMAC取得、DB登録
    IPAddress = request.remote_addr
    MACAddress = IPtoMACAddress(IPAddress)
    if MACAddress:
        MACAddress = MACAddress.upper()
    else:
        return render_template("error.html", error="MACアドレスの取得に失敗しました.")

    if Check_Mac_address(MACAddress):
        return render_template("error.html", error="すでに登録されています.")

    # DBにはDiscordのIDを保存（表示は表示名を渡す）
    db_insert(discord_id, MACAddress)
    return render_template("store.html", DisUsName=display_name)

if __name__ == '__main__':
    print("REGISTER_SERVER_RUNNING")
    #app.debug = True
    app.run(host="0.0.0.0",port=5000)