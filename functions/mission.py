def getMissionNPCComponent(conn, data):

    cur = conn.cursor()
    #    cur.execute("SELECT id, defined_type, defined_subtype, isChoiceReward, reward_item1, reward_item1_count, reward_item2, reward_item2_count, reward_item3, reward_item3_count, reward_item4, reward_item4_count FROM ComponentsRegistry")
    cur.execute("SELECT id, missionID, offersMission, acceptsMission FROM MissionsNPCComponent")

    rows = cur.fetchall()

    for row in rows:
        continue
