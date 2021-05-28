def getInfo(conn, data, objectID):
    from externalFunctions import parseLocale as missionInfo
    import xml.etree.ElementTree as ET
    tree = ET.parse('work/locale.xml')
    root = tree.getroot()
    data['earn'] = {}

    cur = conn.cursor()
    #    cur.execute("SELECT id, defined_type, defined_subtype, isChoiceReward, reward_item1, reward_item1_count, reward_item2, reward_item2_count, reward_item3, reward_item3_count, reward_item4, reward_item4_count FROM ComponentsRegistry")
    cur.execute("SELECT id, defined_type, defined_subtype, isChoiceReward, reward_item1, reward_item1_count, reward_item2, reward_item2_count, reward_item3, reward_item3_count, reward_item4, reward_item4_count, isMission FROM Missions WHERE reward_item1=? OR reward_item2=? OR reward_item3=? OR reward_item4=?", (objectID, objectID, objectID, objectID))

    rows = cur.fetchall()

    for row in rows:
        try:
            # if row[4] == objectID or row[6] == objectID or row[8] == objectID or row[10] == objectID:
            if row[12] == 1:
                missionData = missionInfo.getMissionInfo(row[0], root)
            if row[12] == 0:
                missionData = missionInfo.getAchievementInfo(row[0], root)
            data['earn'][row[0]] = {
                "defined_type": row[1],
                "defined_subtype": row[2],
                "missionName": missionData['name'],
                "missionDescription": missionData['description'],
                "isMission": row[12]
            }

            if objectID == row[4]:
                data['earn'][row[0]]['rewardCount'] = row[5]
            if objectID == row[6]:
                data['earn'][row[0]]['rewardCount'] = row[7]
            if objectID == row[8]:
                data['earn'][row[0]]['rewardCount'] = row[9]
            if objectID == row[10]:
                data['earn'][row[0]]['rewardCount'] = row[11]
        except:
            pass
    return data

