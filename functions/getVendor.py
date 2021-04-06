def getInfo(conn, npcData, comp_id):

    cur = conn.cursor()
    cur.execute("SELECT id, LootMatrixIndex FROM VendorComponent")
    rows = cur.fetchall()

    for row in rows:
        if row[0] == comp_id:
            npcData['LootMatrixIndex'] = row[1]
            break


    getLTIs(cur, npcData)
    getLTIInfo(npcData)
    return npcData


def getLTIs(cur, npcData):
    cur.execute("SELECT LootMatrixIndex, LootTableIndex FROM LootMatrix")
    rows = cur.fetchall()
    npcData['LootTableIndexes'] = []
    for row in rows:
        if row[0] == npcData['LootMatrixIndex']:
            npcData['LootTableIndexes'].append(row[1])

    return npcData

def getLTIInfo(npcData):
    import json
    npcData['LootTables'] = {}
    npcData['totalItemsSold'] = 0
    for ltis in npcData['LootTableIndexes']:
        with open('work/config.json') as f:
            config = json.load(f)
        with open(config['path']+'/lootTableIndexes/'+str(ltis)+'.json') as f:
            lti = json.load(f)
        npcData['LootTables'][ltis] = {
            "sells": len(lti['items']),
            "items": lti['items']
        }
        npcData['totalItemsSold'] += len(lti['items'])
    return npcData
