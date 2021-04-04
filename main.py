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
import functions.createLootTableIndexInfo as ltiFile
import functions.mission as missionFile
import externalFunctions.getAllLootTableIndexes as glti
import externalFunctions.getAllMission as getAllMissions
import externalFunctions.getAllObjects as getAllObjects


def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except:
        print("Error")
    return conn

def writeObjectFile(objectID, objectData):
    with open('output/objects/'+str(math.floor(objectID/256))+'/'+str(objectID)+'.json', 'w', encoding='utf-8') as f:
        json.dump(objectData, f, ensure_ascii=False, indent=4)

def writeLTIFile(objectID, objectData):
    with open('output/lootTableIndexes/'+str(objectID)+'.json', 'w', encoding='utf-8') as f:
        json.dump(objectData, f, ensure_ascii=False, indent=4)

def writeMissionFile(objectID, objectData):
    #print(objectData)
    with open('output/missions/'+str(objectID)+'.json', 'w', encoding='utf-8') as f:
        json.dump(objectData, f, ensure_ascii=False, indent=4)


file = "work/cdclient.sqlite"
db = create_connection(file)

def runObjects(objectID):
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
    writeObjectFile(objectID, objectData)

#12637, 1889

def runLTIs(lootTableIndex):
    ltiData = ltiFile.getInfo(db, lootTableIndex)
    writeLTIFile(lootTableIndex, ltiData)


def runMissions(missionID):
    missionData = missionFile.getMissionInfo(db, missionID)
    writeMissionFile(missionID, missionData)


#lootTableIndexesList = []
#lootTableIndexesList = lootTableIndexesList[lootTableIndexesList.index(752):]


lootTableIndexesList = glti.length(db)
objectIDsList = getAllObjects.length(db)
missionIDsList = getAllMissions.length(db)

lootTableIndexesList = []
objectIDsList = []
missionIDsList = [1718, 689, 792]

for lti in lootTableIndexesList:
    print('Created LootTableIndex: '+str(lti))
    runLTIs(lti)


#objectIDsList = []

for objectID in objectIDsList:
    print('Started Object:', objectID)
    runObjects(objectID)

#missionIDsList = [1718, 689, 792]

for missionID in missionIDsList:
    print('Started Mission:', missionID)
    runMissions(missionID)
