def getInfo(conn, data, objectID):
    data = getProxy(conn, data, objectID)

    for skillID in data['proxySkillIDs']:
        data = getProxySkillBehavior(conn, data, skillID)

    return data

def getProxy(conn, data, objectID):
    data['proxySkillIDs'] = []
    data['proxySkills'] = {}
    cur = conn.cursor()
    cur.execute("SELECT * FROM ObjectSkills")
    rows = cur.fetchall()
    if data['itemComponent']['subItems'] is not None:
        #print('YES')
        #print(data['itemComponent']['subItems'])
        for row in rows:
            if row[0] in data['itemComponent']['subItems']:
                data['proxySkillIDs'].append(row[1])
                obj = {
                    "castOnType": row[2],
                    "AICombatWeight": row[3],
                }
                data['proxySkills'][row[1]] = obj
            #else:
                #print(row[0], data['itemComponent']['subItems'])
    return data


def getProxySkillBehavior(conn, data, skillID):
    cur = conn.cursor()
    cur.execute("SELECT skillID, behaviorID, imaginationcost, cooldowngroup, cooldown, inNpcEditor, skillIcon, imBonusUI, lifeBonusUI, armorBonusUI FROM SkillBehavior")

    rows = cur.fetchall()

    for row in rows:
        if row[0] == skillID:
            data['behaviorIDs'].append(row[1])
            data['proxySkills'][row[0]]['behaviorID'] = row[1]
            data['proxySkills'][row[0]]['imaginationcost'] = row[2]
            data['proxySkills'][row[0]]['cooldowngroup'] = row[3]
            data['proxySkills'][row[0]]['cooldown'] = round(row[4], 2)
            data['proxySkills'][row[0]]['inNpcEditor'] = row[5]
            data['proxySkills'][row[0]]['skillIcon'] = row[6]
            data['proxySkills'][row[0]]['imBonusUI'] = row[7]
            data['proxySkills'][row[0]]['lifeBonusUI'] = row[8]
            data['proxySkills'][row[0]]['armorBonusUI'] = row[9]

    return data



def addProxyEquipLocation(data, cur):
    cur.execute("SELECT id, equipLocation FROM ItemComponent")
    rows = cur.fetchall()
    #print(data['itemComponent']['subItems'])
    for row in rows:
        if row[0] in data['itemComponent']['subItems']:
            #print(row)
            data['itemComponent']['equipLocation'].append(row[1])
    return data
