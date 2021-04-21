def info(conn, objectID):
    cur = conn.cursor()
    cur.execute("SELECT id, name, displayName FROM Objects")
    rows = cur.fetchall()
    obj = {}
    for row in rows:
        if row[0] == objectID:
            if row[2] == None:
                dN = row[1]
            else:
                dN = row[2]
            obj = {
                "name": row[1],
                "displayName": dN
            }
            break

    return obj
