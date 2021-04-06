def length(conn):
    cur = conn.cursor()
    cur.execute("SELECT ActivityID FROM Activity")
    rows = cur.fetchall()
    array = []
    for row in rows:
        if row[0] not in array:
            array.append(row[0])
    return array
