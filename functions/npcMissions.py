def getInfo(conn, npcData, comp_id):
    npcData['missionsList'] = []
    cur = conn.cursor()
    cur.execute("SELECT id, missionID, offersMission FROM MissionNPCComponent")
    rows = cur.fetchall()

    for row in rows:
        if row[0] == comp_id and row[2] == 1:
            npcData['missionsList'].append(row[1])

    return npcData
