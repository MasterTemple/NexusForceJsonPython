def length(conn):
    cur = conn.cursor()
    cur.execute("SELECT id FROM Missions")
    rows = cur.fetchall()
    array = []
    for row in rows:
        if row[0] not in array:
            array.append(row[0])
    return array
