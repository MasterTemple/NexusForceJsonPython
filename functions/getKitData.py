def getInfo(conn, data, kitID):
    cur = conn.cursor()
    cur.execute("SELECT setID, itemIDs, kitType, kitRank, kitImage, skillSetWith2, skillSetWith3, skillSetWith4, skillSetWith5, skillSetWith6 FROM ItemSets"),
    rows = cur.fetchall()
    for row in rows:
        if row[0] == kitID:
            data['info'] = {
                "itemIDsString": row[1],
                "kitType": row[2],
                "kitRank": row[3],
                "kitImage": row[4],
                "skillSetWith2": row[5],
                "skillSetWith3": row[6],
                "skillSetWith4": row[7],
                "skillSetWith5": row[8],
                "skillSetWith6": row[9]
            }
            data['info']['itemIDsArray'] = getItemIDsInfo(cur, row[1], data)
            data['iconURL'] = iconUrlFromID(cur, row[4])
    data['totalWithoutValiant'] = {}
    data['totalWithValiant'] = {}
    data['bonus'] = {}
    data['bonus']['skillSetWith2'] = {}
    data['bonus']['skillSetWith3'] = {}
    data['bonus']['skillSetWith4'] = {}
    data['bonus']['skillSetWith5'] = {}
    data['bonus']['skillSetWith6'] = {}
    ranks = [1, 2, 3]
    if data['info']['kitRank'] in ranks:
        data['name'] = "Rank "+str(data['info']['kitRank'])+" "+data['name']

    data['items'] = {}
    getItemStats(data['info']['itemIDsArray'], data)
    getKitBonuses(cur, data)
    getTotalStats(data)
    for skill in data['skills']['skillSetWith2']:
            data['skills']['skillSetWith2'][skill] = skillBehavior(conn, skill)
    for skill in data['skills']['skillSetWith3']:
            data['skills']['skillSetWith3'][skill] = skillBehavior(conn, skill)
    for skill in data['skills']['skillSetWith4']:
            data['skills']['skillSetWith4'][skill] = skillBehavior(conn, skill)
    for skill in data['skills']['skillSetWith5']:
            data['skills']['skillSetWith5'][skill] = skillBehavior(conn, skill)
    for skill in data['skills']['skillSetWith6']:
            data['skills']['skillSetWith6'][skill] = skillBehavior(conn, skill)

    sumSkillStats(data)
    sumItemStats(data)
    getSkillDescriptions(data)

    #if data['info']['kitRank'] != 3:
    sumBonuses(data)

    return data

def getItemIDsInfo(cur, itemIDs, data):
    itemIDsArray = itemIDs.replace(' ', '')
    itemIDsArray = itemIDsArray.split(',')
    #getItemStats(itemIDsArray, data)
    return itemIDsArray


def getSkillDescriptions(data):
    import externalFunctions.parseLocale as xml
    data['skillSetDescriptions'] = {}
    for skillSet in data['skills']:
        for skill in data['skills'][skillSet]:
            #print(skill)
            data['skills'][skillSet][skill]['description'] = xml.getKitAbility(skill)
            if data['skills'][skillSet][skill]['imBonusUI'] == None and data['skills'][skillSet][skill]['lifeBonusUI'] == None and data['skills'][skillSet][skill]['armorBonusUI'] == None and data['skills'][skillSet][skill]['description'] != None:
                data['skillSetDescriptions'][skillSet] = data['skills'][skillSet][skill]['description']




def getKitBonuses(cur, data):
    cur.execute("SELECT * FROM ItemSetSkills")
    rows = cur.fetchall()
    data['skills'] = {}
    data['skills']['skillSetWith2'] = {}
    data['skills']['skillSetWith3'] = {}
    data['skills']['skillSetWith4'] = {}
    data['skills']['skillSetWith5'] = {}
    data['skills']['skillSetWith6'] = {}
    # data['skills']['skillSetWith2'] = {"SkillSetID": data['info']['skillSetWith2']}
    # data['skills']['skillSetWith3'] = {"SkillSetID": data['info']['skillSetWith3']}
    # data['skills']['skillSetWith4'] = {"SkillSetID": data['info']['skillSetWith4']}
    # data['skills']['skillSetWith5'] = {"SkillSetID": data['info']['skillSetWith5']}
    # data['skills']['skillSetWith6'] = {"SkillSetID": data['info']['skillSetWith6']}

    for row in rows:
        if row[0] == data['info']['skillSetWith2']:
            data['skills']['skillSetWith2'][row[1]] = {"SkillCastType": row[2]}
        if row[0] == data['info']['skillSetWith3']:
            data['skills']['skillSetWith3'][row[1]] = {"SkillCastType": row[2]}
        if row[0] == data['info']['skillSetWith4']:
            data['skills']['skillSetWith4'][row[1]] = {"SkillCastType": row[2]}
        if row[0] == data['info']['skillSetWith5']:
            data['skills']['skillSetWith5'][row[1]] = {"SkillCastType": row[2]}
        if row[0] == data['info']['skillSetWith6']:
            data['skills']['skillSetWith6'][row[1]] = {"SkillCastType": row[2]}

    return data


def getTotalStats(data):
    if data['info']['kitRank'] == 3:
        pass
    else:
        pass
    return data

def getItemStats(itemIDsArray, data):
    import json
    import math
    for itemID in itemIDsArray:
        try:
            with open('work/config.json') as f:
                config = json.load(f)
            with open(config['path']+'/objects/'+str(math.floor(int(itemID)/256))+'/'+str(itemID)+'.json') as f:
                item = json.load(f)
            data['items'][itemID] = item['stats']
            data['items'][itemID]['equipLocation'] = item['itemComponent']['equipLocation'][0]
        except:
            pass

    return data

def iconUrlFromID(cur, iconID, ):
    cur.execute("SELECT * FROM Icons")
    rows = cur.fetchall()
    icon_path = None
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
        iconURL = 'https://static.wikia.nocookie.net/legomessageboards/images/c/ce/LU2.png/revision/latest?cb=20121121213649'
    return iconURL

def skillBehavior(conn, skillID):
    obj = {}
    #obj['behaviorIDs'] = []
    cur = conn.cursor()
    cur.execute("SELECT skillID, behaviorID, imaginationcost, cooldowngroup, cooldown, inNpcEditor, skillIcon, imBonusUI, lifeBonusUI, armorBonusUI FROM SkillBehavior")
    rows = cur.fetchall()
    for row in rows:
        if row[0] == skillID:
            #obj['behaviorIDs'].append(row[1])
            obj = {}
            obj['behaviorID'] = row[1]
            obj['imaginationcost'] = row[2]
            obj['cooldowngroup'] = row[3]
            obj['cooldown'] = round(row[4], 2)
            obj['inNpcEditor'] = row[5]
            obj['skillIcon'] = row[6]
            obj['imBonusUI'] = row[7]
            obj['lifeBonusUI'] = row[8]
            obj['armorBonusUI'] = row[9]

    #obj = easyStats(obj)
    return obj


def easyStats(obj):
    data = {"skills": obj}
    data['skillsStats'] = {}
    for skill in data['skills']:
        try:
            if data['skills'][skill]['imBonusUI'] is not None:
                data['skillsStats']['imBonusUI'] = data['objectSkills'][skill]['imBonusUI']
            elif data['skills'][skill]['lifeBonusUI'] is not None:
                data['skillsStats']['lifeBonusUI'] = data['objectSkills'][skill]['lifeBonusUI']
            elif data['skills'][skill]['armorBonusUI'] is not None:
                data['skillsStats']['armorBonusUI'] = data['objectSkills'][skill]['armorBonusUI']
            elif data['skills'][skill]['castOnType'] == 0:
                data['skillsStats']['cooldown'] = data['objectSkills'][skill]['cooldown']
                data['skillsStats']['cooldowngroup'] = data['objectSkills'][skill]['cooldowngroup']
        except:
            pass
            #print(skill)
    return data

def sumSkillStats(data):
    for skill in data['skills']:
        #print(data['skills'][skill])
        for eachSkill in data['skills'][skill]:
            try:
                if data['skills'][skill][eachSkill]['imBonusUI'] is not None:
                    data['bonus'][skill]['imBonusUI'] = data['skills'][skill][eachSkill]['imBonusUI']
                elif data['skills'][skill][eachSkill]['lifeBonusUI'] is not None:
                    data['bonus'][skill]['lifeBonusUI'] = data['skills'][skill][eachSkill]['lifeBonusUI']
                elif data['skills'][skill][eachSkill]['armorBonusUI'] is not None:
                    data['bonus'][skill]['armorBonusUI'] = data['skills'][skill][eachSkill]['armorBonusUI']
                if data['skills'][skill][eachSkill]['castOnType'] == 0:
                    data['bonus'][skill]['cooldown'] = data['skills'][skill][eachSkill]['cooldown']
                    data['bonus'][skill]['cooldowngroup'] = data['skills'][skill][eachSkill]['cooldowngroup']
                    
            
            except:
                pass
            #print(skill)
    return data


def sumItemStats(data):
    for item in data['items']:
        data['bonus'][item] = {}
        try:
            if data['items'][item]['imBonusUI'] is not None:
                data['bonus'][item]['imBonusUI'] = data['items'][item]['imBonusUI']
        except:
            pass
        try:
            if data['items'][item]['lifeBonusUI'] is not None:
                data['bonus'][item]['lifeBonusUI'] = data['items'][item]['lifeBonusUI']
        except:
            pass
        try:
            if data['items'][item]['armorBonusUI'] is not None:
                #print('ok')
                data['bonus'][item]['armorBonusUI'] = data['items'][item]['armorBonusUI']
        except:
            pass
        try:
            if data['items'][item]['cooldown'] is not None:
                data['bonus'][item]['cooldown'] = data['items'][item]['cooldown']
                data['bonus'][item]['cooldowngroup'] = data['items'][item]['cooldowngroup']
        except:
            pass
            
        try:
            if data['items'][item]['equipLocation'] is not None:
                data['bonus'][item]['equipLocation'] = data['items'][item]['equipLocation']
        except:
            pass
            

    return data

def sumBonuses(data):
    firstNum = 0
    if data['info']['kitRank'] != 3 or len(data['items'].keys()) < 10:

        data['totalWithoutValiant']['imBonusUI'] = 0
        data['totalWithoutValiant']['lifeBonusUI'] = 0
        data['totalWithoutValiant']['armorBonusUI'] = 0
        for item in data['bonus']:
            try:
                if data['bonus'][item]['imBonusUI'] is not None:
                    data['totalWithoutValiant']['imBonusUI'] += data['bonus'][item]['imBonusUI']
            except:
                pass
            try:
                if data['bonus'][item]['lifeBonusUI'] is not None:
                    data['totalWithoutValiant']['lifeBonusUI'] += data['bonus'][item]['lifeBonusUI']
            except:
                pass
            try:
                if data['bonus'][item]['armorBonusUI'] is not None:
                    data['totalWithoutValiant']['armorBonusUI'] += data['bonus'][item]['armorBonusUI']
            except:
                pass
            firstNum+=1
            if data['info']['kitRank'] == 3 and firstNum == 11:
                #print(item)
                break


    else:
        data['totalWithoutValiant']['imBonusUI'] = 0
        data['totalWithoutValiant']['lifeBonusUI'] = 0
        data['totalWithoutValiant']['armorBonusUI'] = 0
        num = 0
        for item in data['bonus']:
            #item = data['bonus'][data['bonus'].indexOf(num)]
            try:
                if data['bonus'][item]['imBonusUI'] is not None:
                    data['totalWithoutValiant']['imBonusUI'] += data['bonus'][item]['imBonusUI']
            except:
                pass
            try:
                if data['bonus'][item]['lifeBonusUI'] is not None:
                    data['totalWithoutValiant']['lifeBonusUI'] += data['bonus'][item]['lifeBonusUI']
            except:
                pass
            try:
                if data['bonus'][item]['armorBonusUI'] is not None:
                    data['totalWithoutValiant']['armorBonusUI'] += data['bonus'][item]['armorBonusUI']
            except:
                pass
            num+=1
            if num == 11:
                break

        data['totalWithValiant']['imBonusUI'] = 0
        data['totalWithValiant']['lifeBonusUI'] = 0
        data['totalWithValiant']['armorBonusUI'] = 0
        
        valiantList = [0, 1, 2, 3, 4, 5, 6, 7, 10,  17, 18]
        
        
        
        valNum = 0
        ventureException = False
        for item in data['bonus']:
            #print(data['bonus'][item])
            if valNum == 9 and data['bonus'][item]['equipLocation'] == 'clavicle':
                ventureException = True

            if valNum in valiantList or ventureException:
                ventureException = False

                try:
                    if data['bonus'][item]['imBonusUI'] is not None:
                        data['totalWithValiant']['imBonusUI'] += data['bonus'][item]['imBonusUI']
                except:
                    pass
                try:
                    if data['bonus'][item]['lifeBonusUI'] is not None:
                        data['totalWithValiant']['lifeBonusUI'] += data['bonus'][item]['lifeBonusUI']
                except:
                    pass
                try:
                    if data['bonus'][item]['armorBonusUI'] is not None:
                        data['totalWithValiant']['armorBonusUI'] += data['bonus'][item]['armorBonusUI']
                except:
                    pass
            valNum+=1


    return data

