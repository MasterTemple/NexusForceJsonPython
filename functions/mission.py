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
        # if row[2] == missionData['NPCOfferComponentID'] and row[1] == 73:
        #     missionData['NPCOfferID'] = row[0]
        # if row[2] == missionData['NPCOfferComponentID'] and row[1] == 73:
        #     missionData['NPCAcceptID'] = row[0]
        if row[2] == missionData['NPCComponent']['NPCOfferComponentID'] and row[1] == 73:
            missionData['NPCOfferID'] = row[0]
        if row[2] == missionData['NPCComponent']['NPCAcceptComponentID'] and row[1] == 73:
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
    #icon_path = None
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


def getMissionStats(cur, missionID, name, conn):
    cur.execute("SELECT id, defined_type, defined_subtype, reward_currency, LegoScore, reward_reputation, isChoiceReward, reward_item1, reward_item1_count, reward_item2, reward_item2_count, reward_item3, reward_item3_count, reward_item4, reward_item4_count, isMission, repeatable, reward_maximagination, reward_maxhealth, reward_maxinventory, reward_bankinventory, reward_emote FROM Missions")
    rows = cur.fetchall()
    from externalFunctions import parseXML as missionInfo

    for row in rows:
        if row[0] == missionID:
            obj = {
                "defined_type": row[1],
                "defined_subtype": row[2],
                "reward_currency": row[3],
                "LEGOScore": row[4],
                "reward_reputation": row[5],
                "isChoiceReward": row[6],
                "rewards": {
                    "item1":{
                        "reward_item1": row[7],
                        "reward_item1_count": row[8]
                    },
                    "item2":{
                        "reward_item2": row[9],
                        "reward_item2_count": row[10]
                    },
                    "item3":{
                        "reward_item3": row[11],
                        "reward_item3_count": row[12]
                    },
                    "item4":{
                        "reward_item4": row[13],
                        "reward_item4_count": row[14]
                    },
                },
                "isMission": row[15],
                "repeatable": row[16],
                "reward_maximagination": row[17],
                "reward_maxhealth": row[18],
                "reward_maxinventory": row[19],
                "reward_bankinventory": row[20],
                "reward_emote": row[21]


            }
            if obj['rewards']['item1']["reward_item1"] != -1:
                obj['rewards']['item1'].update(name.info(conn, row[7]))
            if obj['rewards']['item2']["reward_item2"] != -1:
                obj['rewards']['item2'].update(name.info(conn, row[9]))
            if obj['rewards']['item3']["reward_item3"] != -1:
                obj['rewards']['item3'].update(name.info(conn, row[11]))
            if obj['rewards']['item4']["reward_item4"] != -1:
                obj['rewards']['item4'].update(name.info(conn, row[13]))

            import xml.etree.ElementTree as ET
            tree = ET.parse('work/locale.xml')
            root = tree.getroot()

            if row[15] == 1:
                obj['MissionText'] = missionInfo.getMissionInfo(row[0], root)
            if row[15] == 0:
                obj['MissionText'] = missionInfo.getAchievementInfo(row[0], root)

            return obj


def getMissionText(cur, data):
    pass

def fixReward(missionData):
    if missionData['MissionStats']['isMission'] == 0 and missionData['MissionStats']['isChoiceReward'] == 1:
        missionData['MissionStats']['isChoiceReward'] = 0

    return missionData

def getMissionInfo(conn, missionID):

    cur = conn.cursor()
    import externalFunctions.nameAndDisplayName as name
    missionData = {}
    missionData['MissionStats'] = getMissionStats(cur, missionID, name, conn)
    if missionData['MissionStats']['isMission'] == 1:
        missionData['NPCComponent'] = getMissionNPCComponent(cur, missionID)
        missionData = (missionNPCIDsFromComponent(cur, missionData))
        missionData['NPCAcceptName'] = name.info(conn, missionData['NPCAcceptID'])
        missionData['NPCOfferName'] = name.info(conn, missionData['NPCOfferID'])

    missionData['MissionTasks'] = missionTasksInfo(cur, missionID, name, conn, missionData)
    missionData = fixReward(missionData)

    return missionData

