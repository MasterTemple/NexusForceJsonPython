def makePretty(conn, data):
    cur = conn.cursor()
    if data['itemComponent']['subItems'] is not None:
        #print(data['itemComponent']['subItems'])
        data = subItems(cur, data)
    data = equipLocation(data)
    if data['itemComponent']['preconditions'] is not None:
        data = preconditions(cur, data)
    else:
        data['itemComponent']['levelRequirement'] = 0

    if data['itemComponent']['altCurrencyType'] is not None:
        data = altCurrencyCostName(conn, data)
    if data['itemComponent']['commendationCurrencyType'] is not None:
        data = commendationCurrencyCostName(conn, data)

    data = rarityTableInfoPercents(conn, data)
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
    data['itemComponent']['preconditions'] = data['itemComponent']['preconditions'].split(';')
    data['itemComponent']['preconditions'] = [int(i) for i in data['itemComponent']['preconditions']]
    cur.execute("SELECT id, type, targetLOT FROM Preconditions")
    rows = cur.fetchall()
    for row in rows:
        if row[0] in data['itemComponent']['preconditions'] and row[1] == 22:
            data['itemComponent']['levelRequirement'] = row[2]
        elif row[0] in data['itemComponent']['preconditions']:
            continue
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
