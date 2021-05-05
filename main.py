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
import functions.getDamageCombo as getDamageCombo
import functions.references as references

import externalFunctions.parseLocale as xml


# use `lootTableIndexesList = lootTableIndexesList[lootTableIndexesList.index(752):]` to start at an a location and do the rest (useful if theres an error at file 752 and i dont want to redo the first 751 files)

with open('work/config.json') as f:
    config = json.load(f)

# with open(config['path']+'/search/allLists.json') as f:
with open(config['path']+'/search/allLists.json') as f:

    allLists = json.load(f)

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
    objectData['itemComponent'] = {}
    objectData['itemComponent']['subItems'] = None
    # objectData['itemComponent']['equipLocation'] = None
    # objectData['itemComponent']['sellPrice'] = None
    # objectData['itemComponent']['buyPrice'] = None
    # objectData['itemComponent']['isKitPiece'] = None
    # objectData['itemComponent']['rarity'] = None
    # objectData['itemComponent']['itemComponent'] = None
    # objectData['itemComponent']['inLootTable'] = None
    # objectData['itemComponent']['inVendor'] = None
    # objectData['itemComponent']['stackSize'] = None
    # objectData['itemComponent']['color'] = None
    # objectData['itemComponent']['preconditions'] = None
    # objectData['itemComponent']['isTwoHanded'] = None
    # objectData['itemComponent']['altCurrencyType'] = None
    # objectData['itemComponent']['altCurrencyCost'] = None
    # objectData['itemComponent']['subItems'] = None
    try:
        itemComp.getInfo(db, objectData, objectData['components'][11])
        proxy.getInfo(db, objectData, objectID)
        #print(objectData)
    except:
        pass
    try:
        render.getInfo(db, objectData, objectData['components'][2])
    except:
        objectData['iconURL'] = 'https://github.com/MasterTemple/lu_bot/blob/master/src/unknown.png?raw=true'

    buy.getInfo(db, objectData, objectID)
    earn.getInfo(db, objectData, objectID)
    # proxy.getInfo(db, objectData, objectID)

    pretty.makePretty(db, objectData)
    writeAnyFile(objectID, objectData, True, 'objects')

def runLTIs(lootTableIndex):
    ltiData = ltiFile.getInfo(db, lootTableIndex)
    import externalFunctions.getLTIName as getLTIName
    ltiData['nameInfo'] = getLTIName.getName(lootTableIndex)
    # if ltiData['nameInfo']['Type'] == "Powerup":
    #     ltiData['rarityCount'][]
    writeAnyFile(lootTableIndex, ltiData, False, 'lootTableIndexes')


def runPackages(packageID):
    packageData = objectInfo.getInfo(db, packageID)
    packageData = packageFile.getInfo(db, packageID, packageData)
    getComps.getInfo(db, packageData, packageID)

    render.getInfo(db, packageData, packageData['components'][2])

    writeAnyFile(packageID, packageData, False, 'packages')


def runMissions(missionID):
    missionData = missionFile.getMissionInfo(db, missionID)
    writeAnyFile(missionID, missionData, False, 'missions')


def runNPC(npcID):
    npcData = objectInfo.getInfo(db, npcID)
    npcData["npcID"] = npcID
    getComps.getInfo(db, npcData, npcID)
    try:
        render.getInfo(db, npcData, npcData['components'][2])
    except KeyError:
        npcData['components'][2] = None
        npcData['iconURL'] = None
    try:
        npcData['isVendor'] = 1
        vendor.getInfo(db, npcData, npcData['components'][16])
    except KeyError:
        npcData['isVendor'] = 0
        npcData['components'][16] = None

    try:
        npcData['isMissionGiver'] = 1
        npcData['missions'] = {}
        npcMissions.getInfo(db, npcData, npcData['components'][73])
        for missionID in npcData['missionsList']:
            npcData['missions'][missionID] = missionFile.getMissionInfo(db, missionID)
    except KeyError:
        npcData['isMissionGiver'] = 0
        npcData['components'][73] = None
    vendorPretty.fixPfp(npcData)
    #print(npcData)
    writeAnyFile(npcID, npcData, True, 'npcs')


def runEnemy(enemyID):
    enemyData = objectInfo.getInfo(db, enemyID)
    enemyData["enemyID"] = enemyID
    getComps.getInfo(db, enemyData, enemyID)
    import functions.renderComponent as render
    try:
        enemyData = render.getInfo(db, enemyData, enemyData['components'][2])
    except:
        enemyData['iconURL'] = "unknown"
    enemyDrops.getInfo(db, enemyData, enemyID)
    enemySkills.getInfo(db, enemyData, enemyID)
    behaviors.getInfo(db, enemyData, enemyData['skillIDs'])
    enemyData['overview'] = {}
    pretty.getEnemySkills(enemyData)

    if enemyData['doesntDropAnything'] == False:
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
    #activityData = {"id": activityID}
    activityData = activityFile.getInfo(db, activityID)
    for key in activityData['activities'].keys():
        if "Wishing Well" in key:
            activityFile.totalWishingWellKey(activityData)
            break

    writeAnyFile(activityID, activityData, False, 'activities')


def runBehaviorTrees(behaviorID):
    behaviorData = getDamageCombo.run(db, behaviorID)
    writeAnyFile(behaviorID, behaviorData, True, 'behaviors')



def runSetup(db):
    #print("ok")
    import externalFunctions.setup as setup
    pkgData = setup.packageList(db)
    writeAnyFile("packageList", pkgData, False, 'search')
    activityData = setup.activityList(db)
    writeAnyFile("activityList", activityData, False, 'search')
    behaviorData = setup.behaviorList(db)
    writeAnyFile("behaviorData", behaviorData, False, 'search')



def runReferences():
    # objectsData = references.getInfo(db)
    # # ltiData = ltiFile.getInfo(db, lootTableIndex)
    # # ltiData['nameInfo'] = getLTIName.getName(lootTableIndex)
    # writeAnyFile("objects", objectsData, False, 'references')
    Locale = references.xml2json()
    writeAnyFile("Locale", Locale, False, 'references')
    ObjectsData = references.getObjects(db)
    writeAnyFile("Objects", ObjectsData, False, 'references')
    ItemsData = references.getItems(db)
    writeAnyFile("Items", ItemsData, False, 'references')
    NPCsData = references.getNPCs(db)
    writeAnyFile("NPCs", NPCsData, False, 'references')
    BricksData = references.getBricks(db)
    writeAnyFile("Bricks", BricksData, False, 'references')
    MissionsData = references.getMissions(db)
    writeAnyFile("Missions", MissionsData, False, 'references')
    MissionsLocationData = references.getMissionLocation()
    writeAnyFile("MissionLocations", MissionsLocationData, False, 'references')
    EnemyData = references.getEnemies(db)
    writeAnyFile("Enemies", EnemyData, False, 'references')
    BricksAndItemsData = references.getBricksAndItems(db)
    writeAnyFile("BricksAndItems", BricksAndItemsData, False, 'references')
    PackagesData = references.getPackages(db)
    writeAnyFile("Packages", PackagesData, False, 'references')
    KitData = references.getKits(db)
    writeAnyFile("Kits", KitData, False, 'references')
    SkillData = references.getSkills(db)
    writeAnyFile("Skills", SkillData, False, 'references')
    ActivityData = references.getActivities(db)
    writeAnyFile("Activities", ActivityData, False, 'references')
    LootTableIndexData = references.getLTINames()
    writeAnyFile("LootTableIndexNames", LootTableIndexData, False, 'references')
    PreconditionsData = references.getPreconditionsData(db)
    writeAnyFile("Preconditions", PreconditionsData, False, 'references')
    writeAnyFile("EnemyPFPUpdates", [], False, 'contributor')
    writeAnyFile("NPCPFPUpdates", [], False, 'contributor')


LootTableIndexData = references.getLTINames()
writeAnyFile("LootTableIndexNames", LootTableIndexData, False, 'references')

def runModify():

    with open('work/modifyFile.json') as f:
        modifyFile = json.load(f)

    for data in modifyFile['data']:
        with open(config['path']+'/'+modifyFile['data'][data]['file']) as f:
            editFile = json.load(f)
            for edit in modifyFile['data'][data]['edits']:
                print(edit)

        with open(config['path']+'/'+modifyFile['data'][data]['file']) as f:
            json.dump(modifyFile, f, ensure_ascii=False, indent=4)

    #print(editFile)




def createAllLists(lootTableIndexesList, packagesList, objectIDsList, missionIDsList, npcsList, enemyList, cooldownGroupList, levelsList, kitIDList, activitiesList, behaviorsList):
    listObject = {}
    listObject['lootTableIndexesList'] = lootTableIndexesList
    listObject['packagesList'] = packagesList
    listObject['objectIDsList'] = objectIDsList
    listObject['missionIDsList'] = missionIDsList
    listObject['npcsList'] = npcsList
    listObject['enemyList'] = enemyList
    listObject['cooldownGroupList'] = cooldownGroupList
    listObject['levelsList'] = levelsList
    listObject['kitIDList'] = kitIDList
    listObject['activitiesList'] = activitiesList
    listObject['behaviorsList'] = behaviorsList
    writeAnyFile("allLists", listObject, False, 'search')


if config['startFromFdb'] == True:
    import lcdr.fdb_to_sqlite as lcdr
    lcdr.convert('work/cdclient.fdb', 'work/cdclient.sqlite')


file = "work/cdclient.sqlite"
db = create_connection(file)
# listObject = {}

#runReferences()


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
    import externalFunctions.getAllBehaviors as getAllBehaviors

    lootTableIndexesList = glti.length(db)
    packagesList = getAllPackages.length(db)
    objectIDsList = getAllObjects.getObjects(db)
    missionIDsList = getAllMissions.length(db)
    npcsList = getAllNPCs.length(db)
    enemyList = getAllEnemies.length(db)
    cooldownGroupList = getAllCooldownGroups.length(db)
    levelsList = getAllLevels.length(db)
    kitIDList = getAllKits.length(db)
    activitiesList = getAllActivities.length(db)
    behaviorsList = getAllBehaviors.length(db)
    createAllLists(lootTableIndexesList, packagesList, objectIDsList, missionIDsList, npcsList, enemyList, cooldownGroupList, levelsList, kitIDList, activitiesList, behaviorsList)
    runReferences()
    """
    #creates a file of all these lists
    listObject['lootTableIndexesList'] = lootTableIndexesList
    listObject['packagesList'] = packagesList
    listObject['objectIDsList'] = objectIDsList
    listObject['missionIDsList'] = missionIDsList
    listObject['npcsList'] = npcsList
    listObject['enemyList'] = enemyList
    listObject['cooldownGroupList'] = cooldownGroupList
    listObject['levelsList'] = levelsList
    listObject['kitIDList'] = kitIDList
    listObject['activitiesList'] = activitiesList
    listObject['behaviorsList'] = behaviorsList
    writeAnyFile("allLists", listObject, False, 'search')
    
    createAllLists(lootTableIndexesList, packagesList, objectIDsList, missionIDsList, npcsList, enemyList, cooldownGroupList, levelsList, kitIDList, activitiesList, behaviorsList)
    """


elif config['startByImportingList'] == True:

    lootTableIndexesList = allLists['lootTableIndexesList']
    packagesList = allLists['packagesList']
    objectIDsList = allLists['objectIDsList']
    missionIDsList = allLists['missionIDsList']
    npcsList = allLists['npcsList']
    enemyList = allLists['enemyList']
    cooldownGroupList = allLists['cooldownGroupList']
    levelsList = allLists['levelsList']
    kitIDList = allLists['kitIDList']
    activitiesList = allLists['activitiesList']
    behaviorsList = allLists['behaviorsList']
    # lootTableIndexesList = []
    # packagesList = []
    # behaviorsList = behaviorsList[behaviorsList.index(5896):]

    # percent = 8.1
    # behaviorsList = behaviorsList[behaviorsList.index(behaviorsList[round(len(behaviorsList) * (percent/100))]):]


elif config['executeSpecific'] == True:
    lootTableIndexesList = []  # = allLists['lootTableIndexesList']
    packagesList = []  # = allLists['packagesList']
    objectIDsList = []  # = allLists['objectIDsList']
    missionIDsList = []  # = allLists['missionIDsList']
    npcsList = []  # = allLists['npcsList']
    enemyList = []  # = allLists['enemyList']
    cooldownGroupList = []  # = allLists['cooldownGroupList']
    levelsList = []  # = allLists['levelsList']
    kitIDList = []  # = allLists['kitIDList']
    activitiesList = []  # = allLists['activitiesList']
    behaviorsList = []  # = allLists['behaviorsList']
    # objectIDsList = allLists['objectIDsList']
    # percent = 4.4
    # objectIDsList = objectIDsList[objectIDsList.index(objectIDsList[round(len(objectIDsList) * (percent/100))]):]
    # lootTableIndexesList = allLists['lootTableIndexesList']
    # lootTableIndexesList = lootTableIndexesList[lootTableIndexesList.index(83):]

    #behaviorsList = allLists['behaviorsList']
    #behaviorsList = behaviorsList[behaviorsList.index(11175):]


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
    behaviorsList = config['behaviorsList']

    # enemyList = allLists['enemyList']

    #lootTableIndexesList = allLists['lootTableIndexesList']
    #lootTableIndexesList = lootTableIndexesList[lootTableIndexesList.index(54):]


#kitIDList = allLists['kitIDList']


    # objectIDsList = allLists['objectIDsList']
    # objectIDsList = objectIDsList[objectIDsList.index(5347):]
    #cooldownGroupList = allLists['cooldownGroupList']

    # npcsList = allLists['npcsList']
    # npcsList = npcsList[npcsList.index(6014):]


#enemyList = allLists['enemyList']

#enemyList = allLists['enemyList']

    # objectIDsList = allLists['objectIDsList']
    #
    #
    # # behaviorsList = behaviorsList[behaviorsList.index(11175):]
    # objectIDsList = objectIDsList[objectIDsList.index(12651):]

    #behaviorsList = allLists['behaviorsList']
    # behaviorsList = behaviorsList[behaviorsList.index(11175):]
    # percent = 3.458
    # objectIDsList = objectIDsList[objectIDsList.index(objectIDsList[round(len(objectIDsList) * (percent/100))]):]

else:

    print("Please specify how you would like to create your files in work/config.json")

    # lootTableIndexesList = config['lootTableIndexesList']
    # packagesList = config['packagesList']
    # objectIDsList = config['objectIDsList']
    # missionIDsList = config['missionIDsList']
    # npcsList = config['npcsList']
    # enemyList = config['enemyList']
    # cooldownGroupList = config['cooldownGroupList']
    # levelsList = config['levelsList']
    # kitIDList = config['kitIDList']
    # activitiesList = config['activitiesList']
    # behaviorsList = config['behaviorsList']

#print('start')
# import externalFunctions.getAllBehaviors as getAllBehaviors
# behaviorsList = getAllBehaviors.length(db)

# import externalFunctions.getAllPackages as getAllPackages
# packages = getAllPackages.length(db)
# print(packages)
"""
config['functionsInfo'] formation is [printedOutName, functionToExecute, listOfItemsToExecute, executeOnce]
"""

#packagesList = allLists['packagesList']
# activitiesList = allLists['activitiesList']
#enemyList = allLists['enemyList']
#activitiesList = allLists['activitiesList']


# MissionsData = references.getMissions(db)
# writeAnyFile("Missions", MissionsData, False, 'references')
# MissionsLocationData = references.getMissionLocation()
# writeAnyFile("MissionLocations", MissionsLocationData, False, 'references')
#print(behaviorsList)
now = time.now()
previous = now.strftime("%H:%M:%S")
#print(len(behaviorsList))
#current_time = now.strftime("%H:%M:%S")
print("\r" +'[' + str(now.strftime("%H:%M:%S")) + '] Process Started.')
if config['setup']:
    runSetup(db)
print("\r" +'[' + str(now.strftime("%H:%M:%S")) + "] Setup: 100%")
for func in config['functionsInfo']:
    if func[3] == False:
        for id in eval(func[2]):
            #sys.stdout.write("\r" + func[0] + ": " + str(round(eval(func[2]).index(id)*100/len(eval(func[2])), 3)) + '%')
            #sys.stdout.write("\r" + func[0] + ": " + str(id))
            sys.stdout.write("\r" + func[0] + ": " + str(round(eval(func[2]).index(id)*100/len(eval(func[2])), 3)) + '% ' + str(id))
            sys.stdout.flush()
            eval(func[1])(id)
    else:
        try:
            eval(func[1])(eval(func[2]))
        except:
            pass
            #eval(func[1])()
    print("\r" +'[' + str(now.strftime("%H:%M:%S")) + '] ' + func[0] + ": 100%")
    #    print("\r" + func[0] + ": 100% at "+str(now.strftime("%H:%M:%S")) + " -> " + str(previous))

    #previous = time.now()
    previous = now.strftime("%H:%M:%S")

# runModify()

# PreconditionsData = references.getPreconditionsData(db)
# writeAnyFile("Preconditions", PreconditionsData, False, 'references')
# ActivityData = references.getActivities(db)
# writeAnyFile("Activities", ActivityData, False, 'references')
