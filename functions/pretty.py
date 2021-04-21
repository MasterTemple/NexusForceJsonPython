def makePretty(conn, data):
    cur = conn.cursor()

    if data['itemComponent']['subItems'] is not None:
        # print(data['itemComponent']['subItems'])
        #print(data['itemComponent']['subItems'])
        data = subItems(cur, data)
        # print(data['itemComponent']['subItems'])
    try:
        data = equipLocation(data)
    except:
        pass
    try:
        if data['itemComponent']['preconditions'] is not None:
            #print(data['itemComponent']['preconditions'])
            data = preconditions(cur, data)
        else:
            data['itemComponent']['levelRequirement'] = 0
    except:
        pass
    try:
        if data['itemComponent']['altCurrencyType'] is not None:
            data = altCurrencyCostName(conn, data)
        if data['itemComponent']['commendationCurrencyType'] is not None:
            data = commendationCurrencyCostName(conn, data)
    except:
        pass

    try:
        data = rarityTableInfoPercents(conn, data)
    except:
        pass
    # try:
    data = bigCalculate(data)
    # except :
    #     print('error')
    #     #data = bigCalculate(data)
    #     pass
    try:
        data = lootTableIndexRange(data)
    except:
        pass
    try:
        packageNamesForItemDrops(data, conn)
    except:
        pass
    try:
        data = removeExtra(data)
    except:
        pass
    try:
        addSkillNamesAndDescriptions(data)
    except:
        pass
    try:
        addProxySkillNamesAndDescriptions(data)
    except:
        pass
    try:
        getSkillTreeOverview(data)
    except:
        pass

    try:
        if data['itemComponent']['preconditions'] is not None:
            getPreconditions(data)
    except:
        pass
    return data


def equipLocation(data):
    data['itemComponent']['equipLocationNames'] = []
    data['itemComponent']['isWeapon'] = False

    if 'special_r' in data['itemComponent']['equipLocation']:
        data['itemComponent']['equipLocationNames'].append('Right Hand')
        data['itemComponent']['isWeapon'] = True
    if 'special_l' in data['itemComponent']['equipLocation']:
        data['itemComponent']['equipLocationNames'].append('Left Hand')
    if 'hair' in data['itemComponent']['equipLocation']:
        data['itemComponent']['equipLocationNames'].append('Headgear')
    if 'clavicle' in data['itemComponent']['equipLocation']:
        data['itemComponent']['equipLocationNames'].append('Neck/Back')
    if 'chest' in data['itemComponent']['equipLocation']:
        data['itemComponent']['equipLocationNames'].append('Torso')
    if 'legs' in data['itemComponent']['equipLocation']:
        data['itemComponent']['equipLocationNames'].append('Pants')
        # else:
        #     data['itemComponent']['equipLocationNames'].append(data['itemComponent']['equipLocation'][i])

    return data


def preconditions(cur, data):
    #print(data['itemComponent']['preconditions'])
    try:
        data['itemComponent']['preconditions'] = data['itemComponent']['preconditions'].split(';')
        data['itemComponent']['preconditions'] = [int(i) for i in data['itemComponent']['preconditions']]
        cur.execute("SELECT id, type, targetLOT FROM Preconditions")
        rows = cur.fetchall()
        for row in rows:
            if row[0] in data['itemComponent']['preconditions'] and row[1] == 22:
                data['itemComponent']['levelRequirement'] = row[2]
            elif row[0] in data['itemComponent']['preconditions']:
                continue
    except:
        pass
    return data


def subItems(cur, data):

    # print("try")
    # data['itemComponent']['subItems'] = data['itemComponent']['subItems'].split(';')
    # data['itemComponent']['subItems'] = data['itemComponent']['subItems'].replace(' ', '')
    # data['itemComponent']['subItems'] = [int(i) for i in data['itemComponent']['subItems']]
    for item in data['itemComponent']['subItems']:
        cur.execute("SELECT * FROM ComponentsRegistry")
        rows = cur.fetchall()
        for row in rows:
            if row[0] == item and row[1] == 11:
                subitemComp = row[2]
                #print(subitemComp)
                cur.execute("SELECT id, equipLocation FROM ItemComponent")
                subItemRows = cur.fetchall()
                for subItemRow in subItemRows:
                    if subItemRow[0] == subitemComp:
                        #print(subItemRow[1])
                        data['itemComponent']['equipLocation'].append(subItemRow[1])
                    #print()
    return data


def altCurrencyCostName(curr, data):
    import externalFunctions.nameAndDisplayName as name
    namesObj = name.info(curr, data['itemComponent']['altCurrencyType'])
    data['itemComponent']['altCurrencyName'] = namesObj["name"]
    data['itemComponent']['altCurrencyDisplayName'] = namesObj["displayName"]
    return data


def commendationCurrencyCostName(curr, data):
    import externalFunctions.nameAndDisplayName as name
    namesObj = name.info(curr, data['itemComponent']['commendationCurrencyType'])
    data['itemComponent']['commendationCurrencyName'] = namesObj["name"]
    # data['itemComponent']['commendationCurrencyDisplayName'] = namesObj["displayName"]
    data['itemComponent']['commendationCurrencyDisplayName'] = 'Faction Token'

    return data


def rarityTableInfoPercents(curr, data):
    #print(data)
    for lmi in data['buyAndDrop']['LootMatrixIndexes']:
        #print('lmi'+str(lmi))
        arr = []
        for rtinfo in data['buyAndDrop']['LootMatrixIndexes'][lmi]['rarityTableInfo']:
            arr.append(rtinfo)

        arr.sort()
        #data['buyAndDrop']['LootMatrixIndexes'][lmi]['rarityTableInfo'].sort()
        #print(lmi, arr)

        for index in arr:
            #print(arr[len(arr)-index])
            #chance = data['buyAndDrop']['LootMatrixIndexes'][lmi]['rarityTableInfo'][str(arr[len(arr)-index])]['randmax'] - data['buyAndDrop']['LootMatrixIndexes'][lmi]['rarityTableInfo'][str(arr[len(arr)-(index+1)])]['randmax']
            if index <= len(arr)-1:
                chance = data['buyAndDrop']['LootMatrixIndexes'][lmi]['rarityTableInfo'][arr[len(arr)-index]]['randmax'] - data['buyAndDrop']['LootMatrixIndexes'][lmi]['rarityTableInfo'][arr[len(arr)-index-1]]['randmax']
                #print(chance)
                data['buyAndDrop']['LootMatrixIndexes'][lmi]['rarityTableInfo'][arr[len(arr)-index]]['chance'] = chance
                #data['buyAndDrop']['LootMatrixIndexes'][lmi]['rarityTableInfo'][arr[len(arr)-index]]['chance'] = data['buyAndDrop']['LootMatrixIndexes'][lmi]['rarityTableInfo'][arr[len(arr)-index]]['randmax'] - data['buyAndDrop']['LootMatrixIndexes'][lmi]['rarityTableInfo'][arr[len(arr)-index-1]]['randmax']
            elif len(arr) != 1:
                chance = data['buyAndDrop']['LootMatrixIndexes'][lmi]['rarityTableInfo'][arr[len(arr)-index]]['randmax']
                #print(chance)
                #print(arr[len(arr)-index])
                data['buyAndDrop']['LootMatrixIndexes'][lmi]['rarityTableInfo'][arr[len(arr)-index]]['chance'] = chance
                #data['buyAndDrop']['LootMatrixIndexes'][lmi]['rarityTableInfo'][arr[len(arr)-index]]['chance'] = data['buyAndDrop']['LootMatrixIndexes'][lmi]['rarityTableInfo'][arr[len(arr)-index]]['randmax']
            elif len(arr) == 1:
                chance = data['buyAndDrop']['LootMatrixIndexes'][lmi]['rarityTableInfo'][arr[0]]['randmax']
                #print(chance)
                #print(arr[len(arr)-index])
                data['buyAndDrop']['LootMatrixIndexes'][lmi]['rarityTableInfo'][arr[0]]['chance'] = chance
    return data


def overallChance(data):
    #import math
    rarityVal = (data['itemComponent']['rarity'])

    for lmi in data['buyAndDrop']['LootMatrixIndexes']:
        #(lmi)
        # try:
        #rarityVal = str(rarityVal)
        #if len(data['buyAndDrop']['LootMatrixIndexes'][lmi]['DestructibleComponent']) > 0:
        if rarityVal in data['buyAndDrop']['LootMatrixIndexes'][lmi]['rarityTableInfo'].keys():

        #if rarityVal in data['buyAndDrop']['LootMatrixIndexes'][lmi]['rarityTableInfo'] and rarityVal in data['buyAndDrop']['LootMatrixIndexes'][lmi]['rarityCount']:
            #print('yep')
            #print(data['buyAndDrop']['LootMatrixIndexes'][lmi]['DestructibleComponent']['enemyNames']['displayName'])
            chanceVal = data['buyAndDrop']['LootMatrixIndexes'][lmi]['rarityTableInfo'][(rarityVal)]['chance']
            percentVal = data['buyAndDrop']['LootMatrixIndexes'][lmi]['percent']
            totalItems = data['buyAndDrop']['LootMatrixIndexes'][lmi]['rarityCount'][str(rarityVal)]
            percent = round((percentVal/100.0) * (chanceVal/100.0) * (1.0/totalItems), 6)
            howManyToKill = round(1.0/percent)
            data['buyAndDrop']['LootMatrixIndexes'][lmi]['overallChance'] = {
                "percent": percent, #not this one
                "howManyToKill": howManyToKill
            }
            #print(data['buyAndDrop']['LootMatrixIndexes'][lmi]['overallChance'])
        # except:
        #     continue

    return data


def lootTableIndexRange(data):
    import json
    for lmi in data['buyAndDrop']['LootMatrixIndexes']:
        with open('work/config.json') as f:
            config = json.load(f)
        with open(config['path']+'/lootTableIndexes/'+str(data['buyAndDrop']['LootMatrixIndexes'][lmi]['LootTableIndex'])+'.json') as f:
            lti = json.load(f)
        data['buyAndDrop']['LootMatrixIndexes'][lmi]['LootTableIndexItems'] = len(lti['items'])

    return data


def bigCalculate(data):
    #import math
    rarityVal = (data['itemComponent']['rarity'])

    for lmi in data['buyAndDrop']['LootMatrixIndexes']:
        # try:
        #rarityVal = str(rarityVal)
        #if len(data['buyAndDrop']['LootMatrixIndexes'][lmi]['DestructibleComponent']) > 0:
        if rarityVal in data['buyAndDrop']['LootMatrixIndexes'][lmi]['rarityTableInfo'].keys():

            #if rarityVal in data['buyAndDrop']['LootMatrixIndexes'][lmi]['rarityTableInfo'] and rarityVal in data['buyAndDrop']['LootMatrixIndexes'][lmi]['rarityCount']:
            #print('yep')
            #print(data['buyAndDrop']['LootMatrixIndexes'][lmi]['DestructibleComponent']['enemyNames']['displayName'])
            chanceVal = data['buyAndDrop']['LootMatrixIndexes'][lmi]['rarityTableInfo'][(rarityVal)]['chance']
            chanceArr = []
            chanceSum = 0
            #print(rarityVal)
            for bigChance in data['buyAndDrop']['LootMatrixIndexes'][lmi]['rarityTableInfo']:
                #print(bigChance)
                if data['buyAndDrop']['LootMatrixIndexes'][lmi]['rarityCount'][str(bigChance)] != 0:
                    chanceArr.append(data['buyAndDrop']['LootMatrixIndexes'][lmi]['rarityTableInfo'][(bigChance)]['chance'])
                    chanceSum+=data['buyAndDrop']['LootMatrixIndexes'][lmi]['rarityTableInfo'][(bigChance)]['chance']

            #print(chanceSum)
            chanceVal = chanceVal * (100.0/chanceSum)
            percentVal = data['buyAndDrop']['LootMatrixIndexes'][lmi]['percent']
            totalItems = data['buyAndDrop']['LootMatrixIndexes'][lmi]['rarityCount'][str(rarityVal)]
            #percent = round((percentVal/100.0) * (chanceVal/100.0) * (1.0/totalItems), 6)
            #print(percentVal/100.0)
            #print(data['buyAndDrop']['LootMatrixIndexes'][lmi]['rarityTableInfo'][(data['buyAndDrop']['LootMatrixIndexes'][lmi]['RarityTableIndex'])]['chance']/100.0)
            #print(1.0/data['buyAndDrop']['LootMatrixIndexes'][lmi]['rarityCount'][str(data['buyAndDrop']['LootMatrixIndexes'][lmi]['RarityTableIndex'])])

            percent =round((percentVal/100.0) * (data['buyAndDrop']['LootMatrixIndexes'][lmi]['rarityTableInfo'][(data['itemComponent']['rarity'])]['chance']/100.0) * (1.0/data['buyAndDrop']['LootMatrixIndexes'][lmi]['rarityCount'][str(data['itemComponent']['rarity'])]), 6)
            #print(data['buyAndDrop']['LootMatrixIndexes'][lmi]['LootTableIndex'], percentVal, chanceVal, totalItems)
            try:
                howManyToKill = round(1.0/percent)
            except ZeroDivisionError:
                howManyToKill = 0
            #print(percent)
            data['buyAndDrop']['LootMatrixIndexes'][lmi]['overallChance'] = {
                "percent": percent*100,
                "howManyToKill": howManyToKill
            }
            #print(data['buyAndDrop']['LootMatrixIndexes'][lmi]['overallChance'])

        else:
            data['buyAndDrop']['LootMatrixIndexes'][lmi]['overallChance'] = {
                "percent": 0,
                "howManyToKill": 0
            }
            pass
            #print(rarityVal)
        # except:
        #     continue

    return data


def removeUnusedLootMatrixIndexes(data):
    lmisToDelete = []
    for lmi in data['buyAndDrop']['LootMatrixIndexes']:
        #print(len(data['buyAndDrop']['LootMatrixIndexes'][lmi]['DestructibleComponent']))
        if len(data['buyAndDrop']['LootMatrixIndexes'][lmi]['DestructibleComponent']) == 0 and len(data['buyAndDrop']['LootMatrixIndexes'][lmi]['PackageComponent']) == 0 and len(data['buyAndDrop']['LootMatrixIndexes'][lmi]['ActivityComponent']) == 0:
            #delattr(data, ['buyAndDrop']['LootMatrixIndexes'][lmi])
            lmisToDelete.append(lmi)

    for lmi in lmisToDelete:
        del data['buyAndDrop']['LootMatrixIndexes'][lmi]

    return data


def removeExtra(data):
    data = removeUnusedLootMatrixIndexes(data)
    del data['buyAndDrop']['LootMatrixIndexesArray']
    del data['buyAndDrop']['DestructibleComponents']
    return data

def addSkillNamesAndDescriptions(data):
    import externalFunctions.parseXML as xml
    for skills in data['objectSkills']:
        if data['objectSkills'][skills]['castOnType'] != 1:
            skillInfo = xml.getSkillInfo(skills)
            data['objectSkills'][skills]['info'] = skillInfo
    return data

def addProxySkillNamesAndDescriptions(data):
    import externalFunctions.parseXML as xml
    for skills in data['proxySkills']:
        if data['proxySkills'][skills]['castOnType'] == 0:
            skillInfo = xml.getSkillInfo(skills)
            data['proxySkills'][skills]['info'] = skillInfo
    return data

def getPreconditions(data):
    import externalFunctions.parseXML as xml
    data['itemComponent']['preconditionDescriptions'] = xml.preconditions(data['itemComponent']['preconditions'])


def packageNamesForItemDrops(data, conn):
    # import json
    # with open('output/packageLMIs/'+str(data['buyAndDrop']['LootMatrixIndexes'][lmi]['LootTableIndex'])+'.json') as f:
    #     packageLMIs = json.load(f)
    import externalFunctions.nameAndDisplayName as name

    import json
    with open('work/config.json') as f:
        config = json.load(f)
    with open(config['path']+'/search/packageList.json') as f:
        packageData = json.load(f)
    with open(config['path']+'/search/activityList.json') as f:
        activityData = json.load(f)
    for lmi in data['buyAndDrop']['LootMatrixIndexes']:
        data['buyAndDrop']['LootMatrixIndexes'][lmi]['PackageComponent'] = {}
        data['buyAndDrop']['LootMatrixIndexes'][lmi]['ActivityComponent'] = {}

    packageLMIs = packageData['LootMatrixIndexes']
    activityLMIs = activityData['list']
    for lmi in data['buyAndDrop']['LootMatrixIndexes']:
        #print(lmi)
        if lmi in packageLMIs:
            data['buyAndDrop']['LootMatrixIndexes'][lmi]['PackageComponent'][lmi] = name.info(conn, packageData[str(lmi)])

            #print(data['buyAndDrop']['LootMatrixIndexes'][lmi]['LootMatrixIndex'])
        if lmi in activityLMIs:
            data['buyAndDrop']['LootMatrixIndexes'][lmi]['ActivityComponent'] = activityData['info'][str(lmi)]


def getSkillTreeOverview(data):
    for skill in data['objectSkills']:

        if data['objectSkills'][skill]['castOnType'] == 0:
            import json
            import math
            with open('work/config.json') as f:
                config = json.load(f)
            #print(skill, data['objectSkills'][skill])
            with open(config['path']+'/behaviors/'+str(math.floor(data['objectSkills'][skill]['behaviorID']/256))+'/'+str(data['objectSkills'][skill]['behaviorID'])+'.json') as f:
                behaviorFile = json.load(f)
            data['overview'][data['objectSkills'][skill]['behaviorID']] = behaviorFile['overview']
    try:
        for skill in data['proxySkills']:

            if data['proxySkills'][skill]['castOnType'] == 0:
                import json
                import math
                with open('work/config.json') as f:
                    config = json.load(f)
                #print(skill, data['proxySkills'][skill])
                with open(config['path']+'/behaviors/'+math.floor(data['proxySkills'][skill]['behaviorID']/256)+'/'+data['proxySkills'][skill]['behaviorID']+'.json') as f:
                    behaviorFile = json.load(f)
                data['overview'][data['proxySkills'][skill]['behaviorID']] = behaviorFile['overview']
    except:
        pass
    return data
