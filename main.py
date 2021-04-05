import sqlite3
import json
import math
import sys

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
import functions.enemyDrops as enemyDrops
import functions.enemySkills as enemySkills
import functions.getAllEnemies as getAllEnemies
import functions.rarityTableForEnemy as enemyRTI

import externalFunctions.getAllLootTableIndexes as glti
import externalFunctions.getAllMission as getAllMissions
import externalFunctions.getAllObjects as getAllObjects
import externalFunctions.getAllNPCs as getAllNPCs


def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except:
        print("\nError")
    return conn


def writeObjectFile(objectID, objectData):
    with open('output/objects/' + str(math.floor(objectID / 256)) + '/' + str(objectID) + '.json', 'w',
              encoding='utf-8') as f:
        json.dump(objectData, f, ensure_ascii=False, indent=4)


def writeLTIFile(objectID, objectData):
    with open('output/lootTableIndexes/' + str(objectID) + '.json', 'w', encoding='utf-8') as f:
        json.dump(objectData, f, ensure_ascii=False, indent=4)


def writeMissionFile(objectID, objectData):
    # print(objectData)
    with open('output/missions/' + str(objectID) + '.json', 'w', encoding='utf-8') as f:
        json.dump(objectData, f, ensure_ascii=False, indent=4)


def writeNPCFile(objectID, objectData):
    # print(objectData)
    with open('output/npcs/' + str(math.floor(objectID / 256)) + '/' + str(objectID) + '.json', 'w',
              encoding='utf-8') as f:
        json.dump(objectData, f, ensure_ascii=False, indent=4)


def writeEnemyFile(objectID, objectData):
    # print(objectData)
    with open('output/enemies/' + str(objectID) + '.json', 'w', encoding='utf-8') as f:
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
        # print(npcData['missionsList'])
        for missionID in npcData['missionsList']:
            npcData['missions'][missionID] = missionFile.getMissionInfo(db, missionID)
    else:
        npcData['isMissionGiver'] = 0
    vendorPretty.fixPfp(npcData)

    writeNPCFile(npcID, npcData)


def runEnemy(enemyID):
    enemyData = {"enemyID": enemyID}
    getComps.getInfo(db, enemyData, enemyID)
    enemyDrops.getInfo(db, enemyData, enemyID)
    enemySkills.getInfo(db, enemyData, enemyID)
    enemyRTI.getInfo(db, enemyData, enemyID)
    writeEnemyFile(enemyID, enemyData)


# lootTableIndexesList = []
# lootTableIndexesList = lootTableIndexesList[lootTableIndexesList.index(752):]

file = "work/cdclient.sqlite"
db = create_connection(file)
lootTableIndexesList = glti.length(db)
objectIDsList = getAllObjects.length(db)
missionIDsList = getAllMissions.length(db)
npcsList = getAllNPCs.length(db)
enemyList = getAllEnemies.length(db)

lootTableIndexesList = []
objectIDsList = []
missionIDsList = []
npcsList = []
enemyList = [4712]


for lti in lootTableIndexesList:
    sys.stdout.write("\rLootTableIndexes: " + str(lootTableIndexesList.index(lti)*100/len(lootTableIndexesList)) + '%')
    sys.stdout.flush()
    runLTIs(lti)
print("\rLootTableIndexes: 100%")
import sys

import inspect
import os
for objectID in objectIDsList:
    #print(objectID)
    sys.stdout.write("\rObjects: " + str(objectIDsList.index(objectID)*100/len(objectIDsList)) + '%')
    sys.stdout.flush()
    runObjects(objectID)
    #print("\n\rCompleted: " + str(objectIDsList.index(objectID) * 100 / len(objectIDsList)) + '%', flush=True)
    #time.sleep(0.04)

# missionIDsList = [1718, 689, 792]
print("\rObjects: 100%")
for missionID in missionIDsList:
    sys.stdout.write("\rMissions: " + str(missionIDsList.index(missionID)*100/len(missionIDsList)) + '%')
    sys.stdout.flush()
    runMissions(missionID)
print("\rMissions: 100%")

for npcID in npcsList:
    sys.stdout.write("\rNPCs: " + str(npcsList.index(npcID)*100/len(npcsList)) + '%')
    sys.stdout.flush()
    runNPC(npcID)
print("\rNPCs: 100%")

for enemyID in enemyList:
    sys.stdout.write("\rEnemies: " + str(enemyList.index(enemyID)*100/len(enemyList)) + '%')
    sys.stdout.flush()
    runEnemy(enemyID)
print("\rEnemies: 100%")
