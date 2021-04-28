def rarityTable(conn, data, lti, rti):
    cur = conn.cursor()
    cur.execute("SELECT * FROM RarityTable")
    rows = cur.fetchall()
    data['rarityTableInfo'] = {}
    import json
    with open('work/config.json') as f:
        config = json.load(f)
    with open(config['path']+'/lootTableIndexes/'+str(lti)+'.json') as f:
        rarityCount = json.load(f)
    #print("LTI:",lti,"RTI:",rti)

    for row in rows:
        if row[3] == rti:
            obj = {
                "id": row[0],
                "randmax": round(row[1] * 100, 2),
                "rarity": row[2]
            }
            #print(obj)
            data['rarityTableInfo'][row[2]] = obj
            #print(rti)
            #print(data['drop']['LootTableIndexes'])
            # data['rarityTableInfo'][row[2]] = obj
            #


            data['rarityCount'] = rarityCount['rarityCount']

            #data['drop']['LootTableIndexes'][data['LootTableIndex']].append(obj)

    return data

def getInfo(conn, activityID):
    data = {"id": activityID}
    getActivityRewards(conn, activityID, data)
    #return data
    for activity in data['activities']:
        #data['LootMatrixIndex'] = getLMI(conn, data['comp_val'])
        #data['activities'][activity]['LootMatrixIndexInfo'] = {}
        getLTIFromLMI(conn, data['activities'][activity])
        lootTableIndexRange(data['activities'][activity])
        editLootTableIndexes(data['activities'][activity])
        #return data

        #rarityTable(conn, data, lmi, rti)
        for lmi in data['activities'][activity]['LootTableIndexes']:
            #print(lmi)
            rarityTable(conn, lmi, lmi['LootTableIndex'], lmi['RarityTableIndex'])
            rarityTableInfoPercents(lmi)
            weightedChance(data['activities'][activity])
    #rarityTable(conn, lmi, data['drop']['LootMatrixIndex'], lmi['RarityTableIndex'])
    # rarityTableInfoPercents(data['LootMatrixIndex'])
    # weightedChance(data)

    return data


def lootTableIndexRange(data):
    import json
    for lti in data['LootTableIndexes']:
        #print(lti['LootTableIndex'])
        #num = str(data['drop']['LootTableIndexes'][lti]['LootTableIndex'])
        #print(num)
        with open('work/config.json') as f:
            config = json.load(f)
        with open(config['path']+'/lootTableIndexes/' + str(lti['LootTableIndex']) + '.json') as f:
            ltiFile = json.load(f)
        lti['size'] = len(ltiFile['itemsList'])

    return data

def editLootTableIndexes(data):
    import json
    with open('work/LootTableIndexNames.json') as f:
        names = json.load(f)
    for lti in data['LootTableIndexes']:
        lti['names'] = names['data'][lti['LootTableIndex']]
    return data


def getLMI(conn, comp_val):
    cur = conn.cursor()
    cur.execute("SELECT id, LootMatrixIndex FROM PackageComponent")
    rows = cur.fetchall()
    for row in rows:
        if row[0] == comp_val:
            return row[1]


def getActivityRewards(conn, activityID, data):
    data['activityRatings'] = {}
    data['activities'] = {}

    cur = conn.cursor()
    cur.execute("SELECT * FROM ActivityRewards")
    rows = cur.fetchall()
    for row in rows:
        if row[0] == activityID:
            activity_id = str(row[6])[len(row[6])-1:]
            data['activityRatings'][activity_id] = row[2]

            data['activities'][row[6]] = {
                "LootMatrixIndex": row[3],
                "CurrencyIndex": row[4],
                "activityRating": row[2]
            }

    return data

def getLTIFromLMI(conn, data):
    cur = conn.cursor()
    cur.execute("SELECT * FROM LootMatrix")
    rows = cur.fetchall()
    data['LootTableIndexes'] = []
    for row in rows:
        if row[0] == data['LootMatrixIndex']:
            obj = {
                "LootTableIndex": row[1],
                "RarityTableIndex": row[2],
                "percent": round(row[3] * 100, 2),
                "minToDrop": row[4],
                "maxToDrop": row[5],
            }
            data['LootTableIndexes'].append(obj)

    return data


def rarityTableInfoPercents(data):
    #print(data)
    #return data
    #print(data)
    #for lmi in data:
    #print('lmi'+str(lmi))
    arr = []
    for rtinfo in data['rarityTableInfo']:
        arr.append(rtinfo)

    arr.sort()
    #print(arr)
    #return data
    #data['rarityTableInfo'].sort()
    #print(lmi, arr)

    for index in arr:
        #print(arr[len(arr)-index])
        #chance = data['rarityTableInfo'][str(arr[len(arr)-index])]['randmax'] - data['rarityTableInfo'][str(arr[len(arr)-(index+1)])]['randmax']
        if index <= len(arr)-1:
            chance = data['rarityTableInfo'][arr[len(arr)-index]]['randmax'] - data['rarityTableInfo'][arr[len(arr)-index-1]]['randmax']
            #print(chance)
            data['rarityTableInfo'][arr[len(arr)-index]]['chance'] = chance
            #data['rarityTableInfo'][arr[len(arr)-index]]['chance'] = data['rarityTableInfo'][arr[len(arr)-index]]['randmax'] - data['rarityTableInfo'][arr[len(arr)-index-1]]['randmax']
        elif len(arr) != 1:
            chance = data['rarityTableInfo'][arr[len(arr)-index]]['randmax']
            #print(chance)
            #print(arr[len(arr)-index])
            data['rarityTableInfo'][arr[len(arr)-index]]['chance'] = chance
            #data['rarityTableInfo'][arr[len(arr)-index]]['chance'] = data['rarityTableInfo'][arr[len(arr)-index]]['randmax']
        elif len(arr) == 1:
            chance = data['rarityTableInfo'][arr[0]]['randmax']
            #print(chance)
            #print(arr[len(arr)-index])
            data['rarityTableInfo'][arr[0]]['chance'] = chance

    return data



def weightedChance(data):

    for lti in data['LootTableIndexes']:
        try:
            if lti['rarityTableInfo'] is not None:
                total = 0
                for rti in lti['rarityTableInfo']:
                    #print(lti['rarityTableInfo'][rti]['chance'])
                    #print(lti['rarityCount'][str(rti)])
                    if lti['rarityCount'][str(rti)] != 0:
                        total+= lti['rarityTableInfo'][rti]['chance']
                # print(rti['chance'])

                for rti in lti['rarityTableInfo']:
                    if total != 0:
                        #print(lti['rarityTableInfo'][rti]['chance'], round((100/total)*lti['rarityTableInfo'][rti]['chance'], 2))
                        lti['rarityTableInfo'][rti]['weightedChance'] = round((100/total)*lti['rarityTableInfo'][rti]['chance'], 2)
                        lti['rarityTableInfo'][rti]['weightedChance'] = lti['rarityTableInfo'][rti]['chance']
                        total = 100
                    if lti['rarityCount'][str(rti)] != 0:
                        lti['rarityTableInfo'][rti]['weightedChanceForSpecificItem'] = round(((100/total)*(lti['rarityTableInfo'][rti]['chance']/100))/lti['rarityCount'][str(rti)], 6)
                        lti['rarityTableInfo'][rti]['weightedChanceForAnyItemIncludingDrop'] = round( (lti['percent']/100)*((100/total)*(lti['rarityTableInfo'][rti]['chance']/100)), 6)
                        lti['rarityTableInfo'][rti]['weightedChanceForSpecificItemIncludingDrop'] = round( (lti['percent']/100)*((100/total)*(lti['rarityTableInfo'][rti]['chance']/100))/lti['rarityCount'][str(rti)], 6)
                        lti['rarityTableInfo'][rti]['howManyToKillForSpecific'] = round(100/lti['percent']) * round(100/lti['rarityTableInfo'][rti]['chance']) * lti['rarityCount'][str(rti)]
                        lti['rarityTableInfo'][rti]['howManyToKillForAny'] = round(100/lti['percent']) * round(100/lti['rarityTableInfo'][rti]['chance'])

                if lti['rarityCount'][str(rti)] == 0:
                    #print('ran', lti['LootTableIndex'])
                    lti['rarityTableInfo'][rti]['weightedChance'] = 0
                    lti['rarityTableInfo'][rti]['weightedChanceForSpecificItem'] = 0

                lti['total'] = total
                #print(total)

        #print(lti['rarityTableInfo'])
        except:
            pass

    return data


def bigCalculate(data):
    #import math
    rarityVal = (data['itemComponent']['rarity'])

    for lmi in data['drop']['LootTableIndexes']:
        # try:
        #rarityVal = str(rarityVal)
        #if len(data['DestructibleComponent']) > 0:
        if rarityVal in data['rarityTableInfo'].keys():

            #if rarityVal in data['rarityTableInfo'] and rarityVal in data['rarityCount']:
            #print('yep')
            #print(data['DestructibleComponent']['enemyNames']['displayName'])
            chanceVal = data['rarityTableInfo'][(rarityVal)]['chance']
            chanceArr = []
            chanceSum = 0
            #print(rarityVal)
            for bigChance in data['rarityTableInfo']:
                #print(bigChance)
                if data['rarityCount'][str(bigChance)] != 0:
                    chanceArr.append(data['rarityTableInfo'][(bigChance)]['chance'])
                    chanceSum+=data['rarityTableInfo'][(bigChance)]['chance']

            #print(chanceSum)
            chanceVal = chanceVal * (100.0/chanceSum)
            percentVal = data['percent']
            totalItems = data['rarityCount'][str(rarityVal)]
            percent = round((percentVal/100.0) * (chanceVal/100.0) * (1.0/totalItems), 6)
            howManyToKill = round(1.0/percent)
            data['weightedChance'] = {
                "percent": percent,
                "howManyToKill": howManyToKill
            }
            #print(data['weightedChance'])
        # except:
        #     continue

    return data


def totalWishingWell(data):
    totalActivity = {}
    totalActivity['LootTableIndexesList'] = []
    totalActivity['LootTableIndexes'] = []

    usedLTIS = []
    for activity in data['activities']:
        name = activity
        activity_id = name[len(name)-1:]
        print(activity_id)
        #print(activity)
        for LootTable in data['activities'][activity]['LootTableIndexes']:
            if LootTable['LootTableIndex'] not in usedLTIS:
                totalActivity['LootTableIndexesList'].append(LootTable['LootTableIndex'])
                totalActivity['LootTableIndexes'].append(LootTable)
                usedLTIS.append(LootTable['LootTableIndex'])

                for rarityID in totalActivity['LootTableIndexes'][len(totalActivity['LootTableIndexes'])-1]['rarityTableInfo'].keys():
                    # print(rarityID)
                    # print(totalActivity['LootTableIndexes'][len(totalActivity['LootTableIndexes'])-1]['rarityTableInfo'][rarityID])

                    try:
                        pa = totalActivity['LootTableIndexes'][len(totalActivity['LootTableIndexes'])-1]['rarityTableInfo'][rarityID]['weightedChanceForAnyItemIncludingDrop']
                    except KeyError:
                        pa = 0
                    try:
                        ps = totalActivity['LootTableIndexes'][len(totalActivity['LootTableIndexes'])-1]['rarityTableInfo'][rarityID]['weightedChanceForSpecificItemIncludingDrop']
                    except KeyError:
                        ps = 0
                    try:
                        fs = totalActivity['LootTableIndexes'][len(totalActivity['LootTableIndexes'])-1]['rarityTableInfo'][rarityID]['howManyToKillForSpecific']
                    except KeyError:
                        fs = 0
                    try:
                        fa = totalActivity['LootTableIndexes'][len(totalActivity['LootTableIndexes'])-1]['rarityTableInfo'][rarityID]['howManyToKillForAny']
                    except KeyError:
                        fa = 0
                    totalActivity['LootTableIndexes'][len(totalActivity['LootTableIndexes'])-1]['rarityTableInfo'][rarityID]['weightedChanceForAnyItemIncludingDrop'] = pa
                    totalActivity['LootTableIndexes'][len(totalActivity['LootTableIndexes'])-1]['rarityTableInfo'][rarityID]['weightedChanceForSpecificItemIncludingDrop'] = ps
                    totalActivity['LootTableIndexes'][len(totalActivity['LootTableIndexes'])-1]['rarityTableInfo'][rarityID]['howManyToKillForSpecific'] = fs
                    totalActivity['LootTableIndexes'][len(totalActivity['LootTableIndexes'])-1]['rarityTableInfo'][rarityID]['howManyToKillForAny'] = fa

            else:
                pass
                # for
                # for rarityID in totalActivity['LootTableIndexes'][len(totalActivity['LootTableIndexes'])-1]['rarityTableInfo'].keys():
                #     # print(rarityID)
                #     # print(totalActivity['LootTableIndexes'][len(totalActivity['LootTableIndexes'])-1]['rarityTableInfo'][rarityID])
                #
                #     try:
                #         pa = totalActivity['LootTableIndexes'][len(totalActivity['LootTableIndexes'])-1]['rarityTableInfo'][rarityID]['weightedChanceForAnyItemIncludingDrop']
                #     except KeyError:
                #         pa = 0
                #     try:
                #         ps = totalActivity['LootTableIndexes'][len(totalActivity['LootTableIndexes'])-1]['rarityTableInfo'][rarityID]['weightedChanceForSpecificItemIncludingDrop']
                #     except KeyError:
                #         ps = 0
                #     try:
                #         fs = totalActivity['LootTableIndexes'][len(totalActivity['LootTableIndexes'])-1]['rarityTableInfo'][rarityID]['howManyToKillForSpecific']
                #     except KeyError:
                #         fs = 0
                #     try:
                #         fa = totalActivity['LootTableIndexes'][len(totalActivity['LootTableIndexes'])-1]['rarityTableInfo'][rarityID]['howManyToKillForAny']
                #     except KeyError:
                #         fa = 0
                #     totalActivity['LootTableIndexes'][len(totalActivity['LootTableIndexes'])-1]['rarityTableInfo'][rarityID]['weightedChanceForAnyItemIncludingDrop'].append(pa)
                #     totalActivity['LootTableIndexes'][len(totalActivity['LootTableIndexes'])-1]['rarityTableInfo'][rarityID]['weightedChanceForSpecificItemIncludingDrop'].append(ps)
                #     totalActivity['LootTableIndexes'][len(totalActivity['LootTableIndexes'])-1]['rarityTableInfo'][rarityID]['howManyToKillForSpecific'].append(fs)
                #     totalActivity['LootTableIndexes'][len(totalActivity['LootTableIndexes'])-1]['rarityTableInfo'][rarityID]['howManyToKillForAny'].append(fa)


    # for activity in data['activities']:
    #     print(activity)
    #     for LootTable in data['activities'][activity]['LootTableIndexes']:
    #         print(LootTable)

    name = name[:len(name)-1] + "Total"
    data['activities'][name] = totalActivity
    return data


def totalWishingWellKey(data):
    totalActivity = {}
    totalActivity['LootTableIndexesList'] = []
    totalActivity['LootTableIndexes'] = []
    totalActivity['LootTables'] = {}
    activityChanceByID = {
        "1": 500,
        "2": 250,
        "3": 150,
        "4": 50,
        "5": 25,
        "6": 23,
        "7": 2,
        "8": 1,
    }

    usedLTIS = []
    for activity in data['activities']:
        name = activity
        activity_id = name[len(name)-1:]
        #print(activity_id)
        #print(activity)
        for LootTable in data['activities'][activity]['LootTableIndexes']:
            if LootTable['LootTableIndex'] not in totalActivity['LootTables'].keys():
                totalActivity['LootTables'][LootTable['LootTableIndex']] = {}
                totalActivity['LootTables'][LootTable['LootTableIndex']][activity_id] = LootTable
            elif LootTable['LootTableIndex'] in totalActivity['LootTables'].keys():
                totalActivity['LootTables'][LootTable['LootTableIndex']][activity_id] = LootTable
                pass


        # if LootTable['LootTableIndex'] not in usedLTIS:
            #     totalActivity['LootTableIndexesList'].append(LootTable['LootTableIndex'])
            #     totalActivity['LootTableIndexes'].append(LootTable)
            #     usedLTIS.append(LootTable['LootTableIndex'])
            #
            #     for rarityID in totalActivity['LootTableIndexes'][len(totalActivity['LootTableIndexes'])-1]['rarityTableInfo'].keys():
            #         # print(rarityID)
            #         # print(totalActivity['LootTableIndexes'][len(totalActivity['LootTableIndexes'])-1]['rarityTableInfo'][rarityID])
            #
            #         try:
            #             pa = totalActivity['LootTableIndexes'][len(totalActivity['LootTableIndexes'])-1]['rarityTableInfo'][rarityID]['weightedChanceForAnyItemIncludingDrop']
            #         except KeyError:
            #             pa = 0
            #         try:
            #             ps = totalActivity['LootTableIndexes'][len(totalActivity['LootTableIndexes'])-1]['rarityTableInfo'][rarityID]['weightedChanceForSpecificItemIncludingDrop']
            #         except KeyError:
            #             ps = 0
            #         try:
            #             fs = totalActivity['LootTableIndexes'][len(totalActivity['LootTableIndexes'])-1]['rarityTableInfo'][rarityID]['howManyToKillForSpecific']
            #         except KeyError:
            #             fs = 0
            #         try:
            #             fa = totalActivity['LootTableIndexes'][len(totalActivity['LootTableIndexes'])-1]['rarityTableInfo'][rarityID]['howManyToKillForAny']
            #         except KeyError:
            #             fa = 0
            #         totalActivity['LootTableIndexes'][len(totalActivity['LootTableIndexes'])-1]['rarityTableInfo'][rarityID]['weightedChanceForAnyItemIncludingDrop'] = pa
            #         totalActivity['LootTableIndexes'][len(totalActivity['LootTableIndexes'])-1]['rarityTableInfo'][rarityID]['weightedChanceForSpecificItemIncludingDrop'] = ps
            #         totalActivity['LootTableIndexes'][len(totalActivity['LootTableIndexes'])-1]['rarityTableInfo'][rarityID]['howManyToKillForSpecific'] = fs
            #         totalActivity['LootTableIndexes'][len(totalActivity['LootTableIndexes'])-1]['rarityTableInfo'][rarityID]['howManyToKillForAny'] = fa
            #
            # else:
            #     pass
                # for
                # for rarityID in totalActivity['LootTableIndexes'][len(totalActivity['LootTableIndexes'])-1]['rarityTableInfo'].keys():
                #     # print(rarityID)
                #     # print(totalActivity['LootTableIndexes'][len(totalActivity['LootTableIndexes'])-1]['rarityTableInfo'][rarityID])
                #
                #     try:
                #         pa = totalActivity['LootTableIndexes'][len(totalActivity['LootTableIndexes'])-1]['rarityTableInfo'][rarityID]['weightedChanceForAnyItemIncludingDrop']
                #     except KeyError:
                #         pa = 0
                #     try:
                #         ps = totalActivity['LootTableIndexes'][len(totalActivity['LootTableIndexes'])-1]['rarityTableInfo'][rarityID]['weightedChanceForSpecificItemIncludingDrop']
                #     except KeyError:
                #         ps = 0
                #     try:
                #         fs = totalActivity['LootTableIndexes'][len(totalActivity['LootTableIndexes'])-1]['rarityTableInfo'][rarityID]['howManyToKillForSpecific']
                #     except KeyError:
                #         fs = 0
                #     try:
                #         fa = totalActivity['LootTableIndexes'][len(totalActivity['LootTableIndexes'])-1]['rarityTableInfo'][rarityID]['howManyToKillForAny']
                #     except KeyError:
                #         fa = 0
                #     totalActivity['LootTableIndexes'][len(totalActivity['LootTableIndexes'])-1]['rarityTableInfo'][rarityID]['weightedChanceForAnyItemIncludingDrop'].append(pa)
                #     totalActivity['LootTableIndexes'][len(totalActivity['LootTableIndexes'])-1]['rarityTableInfo'][rarityID]['weightedChanceForSpecificItemIncludingDrop'].append(ps)
                #     totalActivity['LootTableIndexes'][len(totalActivity['LootTableIndexes'])-1]['rarityTableInfo'][rarityID]['howManyToKillForSpecific'].append(fs)
                #     totalActivity['LootTableIndexes'][len(totalActivity['LootTableIndexes'])-1]['rarityTableInfo'][rarityID]['howManyToKillForAny'].append(fa)



    # for activity in data['activities']:
    #     print(activity)
    #     for LootTable in data['activities'][activity]['LootTableIndexes']:
    #         print(LootTable)

    for key in totalActivity['LootTables'].keys():
        #print(key)
        totalActivity['LootTables'][key]
        # weightedChanceForAnyItemIncludingDrop = 0
        # weightedChanceForSpecificItemIncludingDrop = 0
        # howManyToKillForSpecific = 0
        # howManyToKillForAny = 0
        #data['activities'][name[:len(name)-1]+]
        rarityTableInfo = {}
        rarityTableInfo['1'] = {
            "weightedChanceForAnyItemIncludingDrop": 0,
            "weightedChanceForSpecificItemIncludingDrop": 0,
            "howManyToKillForSpecific": 0,
            "howManyToKillForAny": 0
        }
        rarityTableInfo['2'] = {
            "weightedChanceForAnyItemIncludingDrop": 0,
            "weightedChanceForSpecificItemIncludingDrop": 0,
            "howManyToKillForSpecific": 0,
            "howManyToKillForAny": 0
        }
        rarityTableInfo['3'] = {
            "weightedChanceForAnyItemIncludingDrop": 0,
            "weightedChanceForSpecificItemIncludingDrop": 0,
            "howManyToKillForSpecific": 0,
            "howManyToKillForAny": 0
        }
        rarityTableInfo['4'] = {
            "weightedChanceForAnyItemIncludingDrop": 0,
            "weightedChanceForSpecificItemIncludingDrop": 0,
            "howManyToKillForSpecific": 0,
            "howManyToKillForAny": 0
        }
        for subkey in totalActivity['LootTables'][key].keys():
            #print(f"-{subkey}")



            for rarity in totalActivity['LootTables'][key][subkey]['rarityTableInfo']:

                #print(f"--{rarity}")
                try:
                    # print("---", totalActivity['LootTables'][key][subkey]['rarityTableInfo'][rarity]["weightedChanceForAnyItemIncludingDrop"])
                    rarityTableInfo[str(rarity)]['weightedChanceForAnyItemIncludingDrop'] += (totalActivity['LootTables'][key][subkey]['rarityTableInfo'][rarity]["weightedChanceForAnyItemIncludingDrop"] * (activityChanceByID[subkey])/1000 )
                except KeyError:
                    pass
                try:
                    # print("---", totalActivity['LootTables'][key][subkey]['rarityTableInfo'][rarity]["weightedChanceForSpecificItemIncludingDrop"])
                    rarityTableInfo[str(rarity)]['weightedChanceForSpecificItemIncludingDrop'] += (totalActivity['LootTables'][key][subkey]['rarityTableInfo'][rarity]["weightedChanceForSpecificItemIncludingDrop"] * (activityChanceByID[subkey])/1000 )
                except KeyError:
                    pass
                try:
                    # print("---", totalActivity['LootTables'][key][subkey]['rarityTableInfo'][rarity]["howManyToKillForSpecific"])
                    rarityTableInfo[str(rarity)]['howManyToKillForSpecific'] += (totalActivity['LootTables'][key][subkey]['rarityTableInfo'][rarity]["howManyToKillForSpecific"] * (activityChanceByID[subkey])/1000 )
                except KeyError:
                    pass
                try:
                    # print("---", totalActivity['LootTables'][key][subkey]['rarityTableInfo'][rarity]["howManyToKillForAny"])
                    rarityTableInfo[str(rarity)]['howManyToKillForAny'] += (totalActivity['LootTables'][key][subkey]['rarityTableInfo'][rarity]["howManyToKillForAny"] * (activityChanceByID[subkey])/1000 )
                except KeyError:
                    pass


            LootTableIndex = totalActivity['LootTables'][key][subkey]['LootTableIndex']
            RarityTableIndex = totalActivity['LootTables'][key][subkey]['RarityTableIndex']
            percent = totalActivity['LootTables'][key][subkey]['percent']
            minToDrop = totalActivity['LootTables'][key][subkey]['minToDrop']
            maxToDrop = totalActivity['LootTables'][key][subkey]['maxToDrop']
            size = totalActivity['LootTables'][key][subkey]['size']
            names = totalActivity['LootTables'][key][subkey]['names']

        obj = {
            "LootTableIndex": LootTableIndex,
            "RarityTableIndex": RarityTableIndex,
            "percent": percent,
            "minToDrop": minToDrop,
            "maxToDrop": maxToDrop,
            "size": size,
            "names": names,
            "rarityTableInfo": rarityTableInfo
        }
        totalActivity['LootTableIndexes'].append(obj)

    name = name[:len(name)-1] + "Total"
    data['activities'][name] = totalActivity
    return data
