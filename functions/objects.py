def getInfo(conn, objectID):
    #data['equipLocation'] = []
    data = {}
    data['objectID'] = objectID
    data['itemInfo'] = {}
    cur = conn.cursor()
    cur.execute("SELECT id, name, type, description, displayName, _internalNotes FROM Objects")
    import math
    rows = cur.fetchall()

    for row in rows:
        if row[0] == objectID:
            data['itemInfo']['name'] = row[1]
            data['itemInfo']['displayName'] = row[4]
            data['itemInfo']['type'] = row[2]
            data['itemInfo']['description'] = row[3]
            data['itemInfo']['internalNotes'] = row[5]


    return data
