from flask import Flask, request, render_template
import sqlite3
from scapy.all import ARP, Ether, srp
import os
from dotenv import load_dotenv

app = Flask(__name__)

#SQLLiteデータベース関連の情報
# USERTABLE.dbを作成する
# すでに存在していれば、それにアスセスする。
load_dotenv()
dbname = os.getenv("USER_DB")

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
def db_insert(DisUserName,MACAddress):
    conn = sqlite3.connect(dbname)
    # sqliteを操作するカーソルオブジェクトを作成
    cur = conn.cursor()
    cur.execute("INSERT INTO userdata(MAC_ADDRESS,discord_user_ID) values(?, ?);", (MACAddress,DisUserName))
    # データベースへコミット。これで変更が反映される。
    conn.commit()
    # データベースへのコネクションを閉じる。(必須)
    conn.close()

#Topページ
@app.route("/")
def top():
    return render_template("index.html")

#登録[POST]
@app.route("/store", methods=["POST"])
def result():
    
    DisUsName = request.form["DisUsName"]
    IPAddress = request.remote_addr
    MACAddress = IPtoMACAddress(IPAddress).upper()
    
    print(f"ACCESS FROM >> UserName:{DisUsName} IPAddress:{IPAddress} MACAddress:{MACAddress.upper()}")
    
    print(f"結果:{Check_Mac_address(MACAddress.upper())}")
    
    if(Check_Mac_address(MACAddress)):
        print("Already registered MAC address")
        return render_template("error.html",error="すでに登録されています.")
    elif(MACAddress==None):
        print("Failed to obtain MAC address")
        return render_template("error.html",error="MACアドレスの取得に失敗しました.")
    else:
        db_insert(DisUsName,MACAddress) #データベースへ登録
        print("REGISTER OK")
        return render_template("store.html",DisUsName=DisUsName)

if __name__ == '__main__':
    print("REGISTER_SERVER_RUNNING")
    #app.debug = True
    app.run(host="0.0.0.0",port=5000)