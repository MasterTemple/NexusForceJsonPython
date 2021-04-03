def getInfo(conn, lti):
    lootTableIndex = {}
    lootTableIndex['itemsList'] = []
    cur = conn.cursor()
    cur.execute("SELECT * FROM LootTable")

    rows = cur.fetchall()
    for row in rows:
        if row[1] == lti:
            ##print(row[0])
            lootTableIndex['itemsList'].append(row[0])

    lootTableIndex = getComps(conn, lootTableIndex)
    lootTableIndex = getRarity(conn, lootTableIndex)
    lootTableIndex = countRarity(lootTableIndex)

    import externalFunctions.nameAndDisplayName as name
    for objectID in lootTableIndex['items']:
        nameObj = name.info(conn, objectID)
        #print(nameObj)
        if len(nameObj) != 0:
            lootTableIndex['items'][objectID]['name'] = nameObj['name']
            lootTableIndex['items'][objectID]['displayName'] = nameObj['displayName']

    return lootTableIndex

def countRarity(lootTableIndex):
    lootTableIndex['rarityCount'] = {}
    lootTableIndex['rarityCount']['1'] = 0
    lootTableIndex['rarityCount']['2'] = 0
    lootTableIndex['rarityCount']['3'] = 0
    lootTableIndex['rarityCount']['4'] = 0
    lootTableIndex['rarityCount']['5'] = 0
    for objectID in lootTableIndex['items']:
        #print(lootTableIndex['items'][objectID]['rarity'])
        #print(lootTableIndex['rarityCount'][str(lootTableIndex['items'][objectID]['rarity'])])
        lootTableIndex['rarityCount'][str(lootTableIndex['items'][objectID]['rarity'])]+=1
        #print(lootTableIndex['items'][objectID]['rarity'][str(lootTableIndex['items'][objectID]['rarity'])])
    return lootTableIndex

def getRarity(conn, lootTableIndex):
    cur = conn.cursor()
    cur.execute("SELECT id, rarity FROM ItemComponent")
    rows = cur.fetchall()
    # if any(x.itemComponent == 3213 for x in lootTableIndex['items']):
    # if any(shape.get('itemComponent') == 3213 for shape in lootTableIndex['items']):
    #     print('ok')

    for row in rows:
        if row[0] in lootTableIndex['itemComponentValues']:
            #print(row[0], row[1])
            for stuff in lootTableIndex['items']:
                #print(lootTableIndex['items'][stuff]['itemComponent'], row[0])
                if lootTableIndex['items'][stuff]['itemComponent'] == row[0]:
                    lootTableIndex['items'][stuff]['rarity'] = row[1]
                    #print(stuff, row[0], row[1])

    return lootTableIndex

def getComps(conn, lootTableIndex):

    cur = conn.cursor()
    cur.execute("SELECT id, component_type, component_id FROM ComponentsRegistry")
    lootTableIndex['items'] = {}
    lootTableIndex['itemComponentValues'] = []

    rows = cur.fetchall()

    for row in rows:
        if row[0] in lootTableIndex['itemsList'] and row[1] == 11:
            lootTableIndex['itemComponentValues'].append(row[2])

            lootTableIndex['items'][row[0]] = {
                "itemComponent": row[2],
            }

    return lootTableIndex
