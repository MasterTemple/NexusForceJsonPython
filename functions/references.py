def getObjects(conn):
    cur = conn.cursor()
    cur.execute("SELECT id, name, type, displayName FROM Objects ORDER BY displayName ASC")
    rows = cur.fetchall()
    array = []
    for row in rows:
        if row[0] not in array:
            if row[3] is None:
                displayName = row[1]
            else:
                displayName = row[3]
            array.append({
                "id": row[0],
                "name": row[1],
                "type": row[2],
                "displayName": displayName
            })
        else:
            pass
            #print(row[0])
    return array


def getItems(conn):
    cur = conn.cursor()
    cur.execute("SELECT id, name, type, displayName FROM Objects")
    rows = cur.fetchall()
    array = []
    for row in rows:
        if row[0] not in array and (row[2] == 'Loot'):
            if row[3] is None:
                displayName = row[1]
            else:
                displayName = row[3]
            obj = {
                "id": row[0],
                "name": row[1],
                "type": row[2]
            }
            if row[3] is not None:
                obj["displayName"] = row[3]

            array.append(obj)
    return array

def getNPCs(conn):
    cur = conn.cursor()
    cur.execute("SELECT id, name, type, displayName FROM Objects")
    rows = cur.fetchall()
    array = []
    for row in rows:
        if row[0] not in array and (row[2] == 'UserGeneratedNPCs' or row[2] == 'NPC'):
            obj = {
                "id": row[0],
                "name": row[1],
                "type": row[2]
            }
            if row[3] is not None:
                obj["displayName"] = row[3]

            array.append(obj)
    return array

def getBricks(conn):
    cur = conn.cursor()
    cur.execute("SELECT id, name, type, displayName FROM Objects")
    rows = cur.fetchall()
    array = []
    for row in rows:
        if row[0] not in array and (row[2] == 'LEGO brick'):
            obj = {
                "id": row[0],
                "name": row[1],
                "type": row[2]
            }
            if row[3] is not None:
                obj["displayName"] = row[3]

            array.append(obj)
    return array


def getBricksAndItems(conn):
    cur = conn.cursor()
    cur.execute("SELECT id, name, type, displayName FROM Objects")
    rows = cur.fetchall()
    array = []
    for row in rows:
        if row[0] not in array and (row[2] == 'LEGO brick' or row[2] == 'Loot'):
            obj = {
                "id": row[0],
                "name": row[1],
                "type": row[2]
            }
            if row[3] is not None:
                obj["displayName"] = row[3]

            array.append(obj)
    return array

def getMissions(conn):
    cur = conn.cursor()
    cur.execute("SELECT id, defined_type, defined_subtype, isMission FROM Missions")
    rows = cur.fetchall()
    array = []
    import xml.etree.ElementTree as ET
    #tree = ET.parse('./../work/locale.xml')
    tree = ET.parse('./work/locale.xml')
    import externalFunctions.parseLocale as xml

    root = tree.getroot()
    for row in rows:
        if row[3] == 1:
            missionInfo = xml.getMissionInfo(row[0], root)
        if row[3] == 0:
            missionInfo = xml.getAchievementInfo(row[0], root)

        subtype = row[2]
        if subtype is None:
            subtype = row[1]


        array.append({
            "id": row[0],
            "defined_type": row[1],
            "defined_subtype": subtype,
            "name": missionInfo['name'],
            "description": missionInfo['description'],
            "isMission": row[3]
        })

    return array

def getMissionLocation():
    import json
    with open('work/config.json') as f:
        config = json.load(f)
    with open(config['path']+'/references/Missions.json') as f:
        missionFile = json.load(f)

    missionData = {
        "Achievements":{},
        "Missions":{}
    }

    for mission in missionFile:
        if mission['isMission'] == 0:
            if mission['defined_type'] not in missionData.keys():
                missionData['Achievements'][mission['defined_type']] = {}

            if mission['defined_subtype'] not in missionData['Achievements'][mission['defined_type']].keys():
                missionData['Achievements'][mission['defined_type']][mission['defined_subtype']] = []

        if mission['isMission'] == 1:
            if mission['defined_type'] not in missionData.keys():
                missionData['Missions'][mission['defined_type']] = {}
            if mission['defined_subtype'] not in missionData['Missions'][mission['defined_type']].keys():
                missionData['Missions'][mission['defined_type']][mission['defined_subtype']] = []


    for mission in missionFile:

        if mission['defined_subtype'] is None:
            #print(mission['defined_subtype'])
            mission['defined_subtype'] = mission['defined_type']
            #print(mission['defined_subtype'])



        if mission['isMission'] == 0:
            missionData['Achievements'][mission['defined_type']] = {}

            missionData['Achievements'][mission['defined_type']][mission['defined_subtype']] = []

        if mission['isMission'] == 1:
            missionData['Missions'][mission['defined_type']] = {}
            missionData['Missions'][mission['defined_type']][mission['defined_subtype']] = []

    # for mission in missionFile:
    #     if mission['isMission'] == 0:
    #
    #         try:
    #             missionData['Achievements'][mission['defined_type']][mission['defined_subtype']].append({
    #                 "id": mission['id'],
    #                 "name": mission['name'],
    #                 "description": mission['description']
    #
    #             })
    #         except:
    #             missionData['Achievements'][mission['defined_type']][mission['defined_subtype']] = []
    #
    #             missionData['Achievements'][mission['defined_type']][mission['defined_subtype']].append({
    #                 "id": mission['id'],
    #                 "name": mission['name'],
    #                 "description": mission['description']
    #
    #             })
    #
    #
    #     if mission['isMission'] == 1:
    #
    #         try:
    #             missionData['Missions'][mission['defined_type']][mission['defined_subtype']].append({
    #                 "id": mission['id'],
    #                 "name": mission['name'],
    #                 "description": mission['description']
    #
    #             })
    #         except:
    #             missionData['Missions'][mission['defined_type']][mission['defined_subtype']] = []
    #             missionData['Missions'][mission['defined_type']][mission['defined_subtype']].append({
    #                 "id": mission['id'],
    #                 "name": mission['name'],
    #                 "description": mission['description']
    #
    #             })
    for mission in missionFile:
        if mission['isMission'] == 0:
            if mission['defined_subtype'] is None:
                mission['defined_subtype'] = mission['defined_type']

            #print(mission['defined_type'], mission['defined_subtype'])
            try:
                missionData['Achievements'][mission['defined_type']][mission['defined_subtype']].append({
                    "id": mission['id'],
                    "name": mission['name'],
                    "description": mission['description']

                })
            except KeyError:
                missionData['Achievements'][mission['defined_type']][mission['defined_subtype']] = []
                missionData['Achievements'][mission['defined_type']][mission['defined_subtype']].append({
                    "id": mission['id'],
                    "name": mission['name'],
                    "description": mission['description']

                })



        if mission['isMission'] == 1:

            if mission['defined_subtype'] is None:
                mission['defined_subtype'] = mission['defined_type']

            try:
                missionData['Missions'][mission['defined_type']][mission['defined_subtype']].append({
                    "id": mission['id'],
                    "name": mission['name'],
                    "description": mission['description']

                })
            except KeyError:
                missionData['Missions'][mission['defined_type']][mission['defined_subtype']] = []
                missionData['Missions'][mission['defined_type']][mission['defined_subtype']].append({
                    "id": mission['id'],
                    "name": mission['name'],
                    "description": mission['description']

                })





    return missionData


def getEnemies(conn):
    cur = conn.cursor()
    cur.execute("SELECT id, name, type, displayName FROM Objects")
    rows = cur.fetchall()
    array = []
    for row in rows:
        if row[0] not in array and (row[2] == 'Enemies'):
            if row[3] is None:
                displayName = row[1]
            else:
                displayName = row[3]
            array.append({
                "id": row[0],
                "name": row[1],
                "type": row[2],
                "displayName": displayName
            })
        else:
            pass
            #print(row[0])
    return array


def getPackages(conn):
    cur = conn.cursor()
    cur.execute("SELECT id, component_type, component_id FROM ComponentsRegistry")
    rows = cur.fetchall()
    packageIDs = []
    array = []

    for row in rows:
        if row[0] not in array and row[1] == 53:
            packageIDs.append(row[0])


    cur.execute("SELECT id, name, type, displayName FROM Objects")
    rows = cur.fetchall()
    for row in rows:
        if row[0] not in array and row[0] in packageIDs:
            displayName = row[3]
            if displayName == None:
                displayName = "None"
            array.append({
                "id": row[0],
                "name": row[1],
                "type": row[2],
                "displayName": displayName
            })
    return array

def getKits(conn):
    cur = conn.cursor()
    cur.execute("SELECT setID, kitRank FROM ItemSets")
    rows = cur.fetchall()
    data = []
    import externalFunctions.parseLocale as xml
    ranks = [1, 2, 3]
    for row in rows:
        if row[0] not in data:
            info = xml.getKitName(row[0])
            obj = {
                "id": row[0],
                "name": info,
                "kitRank": row[1]
            }
            if obj['kitRank'] in ranks:
                obj['name'] = "Rank "+str(obj['kitRank'])+" "+obj['name']
            data.append(obj)

    return data


def getSkills(conn):
    cur = conn.cursor()
    cur.execute("SELECT skillID, cooldowngroup, skillIcon FROM SkillBehavior")
    rows = cur.fetchall()
    data = {}
    import externalFunctions.parseLocale as xml
    import functions.getKitData as getKitData

    for row in rows:
        if row[0] not in data:
            skillName = xml.getSkillInfo(row[0])
            try:
                data[row[0]] = {
                    "cdg": row[1],
                    "skillIcon": row[2],
                    "iconURL": getKitData.iconUrlFromID(cur, row[2])
                }

            except:
                data[row[0]] = {
                    "cdg": row[1],
                }
            try:
                data[row[0]].update(skillName)
            except:
                pass


    return data


def getActivities(conn):
    cur = conn.cursor()
    cur.execute("SELECT description, objectTemplate FROM ActivityRewards")
    rows = cur.fetchall()
    data = {}
    for row in rows:
        if row[0] not in data:
            data[row[0]] = row[1]
            if "Wishing Well 1" in row[0]:
                name = row[0][:len(row[0])-1] + "Total"
                #print(name)
                data[name] = row[1]
    return data


def getLTINames():
    import json
    with open('work/LootTableIndexNames.json') as f:
        LootTableIndexNames = json.load(f)
    arr = []
    for lti in LootTableIndexNames['data']:
        obj = {}
        obj["lti"] = lti['LootTableIndex']
        try:
            name = lti['Name']
        except KeyError:
            try:
                name = lti['AlternateName']
            except:
                name = "EMPTY"


        obj["name"] = name

        try:
            altname = lti['AlternateName']
        except KeyError:
            try:
                altname = lti['Name']
            except:
                altname = "EMPTY"


        obj["altName"] = altname

        arr.append(obj)

    return arr

def xml2json():
    import re
    obj = {}
    import xml.etree.ElementTree as ET
    tree = ET.parse('E:\LEGO Universe (unpacked)\locale\locale.xml')

    root = tree.getroot()

    for child in root[1]:
        if child.attrib['id']:
            obj[child.attrib['id']] = re.sub("<[^>]+>", "", child[0].text)


    return obj



def getPreconditionsData(conn):
    import json
    with open("work/config.json", encoding='utf-8') as f:
        config = json.load(f)
    with open(config['path']+"/references/locale.json", encoding='utf-8') as f:
        locale = json.load(f)

    cur = conn.cursor()
    cur.execute("SELECT id, reqPrecondition FROM ItemComponent")
    rows = cur.fetchall()
    arrayObj = {}
    for row in rows:
        if row[1] is None or row[1] == "" or row[1] == "62|26":
            continue
        pre = str(row[1]).split(";")
        for req in pre:
            try:
                if arrayObj[req] is None:
                    print('wow')
            except KeyError:
                arrayObj[req] = {}
                arrayObj[req]['components'] = []
                arrayObj[req]['itemIDs'] = []
                arrayObj[req]['description'] = "temp"
                arrayObj[req]['items'] = []



            arrayObj[req]['components'].append(row[0])

            try:
                arrayObj[req]['description'] = locale["Preconditions_"+str(req)+"_FailureReason"]
            except KeyError:
                del arrayObj[req]


    cur.execute("SELECT * FROM ComponentsRegistry")
    rows = cur.fetchall()

    for prereq in arrayObj.keys():
        for row in rows:
            if int(row[1]) == 11 and int(row[2]) in arrayObj[prereq]['components']:
                arrayObj[prereq]['itemIDs'].append(row[0])
                obj = {
                    "comp": row[2],
                    "itemID": row[0],
                }
                try:
                    obj['name'] = locale["Objects_"+str(row[0])+"_name"]
                except KeyError:
                    obj['name'] = "Objects_"+str(row[0])+"_name"

                arrayObj[prereq]['items'].append(obj)

    for prereq in arrayObj.keys():
        del arrayObj[prereq]['components']
        del arrayObj[prereq]['itemIDs']
    return arrayObj

def getObjectsLocale(conn, locale):
    array = []

    cur = conn.cursor()

    cur.execute("SELECT id, type FROM Objects ORDER BY id ASC")
    rows = cur.fetchall()
    for row in rows:
        try:
            array.append({
                "id": row[0],
                "type": row[1],
                "name": locale["Objects_"+str(row[0])+"_name"]
            })
        except:
            pass

    return array

def getItemsLocale(conn, locale):
    array = []

    cur = conn.cursor()

    cur.execute("SELECT id, type FROM Objects WHERE type='Loot' ORDER BY id ASC")
    rows = cur.fetchall()
    for row in rows:
        try:
            array.append({
                "id": row[0],
                "type": row[1],
                "name": locale["Objects_"+str(row[0])+"_name"]
            })
        except:
            pass

    return array

def getNPCsLocale(conn, locale):
    array = []

    cur = conn.cursor()

    cur.execute("SELECT id, type FROM Objects WHERE type='NPC' OR type='UserGeneratedNPCs' ORDER BY id ASC")
    rows = cur.fetchall()
    for row in rows:
        try:
            array.append({
                "id": row[0],
                "type": row[1],
                "name": locale["Objects_"+str(row[0])+"_name"]
            })
        except:
            pass

    return array

def getBricksLocale(conn, locale):
    array = []

    cur = conn.cursor()

    cur.execute("SELECT id, type FROM Objects WHERE type='LEGO Brick' ORDER BY id ASC")
    rows = cur.fetchall()
    for row in rows:
        try:
            array.append({
                "id": row[0],
                "type": row[1],
                "name": locale["Objects_"+str(row[0])+"_name"]
            })
        except:
            pass

    return array

def getEnemiesLocale(conn, locale):
    array = []

    cur = conn.cursor()

    cur.execute("SELECT id, type FROM Objects WHERE type='Enemies' ORDER BY id ASC")
    rows = cur.fetchall()
    for row in rows:
        try:
            array.append({
                "id": row[0],
                "type": row[1],
                "name": locale["Objects_"+str(row[0])+"_name"]
            })
        except:
            pass

    return array

def getBricksAndItemsLocale(conn, locale):
    array = []

    cur = conn.cursor()

    cur.execute("SELECT id, type FROM Objects WHERE type='Loot' OR type='LEGO Brick' ORDER BY id ASC")
    rows = cur.fetchall()
    for row in rows:
        try:
            array.append({
                "id": row[0],
                "type": row[1],
                "name": locale["Objects_"+str(row[0])+"_name"]
            })
        except:
            pass

    return array