def packageList(conn):
    cur = conn.cursor()
    cur.execute("SELECT * FROM ComponentsRegistry")
    rows = cur.fetchall()
    array = []
    data = {}
    obj = {}
    data['LootMatrixIndexes'] = []
    for row in rows:
        if row[0] not in array and row[1] == 53:
            array.append(row[2])
            obj[row[2]] = row[0]

    cur.execute("SELECT * FROM PackageComponent")
    rows = cur.fetchall()
    for row in rows:
        if row[0]  in array:
            data['LootMatrixIndexes'].append(row[1])
            data[row[1]] =  obj[row[0]]
    return data

