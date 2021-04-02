def select_all_tasks(conn, objectID):
    data = {}
    data['objectID'] = objectID
    data['components'] = {}

    cur = conn.cursor()
    cur.execute("SELECT id, component_type, component_id FROM ComponentsRegistry")

    rows = cur.fetchall()

    for row in rows:
        if row[0] == objectID:
            data['components'][row[1]] = row[2]

    return data
