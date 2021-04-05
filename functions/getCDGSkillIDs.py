def getInfo(conn, cdgID):
    data = {}
    data['cooldowngroupID'] = cdgID
    data['skillIDs'] = {}
    cur = conn.cursor()
    cur.execute("SELECT skillID, imaginationcost, cooldowngroup, cooldown FROM SkillBehavior")
    rows = cur.fetchall()

    for row in rows:
        if row[2] == cdgID:
            data['skillIDs'][row[0]] = {
                "imaginationCost": row[1],
                "cooldownTime": row[3]
            }


    import externalFunctions.nameAndDisplayName as name

    for skillID in data['skillIDs']:
        arr = getItemIDsFromSkillID(conn, skillID)
        data['skillIDs'][skillID]['items'] = {}
        for item in arr:
            data['skillIDs'][skillID]['items'][item] = {}
        for itemID in data['skillIDs'][skillID]['items']:
            #print(data['skillIDs'][skillID]['items'])
            #print(itemID)
            data['skillIDs'][skillID]['items'][itemID] = name.info(conn, itemID)
            #print(name.info(conn, itemID))

    return data

def getItemIDsFromSkillID(conn, skillID):
    cur = conn.cursor()
    cur.execute("SELECT objectTemplate, skillID FROM ObjectSkills")
    rows = cur.fetchall()
    array = []
    for row in rows:
        if row[1] == skillID:
            array.append(row[0])

    return array
