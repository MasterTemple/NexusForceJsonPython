def getInfo(conn, data, objectID):
    try:
        data['doesntDropAnything'] = False
        data['drop'] = {
            "DestructibleComponent": data['components'][7]
        }
        data['drop']['LootMatrixIndex'] = {}
        data['drop']['LootTableIndexes'] = []

        getLMIfromDC(conn, data)
        getLTIFromLMI(conn, data)
        lootTableIndexRange(data)
        editLootTableIndexes(data)
    except:
        data['doesntDropAnything'] = True

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
            with open('work/config.json') as f:
                config = json.load(f)
            with open(config['path']+'/lootTableIndexes/'+str(data['drop']['LootMatrixIndexes'][lmi]['LootTableIndex'])+'.json') as f:
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
    import json
    with open('work/config.json') as f:
        config = json.load(f)
    with open(config['path']+'/search/implementedEnemies.json') as f:
        enemiesFile = json.load(f)
    implementedEnemies = enemiesFile['used']

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
    import json
    with open('work/config.json') as f:
        config = json.load(f)
    with open(config['path']+'/search/implementedEnemies.json') as f:
        enemiesFile = json.load(f)
    implementedEnemies = enemiesFile['used']

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
    import json
    with open('work/config.json') as f:
        config = json.load(f)
    with open(config['path']+'/search/implementedEnemies.json') as f:
        enemiesFile = json.load(f)
    implementedEnemies = enemiesFile['used']

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
            with open('work/config.json') as f:
                config = json.load(f)
            with open(config['path']+'/lootTableIndexes/'+str(data['drop']['LootMatrixIndexes'][lmi]['LootTableIndex'])+'.json') as f:
                rarityCount = json.load(f)

            data['drop']['LootMatrixIndexes'][lmi]['rarityCount'] = rarityCount['rarityCount']

            # data['drop']['LootMatrixIndexes'].append(obj)

    return data
