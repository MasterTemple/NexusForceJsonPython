def info(conn, objectID):
    cur = conn.cursor()
    cur.execute("SELECT id, name, displayName FROM Objects")
    rows = cur.fetchall()
    for row in rows:
        if row[0] == objectID:
            obj = {
                "name": row[1],
                "displayName": row[2]
            }
            break
    return obj
