import sys
sys.path.append("/usr/src/app")
from my_module import operate_sqlite3 as sql
sql.delete_db()
sql.create_DB()

sql.add_user("CC:E1:D5:79:29:24", "takahashi4510")
#sql.add_user("0C:9D:92:CD:A1:22", "佐藤さん")
#sql.add_user("58:56:9F:9F:23:5B", "内藤さん")
sql.add_user("BC:24:11:32:F4:1E", "鈴木さん")
sql.add_user("23:FB:32:BD:AD:DA", "小林さん")

sql.list_tables_and_contents()