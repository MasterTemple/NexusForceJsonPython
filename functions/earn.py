def getInfo(conn, data, objectID):

    data['earn'] = {}

    cur = conn.cursor()
    #    cur.execute("SELECT id, defined_type, defined_subtype, isChoiceReward, reward_item1, reward_item1_count, reward_item2, reward_item2_count, reward_item3, reward_item3_count, reward_item4, reward_item4_count FROM ComponentsRegistry")
    cur.execute("SELECT id, defined_type, defined_subtype, isChoiceReward, reward_item1, reward_item1_count, reward_item2, reward_item2_count, reward_item3, reward_item3_count, reward_item4, reward_item4_count, isMission FROM Missions")

    rows = cur.fetchall()

    for row in rows:
        if row[4] == objectID or row[6] == objectID or row[8] == objectID or row[10] == objectID:
            data['earn'][row[0]] = {
                "defined_type": row[1],
                "defined_subtype": row[2],
                "missionName": "CURRENTLY NOT IMPLEMENTED",
                "missionDescription": "CURRENTLY NOT IMPLEMENTED",
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

    return data

