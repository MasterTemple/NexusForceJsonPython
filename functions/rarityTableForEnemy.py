def rarityTable(conn, data, lmi, rti):
    cur = conn.cursor()
    cur.execute("SELECT * FROM RarityTable")
    rows = cur.fetchall()
    data['rarityTableInfo'] = {}
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
            import json
            with open('work/config.json') as f:
                config = json.load(f)
            with open(config['path']+'/lootTableIndexes/'+str(data['LootTableIndex'])+'.json') as f:
                rarityCount = json.load(f)

            data['rarityCount'] = rarityCount['rarityCount']

            #data['drop']['LootTableIndexes'][data['LootTableIndex']].append(obj)

    return data

def getInfo(conn, data, enemyID):
    for lmi in data['drop']['LootTableIndexes']:
        #print(data['drop']['LootMatrixIndex'], lmi['RarityTableIndex'])
        rarityTable(conn, lmi, data['drop']['LootMatrixIndex'], lmi['RarityTableIndex'])
        rarityTableInfoPercents(lmi)
        weightedChance(data)

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

    for lti in data['drop']['LootTableIndexes']:
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
