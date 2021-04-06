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


def activityList(conn):
    cur = conn.cursor()
    cur.execute("SELECT * FROM ActivityRewards")
    rows = cur.fetchall()
    array = []
    data = {}
    obj = {}
    data['LootMatrixIndexes'] = []
    for row in rows:
        if row[3] not in array and row[3] is not None:
            array.append(row[3])
            obj[row[3]] = [row[6]]
        elif row[3] is not None:
            obj[row[3]].append(row[6])
    return {
        "info": obj,
        "list": array
    }

    # cur.execute("SELECT * FROM PackageComponent")
    # rows = cur.fetchall()
    # for row in rows:
    #     if row[0]  in array:
    #         data['LootMatrixIndexes'].append(row[1])
    #         data[row[1]] =  obj[row[0]]
    # return data
