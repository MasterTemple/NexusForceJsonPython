import sqlite3
def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except:
        print("\nError")
    return conn

file = "work/cdclient.sqlite"
db = create_connection(file)
cur = db.cursor()
cur.execute("SELECT * FROM SkillBehavior"),
rows = cur.fetchall()
for row in rows:
    pass
