def getInfo(conn, levels):
    data = {}
    cur = conn.cursor()
    cur.execute("SELECT id, requiredUScore FROM LevelProgressionLookUp")
    rows = cur.fetchall()

    for row in rows:
        data[row[0]] = {
            "requiredUScore": row[1]
        }

    for obj in data:
        #print(obj)
        if obj != 1:
            data[obj]['fromPreviousLevel'] = data[obj]['requiredUScore'] - data[obj-1]['requiredUScore']
        else:
            data[obj]['fromPreviousLevel'] = 0


        if obj != len(data):
            data[obj]['toNextLevel'] = data[obj+1]['requiredUScore'] - data[obj]['requiredUScore']
        else:
            data[obj]['toNextLevel'] = 0



    return data
