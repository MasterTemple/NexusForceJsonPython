def getMissionNPCComponent(cur, missionID):
    from externalFunctions import parseXML as missionInfo
    #    cur.execute("SELECT id, defined_type, defined_subtype, isChoiceReward, reward_item1, reward_item1_count, reward_item2, reward_item2_count, reward_item3, reward_item3_count, reward_item4, reward_item4_count FROM ComponentsRegistry")
    cur.execute("SELECT id, missionID, offersMission, acceptsMission FROM MissionNPCComponent")

    rows = cur.fetchall()

    for row in rows:
        if row[1] == missionID:
            if row[2] == 1 and row[3] == 1:
                NPCOfferComponent = row[0]
                NPCAcceptComponent = row[0]
            if row[2] == 1 and row[3] == 0:
                NPCOfferComponent = row[0]
            if row[2] == 0 and row[3] == 1:
                NPCAcceptComponent = row[0]

    return {"NPCOfferComponentID": NPCOfferComponent, "NPCAcceptComponentID": NPCAcceptComponent}


def missionNPCIDsFromComponent(cur, missionData):
    cur.execute("SELECT id, component_type, component_id FROM ComponentsRegistry")

    rows = cur.fetchall()

    for row in rows:
        if row[2] == missionData['NPCOfferComponentID'] and row[1] == 73:
            missionData['NPCOfferID'] = row[0]
        if row[2] == missionData['NPCOfferComponentID'] and row[1] == 73:
            missionData['NPCAcceptID'] = row[0]
    return missionData


def missionTasksInfo(cur, missionID, name, conn, missionData):
    cur.execute("SELECT id, taskType, target, targetGroup, IconID FROM MissionTasks")
    rows = cur.fetchall()
    for row in rows:
        if row[0] == missionID:
            missionInfo = {
                "id": row[0],
                "taskType": row[1],
                "target": {
                    "targetID": row[2],
                    "targetNames": name.info(conn, row[2])
                },
                "targetGroup": row[3],
                "iconID": row[4],
                "iconURL": iconUrlFromID(cur, row[4], missionData)
            }

    return missionInfo


def iconUrlFromID(cur, iconID, missionData):
    cur.execute("SELECT * FROM Icons")
    rows = cur.fetchall()
    for row in rows:
        if row[0] == iconID:
            icon_path = row[1]

    if icon_path is not None:
        icon_path = icon_path.replace('DDS', 'png')
        icon_path = icon_path.replace('dds', 'png')
        icon_path = icon_path.replace("\\\\", "/")
        icon_path = icon_path.replace("\\", "/")
        icon_path = icon_path.replace(' ', "%20")
        icon_path = icon_path.lower()
        iconURL = 'https://xiphoseer.github.io/lu-res/'+icon_path[6:len(icon_path)]
    else:
        iconURL = 'https://github.com/MasterTemple/lu_bot/blob/master/src/unknown.png?raw=true'
    return iconURL


def getMissionInfo(conn, missionID):
    import xml.etree.ElementTree as ET
    tree = ET.parse('work/locale.xml')
    root = tree.getroot()
    cur = conn.cursor()
    import externalFunctions.nameAndDisplayName as name
    missionData = getMissionNPCComponent(cur, missionID)
    missionData = missionNPCIDsFromComponent(cur, missionData)
    missionData['NPCAcceptName'] = name.info(conn, missionData['NPCAcceptID'])
    missionData['NPCOfferName'] = name.info(conn, missionData['NPCOfferID'])
    missionData['MissionTasks'] = missionTasksInfo(cur, missionID, name, conn, missionData)

    return missionData
