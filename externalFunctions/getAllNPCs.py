def length(conn):
    cur = conn.cursor()
    cur.execute("SELECT id, type FROM Objects")
    rows = cur.fetchall()
    array = []
    for row in rows:
        if row[0] not in array and (row[1] == 'UserGeneratedNPCs' or row[1] == 'NPC'):
            array.append(row[0])
    return array
