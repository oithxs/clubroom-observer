import sys
sys.path.append("/usr/src/app")
from my_module import operate_sqlite3 as sql
# sql.delete_db()
# sql.create_DB()

# sql.add_user("16:de:ff:76:86:61", "takahashi4510")
# sql.add_user("00:93:37:5D:1C:C2", "._.dice._.")
# sql.add_user("30:03:C8:04:25:F7", "watanabem")
# sql.add_user("A6:26:65:67:64:F4", "yorry2101")
# sql.add_user("23:FB:32:BD:AD:DA", "小林さん")

sql.list_tables_and_contents()