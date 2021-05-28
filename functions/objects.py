def getInfo(conn, objectID):
    #data['equipLocation'] = []
    data = {}
    data['objectID'] = objectID
    data['itemInfo'] = {}
    cur = conn.cursor()
    cur.execute("SELECT id, name, type, description, displayName, _internalNotes FROM Objects WHERE id=?", (objectID,))

    row = cur.fetchone()
    displayName = row[4]
    if displayName is None:
        displayName = row[1]
    data['itemInfo']['name'] = row[1]
    data['itemInfo']['displayName'] = displayName
    data['itemInfo']['type'] = row[2]
    data['itemInfo']['description'] = row[3]
    data['itemInfo']['internalNotes'] = row[5]


    return data
