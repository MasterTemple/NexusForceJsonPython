def getInfo(conn, data, itemComponentID):
    #data['equipLocation'] = []
    data['overview'] = {}

    # data['itemComponent'] = {}


    #data['itemComponent']['subItems'] = []
    cur = conn.cursor()
    cur.execute("SELECT * FROM ItemComponent WHERE id=?", (itemComponentID,))
    import math
    row = cur.fetchone()
    data['itemComponent']['equipLocation'] = [row[1]]
    data['itemComponent']['sellPrice'] = math.floor(row[2]/10)
    data['itemComponent']['buyPrice'] = row[2]
    data['itemComponent']['isKitPiece'] = row[3]
    data['itemComponent']['rarity'] = row[4]
    data['itemComponent']['itemComponent'] = row[6]
    data['itemComponent']['inLootTable'] = row[7]
    data['itemComponent']['inVendor'] = row[8]
    data['itemComponent']['stackSize'] = row[16]
    data['itemComponent']['color'] = row[17]
    data['itemComponent']['preconditions'] = row[21]
    data['itemComponent']['isTwoHanded'] = row[26]
    data['itemComponent']['altCurrencyType'] = row[29]
    data['itemComponent']['altCurrencyCost'] = row[30]
    data['itemComponent']['subItems'] = row[31]
    if row[31] is not None:
        #print(row[31])
        #print(data['itemComponent']['subItems'])
        # data['itemComponent']['subItems'] = data['itemComponent']['subItems'].split(';')
        # data['itemComponent']['subItems'] = data['itemComponent']['subItems'].replace(' ', '')
        try:
            data['itemComponent']['subItems'] = row[31].replace(" ", ";")
            data['itemComponent']['subItems'] = row[31].replace(",", ";")

            #data['itemComponent']['subItems'] = [i for i in data['itemComponent']['subItems'].replace(" ", "")]
            #print(data['itemComponent']['subItems'])
            try:
                data['itemComponent']['subItems'] = [int(i) for i in data['itemComponent']['subItems'].split(';')]
                #print(data['itemComponent']['subItems'])
            except:
                pass
            #print(row[31])
            #print(data['itemComponent']['subItems'])
            #data['itemComponent']['subItems'] = [i for i in data['itemComponent']['subItems'].replace(' ', '')]
            if len(data['itemComponent']['subItems']) > 1:
                #print(data['itemComponent']['subItems'])

                data['itemComponent']['subItems'] = [int(i) for i in data['itemComponent']['subItems']]
                #print(data['itemComponent']['subItems'])

             #print(row[31])
            # data = addProxy(data, cur)
        except:
            pass
            #print()
            #print(data['itemComponent']['subItems'])
    #data['itemComponent']['equipLocation'].append(int(row[31]))

    data['itemComponent']['commendationCurrencyType'] = row[34]
    data['itemComponent']['commendationCurrencyCost'] = row[35]

    # data = modifyData(data, cur)
    #print(data['itemComponent']['subItems'])

    return data

# def addProxy(data, cur):
#     cur.execute("SELECT id, equipLocation FROM ItemComponent")
#     rows = cur.fetchall()
#     print(data['itemComponent']['subItems'])
#     for row in rows:
#         if row[0] in data['itemComponent']['subItems']:
#             print(row)
#             data['itemComponent']['equipLocation'].append(row[1])
#     return data
