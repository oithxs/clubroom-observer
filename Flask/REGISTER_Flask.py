from flask import Flask, request, render_template
import sqlite3

from scapy.all import ARP, Ether, srp


app = Flask(__name__)

#SQLLiteデータベース関連の情報
# USERTABLE.dbを作成する
# すでに存在していれば、それにアスセスする。
dbname = 'USERTABLE.db'

#MACアドレスに変換
#
def IPtoMAcAddress(IPAddress):
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
def db_insert(DisUserName,MACAddress):
    conn = sqlite3.connect(dbname)
    # sqliteを操作するカーソルオブジェクトを作成
    cur = conn.cursor()
    cur.execute("INSERT INTO userdata(MAC_ADDRESS,discord_user_ID) values(?, ?);", (MACAddress,DisUserName))
    # データベースへコミット。これで変更が反映される。
    conn.commit()
    # データベースへのコネクションを閉じる。(必須)
    conn.close()

@app.route("/")
def top():
    return render_template("index.html")

@app.route("/store", methods=["POST"])
def result():
    DisUsName = request.form["DisUsName"]
    IPAddress = request.remote_addr
    MACAddress = IPtoMAcAddress(IPAddress)
    print(f"STORE>> UserName:{DisUsName} IPAddress:{IPAddress} MACAddress:{MACAddress}")
    db_insert(DisUsName,MACAddress)
    return render_template("store.html",DisUsName=DisUsName)

if __name__ == '__main__':
    print("REGISTER_SERVER_RUNNING")
    app.debug = True
    app.run(host="0.0.0.0")