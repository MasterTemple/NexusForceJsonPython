def getInfo(cur, id):
    cur.execute("SELECT objectTemplate, skillID FROM ObjectSkills"),
    rows = cur.fetchall()
    #skillID = 0
    skillID = None
    for row in rows:
        if row[0] == id:
            skillID = row[1]

    return getBehaviorIDFromSkillID(cur, skillID)


def getBehaviorIDFromSkillID(cur, skillID):
    cur.execute("SELECT skillID, behaviorID FROM SkillBehavior"),
    rows = cur.fetchall()
    for row in rows:
        if row[0] == skillID:
            return row[1]
    return
