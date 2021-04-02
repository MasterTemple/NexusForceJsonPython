def getInfo(conn, data, itemComponentID):
    #data['equipLocation'] = []
    data['itemComponent'] = {}
    cur = conn.cursor()
    cur.execute("SELECT * FROM ItemComponent")
    import math
    rows = cur.fetchall()

    for row in rows:
        if row[0] == itemComponentID:
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
            data['itemComponent']['preConditions'] = row[21]
            data['itemComponent']['isTwoHanded'] = row[26]
            data['itemComponent']['altCurrencyType'] = row[29]
            data['itemComponent']['altCurrencyCost'] = row[30]
            data['itemComponent']['subItems'] = row[31]
            data['itemComponent']['commendationCurrencyType'] = row[34]
            data['itemComponent']['commendationCurrencyCost'] = row[35]

    # data = modifyData(data, cur)
    return data

# def modifyData(data, cur):
#     factionTokens = [8318, 8319, 8320, 8321]
#     if data['itemComponent']['altCurrencyType'] != null:
#         cur.execute("SELECT * FROM Objects")
#         row = cur.findOne()
#
#     data['itemComponent']['altCurrencyName']
#
#
#     return  data
