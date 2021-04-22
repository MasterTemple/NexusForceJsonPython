def getObjects(conn):
    cur = conn.cursor()
    cur.execute("SELECT id, name, type, displayName FROM Objects")
    rows = cur.fetchall()
    array = []
    for row in rows:
        if row[0] not in array:
            if row[3] is None:
                displayName = row[1]
            else:
                displayName = row[3]
            array.append({
                "id": row[0],
                "name": row[1],
                "type": row[2],
                "displayName": displayName
            })
        else:
            pass
            #print(row[0])
    return array


def getItems(conn):
    cur = conn.cursor()
    cur.execute("SELECT id, name, type, displayName FROM Objects")
    rows = cur.fetchall()
    array = []
    for row in rows:
        if row[0] not in array and (row[2] == 'Loot'):
            if row[3] is None:
                displayName = row[1]
            else:
                displayName = row[3]
            array.append({
                "id": row[0],
                "name": row[1],
                "type": row[2],
                "displayName": displayName
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


def getBricksAndItems(conn):
    cur = conn.cursor()
    cur.execute("SELECT id, name, type, displayName FROM Objects")
    rows = cur.fetchall()
    array = []
    for row in rows:
        if row[0] not in array and (row[2] == 'LEGO brick' or row[2] == 'Loot'):
            array.append({
                "id": row[0],
                "name": row[1],
                "type": row[2],
                "displayName": row[3]
            })
    return array

def getMissions(conn):
    cur = conn.cursor()
    cur.execute("SELECT id, defined_type, defined_subtype, isMission FROM Missions")
    rows = cur.fetchall()
    array = []
    import xml.etree.ElementTree as ET
    #tree = ET.parse('./../work/locale.xml')
    tree = ET.parse('./work/locale.xml')
    import externalFunctions.parseXML as xml

    root = tree.getroot()
    for row in rows:
        if row[3] == 1:
            missionInfo = xml.getMissionInfo(row[0], root)
        if row[3] == 0:
            missionInfo = xml.getAchievementInfo(row[0], root)

        subtype = row[2]
        if subtype is None:
            subtype = row[1]


        array.append({
            "id": row[0],
            "defined_type": row[1],
            "defined_subtype": subtype,
            "name": missionInfo['name'],
            "description": missionInfo['description'],
            "isMission": row[3]
        })

    return array

def getMissionLocation():
    import json
    with open('work/config.json') as f:
        config = json.load(f)
    with open(config['path']+'/references/Missions.json') as f:
        missionFile = json.load(f)

    missionData = {
        "Achievements":{},
        "Missions":{}
    }

    for mission in missionFile:
        if mission['isMission'] == 0:
            if mission['defined_type'] not in missionData.keys():
                missionData['Achievements'][mission['defined_type']] = {}

            if mission['defined_subtype'] not in missionData['Achievements'][mission['defined_type']].keys():
                missionData['Achievements'][mission['defined_type']][mission['defined_subtype']] = []

        if mission['isMission'] == 1:
            if mission['defined_type'] not in missionData.keys():
                missionData['Missions'][mission['defined_type']] = {}
            if mission['defined_subtype'] not in missionData['Missions'][mission['defined_type']].keys():
                missionData['Missions'][mission['defined_type']][mission['defined_subtype']] = []


    for mission in missionFile:

        if mission['defined_subtype'] is None:
            #print(mission['defined_subtype'])
            mission['defined_subtype'] = mission['defined_type']
            #print(mission['defined_subtype'])



        if mission['isMission'] == 0:
            missionData['Achievements'][mission['defined_type']] = {}

            missionData['Achievements'][mission['defined_type']][mission['defined_subtype']] = []

        if mission['isMission'] == 1:
            missionData['Missions'][mission['defined_type']] = {}
            missionData['Missions'][mission['defined_type']][mission['defined_subtype']] = []

    # for mission in missionFile:
    #     if mission['isMission'] == 0:
    #
    #         try:
    #             missionData['Achievements'][mission['defined_type']][mission['defined_subtype']].append({
    #                 "id": mission['id'],
    #                 "name": mission['name'],
    #                 "description": mission['description']
    #
    #             })
    #         except:
    #             missionData['Achievements'][mission['defined_type']][mission['defined_subtype']] = []
    #
    #             missionData['Achievements'][mission['defined_type']][mission['defined_subtype']].append({
    #                 "id": mission['id'],
    #                 "name": mission['name'],
    #                 "description": mission['description']
    #
    #             })
    #
    #
    #     if mission['isMission'] == 1:
    #
    #         try:
    #             missionData['Missions'][mission['defined_type']][mission['defined_subtype']].append({
    #                 "id": mission['id'],
    #                 "name": mission['name'],
    #                 "description": mission['description']
    #
    #             })
    #         except:
    #             missionData['Missions'][mission['defined_type']][mission['defined_subtype']] = []
    #             missionData['Missions'][mission['defined_type']][mission['defined_subtype']].append({
    #                 "id": mission['id'],
    #                 "name": mission['name'],
    #                 "description": mission['description']
    #
    #             })
    for mission in missionFile:
        if mission['isMission'] == 0:
            if mission['defined_subtype'] is None:
                mission['defined_subtype'] = mission['defined_type']

            #print(mission['defined_type'], mission['defined_subtype'])
            try:
                missionData['Achievements'][mission['defined_type']][mission['defined_subtype']].append({
                    "id": mission['id'],
                    "name": mission['name'],
                    "description": mission['description']

                })
            except KeyError:
                missionData['Achievements'][mission['defined_type']][mission['defined_subtype']] = []
                missionData['Achievements'][mission['defined_type']][mission['defined_subtype']].append({
                    "id": mission['id'],
                    "name": mission['name'],
                    "description": mission['description']

                })



        if mission['isMission'] == 1:

            if mission['defined_subtype'] is None:
                mission['defined_subtype'] = mission['defined_type']

            try:
                missionData['Missions'][mission['defined_type']][mission['defined_subtype']].append({
                    "id": mission['id'],
                    "name": mission['name'],
                    "description": mission['description']

                })
            except KeyError:
                missionData['Missions'][mission['defined_type']][mission['defined_subtype']] = []
                missionData['Missions'][mission['defined_type']][mission['defined_subtype']].append({
                    "id": mission['id'],
                    "name": mission['name'],
                    "description": mission['description']

                })





    return missionData


def getEnemies(conn):
    cur = conn.cursor()
    cur.execute("SELECT id, name, type, displayName FROM Objects")
    rows = cur.fetchall()
    array = []
    for row in rows:
        if row[0] not in array and (row[2] == 'Enemies'):
            if row[3] is None:
                displayName = row[1]
            else:
                displayName = row[3]
            array.append({
                "id": row[0],
                "name": row[1],
                "type": row[2],
                "displayName": displayName
            })
        else:
            pass
            #print(row[0])
    return array


def getPackages(conn):
    cur = conn.cursor()
    cur.execute("SELECT id, component_type, component_id FROM ComponentsRegistry")
    rows = cur.fetchall()
    packageIDs = []
    array = []

    for row in rows:
        if row[0] not in array and row[1] == 53:
            packageIDs.append(row[0])


    cur.execute("SELECT id, name, type, displayName FROM Objects")
    rows = cur.fetchall()
    for row in rows:
        if row[0] not in array and row[0] in packageIDs:
            array.append({
                "id": row[0],
                "name": row[1],
                "type": row[2],
                "displayName": row[3]
            })
    return array

def getKits(idList):
    data = []
    import externalFunctions.parseXML as xml
    for id in idList:
        info = xml.getKitName(id)
        data.append({
            "id": id,
            "name": info
        })
    return data
