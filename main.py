import sqlite3
import json
import functions.getComponents as getComps
import functions.itemComponent as itemComp
import functions.objects as objectInfo

def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by the db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except:
        print("Error")

    return conn

def writeFile(objectID):
    with open('output/'+str(objectID)+'.json', 'w', encoding='utf-8') as f:
        json.dump(objectData, f, ensure_ascii=False, indent=4)

#import functions
file = "cdclient.sqlite"
objectID = 7415
db = create_connection(file)
objectData = objectInfo.getInfo(db, objectID)
objectData = getComps.getInfo(db, objectData, objectID)
objectData = itemComp.getInfo(db, objectData, objectData['components'][11])
writeFile(objectID)



