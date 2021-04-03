import sqlite3
import json
import math

import functions.getComponents as getComps
import functions.itemComponent as itemComp
import functions.objects as objectInfo
import functions.getObjectSkills as objectSkills
import functions.getBehaviors as behaviors
import functions.pretty as pretty
import functions.renderComponent as render
import functions.buyAndDrop as buy
import functions.earn as earn
import functions.proxy as proxy


def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except:
        print("Error")
    return conn

def writeFile(objectID, objectData):
    with open('output/'+str(math.floor(objectID/256))+'/'+str(objectID)+'.json', 'w', encoding='utf-8') as f:
        json.dump(objectData, f, ensure_ascii=False, indent=4)

file = "cdclient.sqlite"
db = create_connection(file)

def run(objectID):
    objectData = objectInfo.getInfo(db, objectID)
    objectData = getComps.getInfo(db, objectData, objectID)
    objectData = objectSkills.getInfo(db, objectData, objectID)
    objectData = behaviors.getInfo(db, objectData, objectData['skillIDs'])
    objectData = itemComp.getInfo(db, objectData, objectData['components'][11])
    objectData = render.getInfo(db, objectData, objectData['components'][2])
    objectData = buy.getInfo(db, objectData, objectID)
    objectData = earn.getInfo(db, objectData, objectID)
    objectData = proxy.getInfo(db, objectData, objectID)

    objectData = pretty.makePretty(db, objectData)
    writeFile(objectID, objectData)


objectIDsList = [7415, 1889, 12637]
for objectID in objectIDsList:
    run(objectID)



