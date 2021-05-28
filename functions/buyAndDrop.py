def getInfo(conn, data, objectID):
    data['buyAndDrop'] = {}
    data['buyAndDrop']['LootTableIndexes'] = []
    data['buyAndDrop']['LootMatrixIndexesArray'] = []
    data['buyAndDrop']['LootMatrixIndexes'] = {}
    data = getLTI(conn, data, objectID)
    data = getLMI(conn, data)
    data = inNPC(conn, data)
    data = getVendorComponents(conn, data)
    data = getVendorIDs(conn, data)
    data = getVendorNames(conn, data)
    data = getDestructibleComponents(conn, data)
    data = getEnemyIDs(conn, data)
    data = getEnemyNames(conn, data)

    # cur = conn.cursor()
    # cur.execute("SELECT * FROM LootTable")
    # rows = cur.fetchall()
    return data


def getLTI(conn, data, objectID):
    cur = conn.cursor()
    cur.execute("SELECT * FROM LootTable WHERE itemid=?", (objectID,))
    rows = cur.fetchall()

    for row in rows:
        data['buyAndDrop']['LootTableIndexes'].append(row[1])

    return data


def getLMI(conn, data):
    cur = conn.cursor()
    cur.execute("SELECT * FROM LootMatrix WHERE LootTableIndex IN ("+ ",".join(["?" for _ in data['buyAndDrop']['LootTableIndexes']]) + ")", data['buyAndDrop']['LootTableIndexes'])
    rows = cur.fetchall()
    for row in rows:

        data['buyAndDrop']['LootMatrixIndexesArray'].append(row[0])
        obj = {
            "LootMatrixIndex": row[0],
            "LootTableIndex": row[1],
            "RarityTableIndex": row[2],
            "percent": round(row[3] * 100, 2),
            "minToDrop": row[4],
            "maxToDrop": row[5],
            "DestructibleComponent": {}
        }
        data['buyAndDrop']['LootMatrixIndexes'][row[0]] = obj
        data['buyAndDrop']['LootMatrixIndexes'][row[0]]['rarityTableInfo'] = {}
        data = rarityTable(conn, data, row[0], row[2])
        # data['buyAndDrop']['LootMatrixIndexes'].append(obj)

    return data


def inNPC(conn, data):
    cur = conn.cursor()
    cur.execute("SELECT * FROM LootMatrixIndex WHERE LootMatrixIndex IN ("+",".join(["?" for _ in data['buyAndDrop']['LootMatrixIndexesArray']])+")", data['buyAndDrop']['LootMatrixIndexesArray'])
    rows = cur.fetchall()
    for row in rows:
        data['buyAndDrop']['LootMatrixIndexes'][row[0]]['inNpcEditor'] = row[1]

    return data


def getVendorComponents(conn, data):
    cur = conn.cursor()
    data['buyAndDrop']['VendorComponents'] = []
    cur.execute("SELECT id, LootMatrixIndex FROM VendorComponent WHERE LootMatrixIndex IN ("+ ",".join(["?" for _ in data['buyAndDrop']['LootMatrixIndexesArray']]) + ")", data['buyAndDrop']['LootMatrixIndexesArray'])
    rows = cur.fetchall()
    for row in rows:
        data['buyAndDrop']['VendorComponents'].append(row[0])

    return data


def getVendorIDs(conn, data):
    cur = conn.cursor()
    data['buyAndDrop']['VendorIDs'] = []
    cur.execute("SELECT * FROM ComponentsRegistry WHERE component_id IN ("+ ",".join(["?" for _ in data['buyAndDrop']['VendorComponents']]) + ") AND component_type=16", data['buyAndDrop']['VendorComponents'])
    rows = cur.fetchall()
    for row in rows:
        data['buyAndDrop']['VendorIDs'].append(row[0])

    return data


def getVendorNames(conn, data):
    cur = conn.cursor()
    data['buyAndDrop']['Vendors'] = []
    cur.execute("SELECT id, name, displayName FROM Objects WHERE id IN ("+ ",".join(["?" for _ in data['buyAndDrop']['VendorIDs']]) + ")", data['buyAndDrop']['VendorIDs'])
    rows = cur.fetchall()
    for row in rows:
        obj = {
            "id": row[0],
            "name": row[1],
            "displayName": row[2]
        }
        data['buyAndDrop']['Vendors'].append(obj)
    return data


def getDestructibleComponents(conn, data):
    import json
    with open('work/config.json') as f:
        config = json.load(f)
    with open(config['path']+'/search/implementedEnemies.json') as f:
        enemiesFile = json.load(f)
    implementedEnemies = enemiesFile['used']
    #packages = [13102]
    cur = conn.cursor()
    data['buyAndDrop']['DestructibleComponents'] = []
    cur.execute("SELECT id, LootMatrixIndex FROM DestructibleComponent WHERE LootMatrixIndex IN ("+ ",".join(["?" for _ in data['buyAndDrop']['LootMatrixIndexesArray']]) + ")", data['buyAndDrop']['LootMatrixIndexesArray'])
    rows = cur.fetchall()
    for row in rows:
        data['buyAndDrop']['DestructibleComponents'].append(row[0])
        #print(row[1], row[0])
        #if row[1] not in data['buyAndDrop']['LootMatrixIndexes'][row[1]]['DestructibleComponent']:
        #if row[1] not in data['buyAndDrop']['LootMatrixIndexes'][row[1]]['DestructibleComponent']:
        enemyID = getOneEnemyID(conn, data, row[0])
        #print(enemyID)

        if enemyID in implementedEnemies:
            data['buyAndDrop']['LootMatrixIndexes'][row[1]]['DestructibleComponent'][row[0]] = {
                "enemyID": enemyID,
                "enemyNames": getOneEnemyName(conn, data, enemyID)
            }
        #data['buyAndDrop']['LootMatrixIndexes'][row[1]]['DestructibleComponent']['enemyNames'] = getOneEnemyName(conn, data, data['buyAndDrop']['LootMatrixIndexes'][row[1]]['DestructibleComponent']['enemyID'])
        #if True:
           # data['buyAndDrop']['LootMatrixIndexes'][row[1]]['DestructibleComponent']['comp_val'] = (row[0])
           # data['buyAndDrop']['LootMatrixIndexes'][row[1]]['DestructibleComponent']['enemyID'] = getOneEnemyID(conn, data, row[0])
           # data['buyAndDrop']['LootMatrixIndexes'][row[1]]['DestructibleComponent']['enemyNames'] = getOneEnemyName(conn, data, data['buyAndDrop']['LootMatrixIndexes'][row[1]]['DestructibleComponent']['enemyID'])
    return data


def getEnemyIDs(conn, data):
    import json
    with open('work/config.json') as f:
        config = json.load(f)
    with open(config['path']+'/search/implementedEnemies.json') as f:
        enemiesFile = json.load(f)
    implementedEnemies = enemiesFile['used']
    #import json
    with open('work/config.json') as f:
        config = json.load(f)
    with open(config['path']+'/search/implementedEnemies.json') as f:
        enemiesFile = json.load(f)
    implementedEnemies = enemiesFile['used']
    cur = conn.cursor()
    data['buyAndDrop']['EnemyIDs'] = []

    implementedEnemies = [str(x) for x in implementedEnemies]

    implementedEnemiesString = ",".join(implementedEnemies)
    dCompsArray = [str(x) for x in data['buyAndDrop']['DestructibleComponents']]
    componentsString = ",".join(dCompsArray)

    query = f"SELECT * FROM ComponentsRegistry WHERE component_type=7 and component_id IN ({componentsString}) AND id IN ({implementedEnemiesString})"
    cur.execute(query)

    # cur.execute("SELECT * FROM ComponentsRegistry WHERE component_type=7 AND component_id IN ("+ ",".join(["?" for _ in data['buyAndDrop']['DestructibleComponents']]) + ") AND id IN ("+ ",".join(["?" for _ in implementedEnemies]) + ")", (data['buyAndDrop']['DestructibleComponents'], implementedEnemies))
    rows = cur.fetchall()
    for row in rows:
        #if row[2] in data['buyAndDrop']['DestructibleComponents'] and row[1] == 7 and row[0] in implementedEnemies:
        data['buyAndDrop']['EnemyIDs'].append(row[0])

    return data


def getEnemyNames(conn, data):
    cur = conn.cursor()
    data['buyAndDrop']['Enemies'] = []
    cur.execute("SELECT id, name, displayName FROM Objects WHERE id IN ("+ ",".join(["?" for _ in data['buyAndDrop']['EnemyIDs']]) + ")", data['buyAndDrop']['EnemyIDs'])
    rows = cur.fetchall()
    for row in rows:
        #if row[0] in data['buyAndDrop']['EnemyIDs']:
        obj = {
            "id": row[0],
            "name": row[1],
            "displayName": row[2]
        }
        data['buyAndDrop']['Enemies'].append(obj)
    return data


def getOneEnemyID(conn, data, dComp):
    import json
    with open('work/config.json') as f:
        config = json.load(f)
    with open(config['path']+'/search/implementedEnemies.json') as f:
        enemiesFile = json.load(f)
    implementedEnemies = enemiesFile['used']

    cur = conn.cursor()
    data['buyAndDrop']['EnemyIDs'] = []
    # cur.execute("SELECT * FROM ComponentsRegistry WHERE component_type=7 AND component_id=? AND id IN ("+ ",".join(["?" for _ in implementedEnemies]) + ")", (dComp, implementedEnemies))
    implementedEnemies = [str(x) for x in implementedEnemies]

    joinedString = ",".join(implementedEnemies)
    query = f"SELECT * FROM ComponentsRegistry WHERE component_type=7 and component_id={dComp} AND id IN ({joinedString})"
    cur.execute(query)

    # query = f"SELECT * FROM ComponentsRegistry WHERE component_type=7 and component_id={dComp} AND id IN ({','.join(['?' for _ in implementedEnemies])})"
    # cur.execute(query, (implementedEnemies,))

    row = cur.fetchone()
    if row is not None:
        return row[0]
    # print(row)
    #if row[2] == dComp and row[1] == 7 and row[0] in implementedEnemies:
        #data['buyAndDrop']['EnemyIDs'].append(row[0])
    # return row[0]

        #return data



def getOneEnemyName(conn, data, objectID):
    cur = conn.cursor()
    data['buyAndDrop']['Enemies'] = []
    cur.execute("SELECT id, name, displayName FROM Objects WHERE id=?", (objectID,))
    row = cur.fetchone()
        # if row[0] == objectID:
    obj = {
        "name": row[1],
        "displayName": row[2]
    }
    return obj


def rarityTable(conn, data, lmi, rti):
    cur = conn.cursor()
    cur.execute("SELECT * FROM RarityTable WHERE RarityTableIndex=?", (rti,))
    rows = cur.fetchall()
    for row in rows:
        #if row[3] == rti:
        obj = {
            "id": row[0],
            "randmax": round(row[1] * 100, 2),
            "rarity": row[2]
        }
        #print(rti)
        #print(data['buyAndDrop']['LootMatrixIndexes'])
        data['buyAndDrop']['LootMatrixIndexes'][lmi]['rarityTableInfo'][row[2]] = obj

        import json
        with open('work/config.json') as f:
            config = json.load(f)
        with open(config['path']+'/lootTableIndexes/'+str(data['buyAndDrop']['LootMatrixIndexes'][lmi]['LootTableIndex'])+'.json') as f:
            rarityCount = json.load(f)

        data['buyAndDrop']['LootMatrixIndexes'][lmi]['rarityCount'] = rarityCount['rarityCount']

        # data['buyAndDrop']['LootMatrixIndexes'].append(obj)

    return data
