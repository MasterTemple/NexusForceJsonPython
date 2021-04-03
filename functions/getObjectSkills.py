def getInfo(conn, data, objectID):
    data['skillIDs'] = []
    data['objectSkills'] = {}
    cur = conn.cursor()
    cur.execute("SELECT * FROM ObjectSkills")
    rows = cur.fetchall()

    for row in rows:
        if row[0] == objectID:
            data['skillIDs'].append(row[1])
            data['objectSkills'][row[1]] = {
                "castOnType": row[2],
                "AICombatWeight": row[3],
            }

    return data
