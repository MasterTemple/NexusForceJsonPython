def getInfo(conn, data, skillIDs):
    data['behaviorIDs'] = []

    cur = conn.cursor()
    cur.execute("SELECT skillID, behaviorID, imaginationcost, cooldowngroup, cooldown, inNpcEditor, skillIcon, imBonusUI, lifeBonusUI, armorBonusUI FROM SkillBehavior")
    rows = cur.fetchall()
    for row in rows:
        if row[0] in skillIDs:
            data['behaviorIDs'].append(row[1])
            data['objectSkills'][row[0]]['behaviorID'] = row[1]
            data['objectSkills'][row[0]]['imaginationcost'] = row[2]
            data['objectSkills'][row[0]]['cooldowngroup'] = row[3]
            data['objectSkills'][row[0]]['cooldown'] = round(row[4], 2)
            data['objectSkills'][row[0]]['inNpcEditor'] = row[5]
            data['objectSkills'][row[0]]['skillIcon'] = row[6]
            data['objectSkills'][row[0]]['imBonusUI'] = row[7]
            data['objectSkills'][row[0]]['lifeBonusUI'] = row[8]
            data['objectSkills'][row[0]]['armorBonusUI'] = row[9]
    data = easyStats(data)
    return data


def easyStats(data):
    data['stats'] = {}
    for skill in data['objectSkills']:
        try:
            if data['objectSkills'][skill]['imBonusUI'] is not None:
                data['stats']['imBonusUI'] = data['objectSkills'][skill]['imBonusUI']
            elif data['objectSkills'][skill]['lifeBonusUI'] is not None:
                data['stats']['lifeBonusUI'] = data['objectSkills'][skill]['lifeBonusUI']
            elif data['objectSkills'][skill]['armorBonusUI'] is not None:
                data['stats']['armorBonusUI'] = data['objectSkills'][skill]['armorBonusUI']
            elif data['objectSkills'][skill]['castOnType'] == 0:
                data['stats']['cooldown'] = data['objectSkills'][skill]['cooldown']
                data['stats']['cooldowngroup'] = data['objectSkills'][skill]['cooldowngroup']
        except:
            pass
            #print(skill)
    return data

