def length(conn):
    cur = conn.cursor()
    cur.execute("SELECT id, component_type FROM ComponentsRegistry")
    rows = cur.fetchall()
    array = []
    for row in rows:
        if row[0] not in array and row[1] == 53:
            array.append(row[0])
    return array
