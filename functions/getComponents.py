def getInfo(conn, data, objectID):

    data['components'] = {}

    cur = conn.cursor()
    cur.execute("SELECT id, component_type, component_id FROM ComponentsRegistry WHERE id=?", (objectID,))

    rows = cur.fetchall()

    for row in rows:
        data['components'][row[1]] = row[2]

    return data
