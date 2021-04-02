import sqlite3
import json

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

import functions.getComponents as comp

file = "cdclient.sqlite"
objectID = 7570
db = create_connection(file)
objectData = comp.select_all_tasks(db, objectID)
print(objectData)

with open('output/'+str(objectID)+'.json', 'w', encoding='utf-8') as f:
    json.dump(objectData, f, ensure_ascii=False, indent=4)



