import sqlite3
import json
import math
import sys
import os
from datetime import datetime as time

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
import functions.getLevelData as getLevelData
import functions.getCDGSkillIDs as getCDGSkillIDs
import functions.getKitData as getKitData
import functions.packageFile as packageFile
import functions.activityFile as activityFile
import externalFunctions.parseXML as xml


# use `lootTableIndexesList = lootTableIndexesList[lootTableIndexesList.index(752):]` to start at an a location and do the rest (useful if theres an error at file 752 and i dont want to redo the first 751 files)

with open('work/config.json') as f:
    config = json.load(f)

def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except:
        print("\nError")
    return conn

def writeAnyFile(ID, data, hasSubDir, fileName):
    if hasSubDir:
        os.makedirs(os.path.dirname(config['path'] + '/' + fileName + '/' + str(math.floor(ID / 256)) + '/' + str(ID) + '.json'), exist_ok=True)
        with open(config['path'] + '/' + fileName + '/' + str(math.floor(ID / 256)) + '/' + str(ID) + '.json', 'w',
                  encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
    else:
        os.makedirs(os.path.dirname(config['path'] + '/' + fileName + '/' + str(ID) + '.json'), exist_ok=True)
        with open(config['path'] + '/' + fileName + '/' + str(ID) + '.json', 'w',
                  encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

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
    writeAnyFile(objectID, objectData, True, 'objects')

def runLTIs(lootTableIndex):
    ltiData = ltiFile.getInfo(db, lootTableIndex)
    ltiData['nameInfo'] = getLTIName.getName(lootTableIndex)
    writeAnyFile(lootTableIndex, ltiData, False, 'lootTableIndexes')


def runPackages(packageID):
    packageData = packageFile.getInfo(db, packageID)
    writeAnyFile(packageID, packageData, False, 'packages')


def runMissions(missionID):
    missionData = missionFile.getMissionInfo(db, missionID)
    writeAnyFile(missionID, missionData, False, 'missions')


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
        for missionID in npcData['missionsList']:
            npcData['missions'][missionID] = missionFile.getMissionInfo(db, missionID)
    else:
        npcData['isMissionGiver'] = 0
    vendorPretty.fixPfp(npcData)
    writeAnyFile(npcID, npcData, True, 'npcs')


def runEnemy(enemyID):
    enemyData = {"enemyID": enemyID}
    getComps.getInfo(db, enemyData, enemyID)
    enemyDrops.getInfo(db, enemyData, enemyID)
    enemySkills.getInfo(db, enemyData, enemyID)
    enemyRTI.getInfo(db, enemyData, enemyID)
    writeAnyFile(enemyID, enemyData, False, 'enemies')


def runCooldownGroup(cdgID):
    cdgData = getCDGSkillIDs.getInfo(db, cdgID)

    # ltiData = ltiFile.getInfo(db, lootTableIndex)
    # ltiData['nameInfo'] = getLTIName.getName(lootTableIndex)
    writeAnyFile(cdgID, cdgData, False, 'cooldowngroup')


def runLevels(level):
    lvlData = getLevelData.getInfo(db, level)
    writeAnyFile("levels", lvlData, False, 'levelData')


def runKits(kitID):
    #print(kitID)
    kitData = {"id": kitID}
    kitData['name'] = xml.getKitName(kitID)
    getKitData.getInfo(db, kitData, kitID)
    writeAnyFile(kitID, kitData, False, 'kitData')


def runActivity(activityID):
    activityData = {"id": activityID}
    activityData = activityFile.getInfo(db, activityID)
    writeAnyFile(activityID, activityData, False, 'activities')


def runSetup(db):
    #print("ok")
    import externalFunctions.setup as setup
    pkgData = setup.packageList(db)
    writeAnyFile("packageList", pkgData, False, 'search')


if config['startFromFdb'] == True:
    import lcdr.fdb_to_sqlite as lcdr
    lcdr.convert('work/cdclient.fdb', 'work/cdclient.sqlite')


file = "work/cdclient.sqlite"
db = create_connection(file)

runSetup(db)

if config['startFromSqlite'] == True or config['startFromFdb'] == True:
    import externalFunctions.getAllLootTableIndexes as glti
    import externalFunctions.getAllMission as getAllMissions
    import externalFunctions.getAllObjects as getAllObjects
    import externalFunctions.getAllNPCs as getAllNPCs
    import externalFunctions.getLTIName as getLTIName
    import externalFunctions.getAllCooldownGroups as getAllCooldownGroups
    import externalFunctions.getAllLevels as getAllLevels
    import externalFunctions.getAllKits as getAllKits
    import externalFunctions.getAllPackages as getAllPackages
    import externalFunctions.getAllActivities as getAllActivities

    lootTableIndexesList = glti.length(db)
    packagesList = getAllPackages.length(db)
    objectIDsList = getAllObjects.length(db)
    missionIDsList = getAllMissions.length(db)
    npcsList = getAllNPCs.length(db)
    enemyList = getAllEnemies.length(db)
    cooldownGroupList = getAllCooldownGroups.length(db)
    levelsList = getAllLevels.length(db)
    kitIDList = getAllKits.length(db)
    activitiesList = getAllActivities.length(db)

elif config['justUpdateGivenInfo'] == True:

    lootTableIndexesList = config['lootTableIndexesList']
    packagesList = config['packagesList']
    objectIDsList = config['objectIDsList']
    missionIDsList = config['missionIDsList']
    npcsList = config['npcsList']
    enemyList = config['enemyList']
    cooldownGroupList = config['cooldownGroupList']
    levelsList = config['levelsList']
    kitIDList = config['kitIDList']
    activitiesList = config['activitiesList']
else:

    print("Please specify how you would like to create your files in work/config.json")
    lootTableIndexesList = config['lootTableIndexesList']
    packagesList = config['packagesList']
    objectIDsList = config['objectIDsList']
    missionIDsList = config['missionIDsList']
    npcsList = config['npcsList']
    enemyList = config['enemyList']
    cooldownGroupList = config['cooldownGroupList']
    levelsList = config['levelsList']
    kitIDList = config['kitIDList']
    activitiesList = config['activitiesList']


# import externalFunctions.getAllPackages as getAllPackages
# packages = getAllPackages.length(db)
# print(packages)
"""
config['functionsInfo'] formation is [printedOutName, functionToExecute, listOfItemsToExecute, executeOnce]
"""
now = time.now()
previous = now.strftime("%H:%M:%S")
#current_time = now.strftime("%H:%M:%S")
print("\r" +'[' + str(now.strftime("%H:%M:%S")) + '] Process Started.')
for func in config['functionsInfo']:
    if func[3] == False:
        for id in eval(func[2]):
            sys.stdout.write("\r" + func[0] + ": " + str(round(eval(func[2]).index(id)*100/len(eval(func[2])), 3)) + '%')
            sys.stdout.flush()
            eval(func[1])(id)
    else:
        eval(func[1])(eval(func[2]))
    print("\r" +'[' + str(now.strftime("%H:%M:%S")) + '] ' + func[0] + ": 100%")
    #    print("\r" + func[0] + ": 100% at "+str(now.strftime("%H:%M:%S")) + " -> " + str(previous))

    #previous = time.now()
    previous = now.strftime("%H:%M:%S")

