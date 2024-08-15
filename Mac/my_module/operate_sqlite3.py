import sqlite3
import os

DATABASE="USERTABLE.db"

def create_DB():
    con=sqlite3.connect(DATABASE)
    cur=con.cursor()
    cur.execute(
        "CREATE TABLE IF NOT EXISTS userdata (MAC_ADDRESS TEXTPROMARY KEY,discord_user_ID TEXT)"
    )
    con.close()


def add_user(mac_addr,dis_user_id):
    con = sqlite3.connect(DATABASE)
    cur=con.cursor()
    cur.execute("SELECT * FROM userdata WHERE MAC_ADDRESS = ?",(mac_addr,))
    exit_dis_id=cur.fetchall()
    if exit_dis_id:
        print(f"このmacaddressは既に登録されています。\nmac : {mac_addr}\ndis : {dis_user_id}")
        return
    cur.execute("INSERT INTO userdata (MAC_ADDRESS, discord_user_ID) VALUES (?, ?)",(mac_addr,dis_user_id))
    con.commit()
    con.close()

def search_user(mac_addr):
    con=sqlite3.connect(DATABASE)
    cur=con.cursor()
    try:
        D_userdata=cur.execute("SELECT * FROM userdata WHERE MAC_ADDRESS = ?",(mac_addr,)).fetchall()
        return D_userdata[0][1]
    except IndexError:
        return None
    finally:
        con.close()




def delete_db():
    os.remove(DATABASE)


def list_tables_and_contents():
    con = sqlite3.connect(DATABASE)
    cursor = con.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    for table in tables:
        print(f"Contents of table {table[0]}:")
        cursor.execute(f"SELECT * FROM {table[0]};")
        rows = cursor.fetchall()
        for row in rows:
            print(row)
        print("\n")  # テーブル間に空行を挿入
    con.close()



if __name__ == "__main__":
    create_DB()
    add_user("xxx.xxx","XXXX")
    add_user("000.000","0000")
    data = search_user(mac_addr="000.111")
    list_tables_and_contents()
    delete_db()
    print(end="\n\n")
    print(data)
