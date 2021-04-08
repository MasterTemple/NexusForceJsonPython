def getObjects(conn):
    cur = conn.cursor()
    cur.execute("SELECT id, name, type, displayName FROM Objects")
    rows = cur.fetchall()
    array = []
    for row in rows:
        if row[0] not in array:
            array.append({
                "id": row[0],
                "name": row[1],
                "type": row[2],
                "displayName": row[3]
            })
    return array


def getItems(conn):
    cur = conn.cursor()
    cur.execute("SELECT id, name, type, displayName FROM Objects")
    rows = cur.fetchall()
    array = []
    for row in rows:
        if row[0] not in array and (row[2] == 'Loot'):
            array.append({
                "id": row[0],
                "name": row[1],
                "type": row[2],
                "displayName": row[3]
            })
    return array

def getNPCs(conn):
    cur = conn.cursor()
    cur.execute("SELECT id, name, type, displayName FROM Objects")
    rows = cur.fetchall()
    array = []
    for row in rows:
        if row[0] not in array and (row[2] == 'UserGeneratedNPCs' or row[2] == 'NPC'):
            array.append({
                "id": row[0],
                "name": row[1],
                "type": row[2],
                "displayName": row[3]
            })
    return array

def getBricks(conn):
    cur = conn.cursor()
    cur.execute("SELECT id, name, type, displayName FROM Objects")
    rows = cur.fetchall()
    array = []
    for row in rows:
        if row[0] not in array and (row[2] == 'LEGO brick'):
            array.append({
                "id": row[0],
                "name": row[1],
                "type": row[2],
                "displayName": row[3]
            })
    return array


def getMissions(conn):
    cur = conn.cursor()
    cur.execute("SELECT id, defined_type, defined_subtype FROM Missions")
    rows = cur.fetchall()
    array = []
    import xml.etree.ElementTree as ET
    #tree = ET.parse('./../work/locale.xml')
    tree = ET.parse('./work/locale.xml')
    import externalFunctions.parseXML as xml

    root = tree.getroot()
    for row in rows:
        missionInfo = xml.getMissionInfo(row[0], root)
        array.append({
            "id": row[0],
            "defined_type": row[1],
            "defined_subtype": row[2],
            "name": missionInfo['name'],
            "description": missionInfo['description']
        })

    return array

