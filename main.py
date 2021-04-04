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
import functions.getVendor as vendor
import functions.npcMissions as npcMissions
import functions.vendorPretty as vendorPretty

import externalFunctions.getAllLootTableIndexes as glti
import externalFunctions.getAllMission as getAllMissions
import externalFunctions.getAllObjects as getAllObjects
import externalFunctions.getAllNPCs as getAllNPCs


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


def writeNPCFile(objectID, objectData):
    #print(objectData)
    with open('output/npcs/'+str(math.floor(objectID/256))+'/'+str(objectID)+'.json', 'w', encoding='utf-8') as f:
        json.dump(objectData, f, ensure_ascii=False, indent=4)




def runObjects(objectID):
    objectData = objectInfo.getInfo(db, objectID)
    getComps.getInfo(db, objectData, objectID)
    objectSkills.getInfo(db, objectData, objectID)
    behaviors.getInfo(db, objectData, objectData['skillIDs'])
    itemComp.getInfo(db, objectData, objectData['components'][11])
    render.getInfo(db, objectData, objectData['components'][2])
    buy.getInfo(db, objectData, objectID)
    earn.getInfo(db, objectData, objectID)
    proxy.getInfo(db, objectData, objectID)

    pretty.makePretty(db, objectData)
    writeObjectFile(objectID, objectData)

def runLTIs(lootTableIndex):
    ltiData = ltiFile.getInfo(db, lootTableIndex)
    writeLTIFile(lootTableIndex, ltiData)


def runMissions(missionID):
    missionData = missionFile.getMissionInfo(db, missionID)
    writeMissionFile(missionID, missionData)

def runNPC(npcID):
    npcData = {"npcID": npcID}
    getComps.getInfo(db, npcData, npcID)
    render.getInfo(db, npcData, npcData['components'][2])
    if npcData['components'][16] is not None:
        npcData['isVendor'] = 1
        vendor.getInfo(db, npcData, npcData['components'][16])
    else:
        npcData['isVendor'] = 0

    if npcData['components'][73] is not None:
        npcData['isMissionGiver'] = 1
        npcData['missions'] = {}
        npcMissions.getInfo(db, npcData, npcData['components'][73])
        #print(npcData['missionsList'])
        for missionID in npcData['missionsList']:
            npcData['missions'][missionID] = missionFile.getMissionInfo(db, missionID)
    else:
        npcData['isMissionGiver'] = 0
    vendorPretty.fixPfp(npcData)

    writeNPCFile(npcID, npcData)



#lootTableIndexesList = []
#lootTableIndexesList = lootTableIndexesList[lootTableIndexesList.index(752):]

file = "work/cdclient.sqlite"
db = create_connection(file)
lootTableIndexesList = glti.length(db)
objectIDsList = getAllObjects.length(db)
missionIDsList = getAllMissions.length(db)
npcsList = getAllNPCs.length(db)

lootTableIndexesList = []
objectIDsList = [] #items only
missionIDsList = []
npcsList = [13569]

for lti in lootTableIndexesList:
    print('Created LootTableIndex: '+str(lti))
    runLTIs(lti)


#objectIDsList = []

for objectID in objectIDsList:
    print('Started Item:', objectID)
    runObjects(objectID)

#missionIDsList = [1718, 689, 792]

for missionID in missionIDsList:
    print('Started Mission:', missionID)
    runMissions(missionID)

for npcID in npcsList:
    print('Started NPC:', npcID)
    runNPC(npcID)
