def getInfo(conn, data, objectID):
    data['drop'] = {
        "DestructibleComponent": data['components'][7]
    }
    data['drop']['LootMatrixIndex'] = {}
    data['drop']['LootTableIndexes'] = []

    getLMIfromDC(conn, data)
    getLTIFromLMI(conn, data)
    lootTableIndexRange(data)
    editLootTableIndexes(data)

    #data = getLTI(conn, data, objectID)
    #data = getLMI(conn, data)
    #data = getDestructibleComponents(conn, data)
    # data = getEnemyIDs(conn, data)
    # data = getEnemyNames(conn, data)

    # cur = conn.cursor()
    # cur.execute("SELECT * FROM LootTable")
    # rows = cur.fetchall()
    return data


def lootTableIndexRange(data):
    import json
    for lti in data['drop']['LootTableIndexes']:
        #print(lti['LootTableIndex'])
        #num = str(data['drop']['LootTableIndexes'][lti]['LootTableIndex'])
        #print(num)
        with open('output/lootTableIndexes/' + str(lti['LootTableIndex']) + '.json') as f:
            ltiFile = json.load(f)
        lti['size'] = len(ltiFile['itemsList'])

    return data

def editLootTableIndexes(data):
    import json
    with open('LootTableIndexNames.json') as f:
        names = json.load(f)
    for lti in data['drop']['LootTableIndexes']:
        lti['names'] = names['data'][lti['LootTableIndex']]
    return data


def rarityTable(conn, data, lmi, rti):
    cur = conn.cursor()
    cur.execute("SELECT * FROM RarityTable")
    rows = cur.fetchall()
    for row in rows:
        if row[3] == rti:
            obj = {
                "id": row[0],
                "randmax": round(row[1] * 100, 2),
                "rarity": row[2]
            }
            #print(rti)
            #print(data['drop']['LootMatrixIndexes'])
            data['drop']['LootMatrixIndexes'][lmi]['rarityTableInfo'][row[2]] = obj

            import json
            with open('output/lootTableIndexes/'+str(data['drop']['LootMatrixIndexes'][lmi]['LootTableIndex'])+'.json') as f:
                rarityCount = json.load(f)

            data['drop']['LootMatrixIndexes'][lmi]['rarityCount'] = rarityCount['rarityCount']

            # data['drop']['LootMatrixIndexes'].append(obj)

    return data

def getLMIfromDC(conn, data):
    cur = conn.cursor()
    cur.execute("SELECT id, LootMatrixIndex FROM DestructibleComponent")
    rows = cur.fetchall()
    for row in rows:
        if row[0] == data['drop']['DestructibleComponent']:
            data['drop']['LootMatrixIndex'] = row[1]
    return data


def getLTIFromLMI(conn, data):
    cur = conn.cursor()
    cur.execute("SELECT * FROM LootMatrix")
    rows = cur.fetchall()

    for row in rows:
        if row[0] == data['drop']['LootMatrixIndex']:
            obj = {
                "LootTableIndex": row[1],
                "RarityTableIndex": row[2],
                "percent": round(row[3] * 100, 2),
                "minToDrop": row[4],
                "maxToDrop": row[5],
            }
            data['drop']['LootTableIndexes'].append(obj)

    return data



def getLTI(conn, data, objectID):
    cur = conn.cursor()
    cur.execute("SELECT * FROM LootTable")
    rows = cur.fetchall()

    for row in rows:
        if row[0] == objectID:
            data['drop']['LootTableIndexes'].append(row[1])

    return data


def getLMI(conn, data):
    cur = conn.cursor()
    cur.execute("SELECT * FROM LootMatrix")
    rows = cur.fetchall()
    for row in rows:
        if row[0] in data['drop']['LootTableIndexes']:
            data['drop']['LootMatrixIndexesArray'].append(row[0])
            obj = {
                "LootMatrixIndex": row[0],
                "LootTableIndex": row[1],
                "RarityTableIndex": row[2],
                "percent": round(row[3] * 100, 2),
                "minToDrop": row[4],
                "maxToDrop": row[5],
                "DestructibleComponent": {}
            }
            data['drop']['LootMatrixIndexes'][row[0]] = obj
            data['drop']['LootMatrixIndexes'][row[0]]['rarityTableInfo'] = {}
            data = rarityTable(conn, data, row[0], row[2])
            # data['drop']['LootMatrixIndexes'].append(obj)

    return data

def getDestructibleComponents(conn, data):
    implementedEnemies = [6359, 16197, 14572,  6454,  8096,  8097, 14381,  4712, 6253,  6668,  8090,  8091,  6351,  8088,  8089, 11218, 11988, 11214, 11984, 11220, 11989, 11219, 12654, 12002, 12003, 12000, 12001, 12004, 12005, 11212, 11216, 11986, 11217, 11987, 11213, 11983, 11982, 11215, 11985, 13068, 10512,  7815,  7816,  7805, 11225, 11226,  6789,  6806, 6550, 13995, 16050, 16047, 16048, 16049, 16289, 14024, 14026, 14029, 14028, 14027, 14025, 14491, 16191, 14007, 14009, 16511, 14008, 12610, 12588, 12609, 12605, 12612, 12611, 11999, 12467, 12468, 12469, 12590, 13523, 13524, 12591, 12653, 12602, 12586, 12604, 12587, 12589, 12600, 12387, 12542,  8238,  8433]

    cur = conn.cursor()
    data['drop']['DestructibleComponents'] = []
    cur.execute("SELECT id, LootMatrixIndex FROM DestructibleComponent")
    rows = cur.fetchall()
    for row in rows:
        if row[1] in data['drop']['LootMatrixIndexesArray']:
            data['drop']['DestructibleComponents'].append(row[0])
            #print(row[1], row[0])
            #if row[1] not in data['drop']['LootMatrixIndexes'][row[1]]['DestructibleComponent']:
            #if row[1] not in data['drop']['LootMatrixIndexes'][row[1]]['DestructibleComponent']:
            enemyID = getOneEnemyID(conn, data, row[0])
            #print(enemyID)
            if enemyID in implementedEnemies:
                data['drop']['LootMatrixIndexes'][row[1]]['DestructibleComponent'][row[0]] = {
                    "enemyID": enemyID,
                    "enemyNames": getOneEnemyName(conn, data, enemyID)
                }
            #data['drop']['LootMatrixIndexes'][row[1]]['DestructibleComponent']['enemyNames'] = getOneEnemyName(conn, data, data['drop']['LootMatrixIndexes'][row[1]]['DestructibleComponent']['enemyID'])
            #if True:
            # data['drop']['LootMatrixIndexes'][row[1]]['DestructibleComponent']['comp_val'] = (row[0])
            # data['drop']['LootMatrixIndexes'][row[1]]['DestructibleComponent']['enemyID'] = getOneEnemyID(conn, data, row[0])
            # data['drop']['LootMatrixIndexes'][row[1]]['DestructibleComponent']['enemyNames'] = getOneEnemyName(conn, data, data['drop']['LootMatrixIndexes'][row[1]]['DestructibleComponent']['enemyID'])
    return data


def getEnemyIDs(conn, data):
    implementedEnemies = [6359, 16197, 14572,  6454,  8096,  8097, 14381,  4712, 6253,  6668,  8090,  8091,  6351,  8088,  8089, 11218, 11988, 11214, 11984, 11220, 11989, 11219, 12654, 12002, 12003, 12000, 12001, 12004, 12005, 11212, 11216, 11986, 11217, 11987, 11213, 11983, 11982, 11215, 11985, 13068, 10512,  7815,  7816,  7805, 11225, 11226,  6789,  6806, 6550, 13995, 16050, 16047, 16048, 16049, 16289, 14024, 14026, 14029, 14028, 14027, 14025, 14491, 16191, 14007, 14009, 16511, 14008, 12610, 12588, 12609, 12605, 12612, 12611, 11999, 12467, 12468, 12469, 12590, 13523, 13524, 12591, 12653, 12602, 12586, 12604, 12587, 12589, 12600, 12387, 12542,  8238,  8433]

    cur = conn.cursor()
    data['drop']['EnemyIDs'] = []
    cur.execute("SELECT * FROM ComponentsRegistry")
    rows = cur.fetchall()
    for row in rows:
        if row[2] in data['drop']['DestructibleComponents'] and row[1] == 7 and row[0] in implementedEnemies:
            data['drop']['EnemyIDs'].append(row[0])

    return data


def getEnemyNames(conn, data):
    cur = conn.cursor()
    data['drop']['Enemies'] = []
    cur.execute("SELECT id, name, displayName FROM Objects")
    rows = cur.fetchall()
    for row in rows:
        if row[0] in data['drop']['EnemyIDs']:
            obj = {
                "id": row[0],
                "name": row[1],
                "displayName": row[2]
            }
            data['drop']['Enemies'].append(obj)
    return data


def getOneEnemyID(conn, data, dComp):
    implementedEnemies = [6359, 16197, 14572,  6454,  8096,  8097, 14381,  4712, 6253,  6668,  8090,  8091,  6351,  8088,  8089, 11218, 11988, 11214, 11984, 11220, 11989, 11219, 12654, 12002, 12003, 12000, 12001, 12004, 12005, 11212, 11216, 11986, 11217, 11987, 11213, 11983, 11982, 11215, 11985, 13068, 10512,  7815,  7816,  7805, 11225, 11226,  6789,  6806, 6550, 13995, 16050, 16047, 16048, 16049, 16289, 14024, 14026, 14029, 14028, 14027, 14025, 14491, 16191, 14007, 14009, 16511, 14008, 12610, 12588, 12609, 12605, 12612, 12611, 11999, 12467, 12468, 12469, 12590, 13523, 13524, 12591, 12653, 12602, 12586, 12604, 12587, 12589, 12600, 12387, 12542,  8238,  8433]

    cur = conn.cursor()
    data['drop']['EnemyIDs'] = []
    cur.execute("SELECT * FROM ComponentsRegistry")
    rows = cur.fetchall()
    for row in rows:
        if row[2] == dComp and row[1] == 7 and row[0] in implementedEnemies:
            #data['drop']['EnemyIDs'].append(row[0])
            return row[0]

        #return data



def getOneEnemyName(conn, data, objectID):
    cur = conn.cursor()
    data['drop']['Enemies'] = []
    cur.execute("SELECT id, name, displayName FROM Objects")
    rows = cur.fetchall()
    for row in rows:
        if row[0] == objectID:
            obj = {
                "name": row[1],
                "displayName": row[2]
            }
            return obj


def rarityTable(conn, data, lmi, rti):
    cur = conn.cursor()
    cur.execute("SELECT * FROM RarityTable")
    rows = cur.fetchall()
    for row in rows:
        if row[3] == rti:
            obj = {
                "id": row[0],
                "randmax": round(row[1] * 100, 2),
                "rarity": row[2]
            }
            #print(rti)
            #print(data['drop']['LootMatrixIndexes'])
            data['drop']['LootMatrixIndexes'][lmi]['rarityTableInfo'][row[2]] = obj

            import json
            with open('output/lootTableIndexes/'+str(data['drop']['LootMatrixIndexes'][lmi]['LootTableIndex'])+'.json') as f:
                rarityCount = json.load(f)

            data['drop']['LootMatrixIndexes'][lmi]['rarityCount'] = rarityCount['rarityCount']

            # data['drop']['LootMatrixIndexes'].append(obj)

    return data
