import sqlite3
import os
import json

def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except:
        print("\nError")
    return conn


with open('./../output/search/behaviorData.json') as x:
    behaviorData = json.load(x)

def writeFile(data):

    #os.makedirs(os.path.dirname('test.json'), exist_ok=True)
    with open('test.json', 'w',
              encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

file = "./../work/cdclient.sqlite"
db = create_connection(file)

actions = ["action", "miss action", "blocked action", "action_false", "action_true", "start_action", "chain_action", "break_action", "double_jump_action", "ground_action", "jump_action", "hit_action", "hit_action_enemy", "timeout_action", "air_action", "falling_action", "jetpack_action", "spawn_fail_action", "action_failed", "action_consumed", "blocked_action", "moving_action", "on_success", "behavior","behavior 0","behavior 1","behavior 2","behavior 3","behavior 4","behavior 5","behavior 6","behavior 7","behavior 8","behavior 9","bahavior 2"]

cur = db.cursor()
cur.execute("SELECT * FROM BehaviorParameter"),
rows = cur.fetchall()
behaviorID = 25981
data = {}
used = []
data['overview'] = {}
data['overview']['hasChargeUp'] = False
data['overview']['spawnsObject'] = False
data['overview']['meleeAttack'] = False
data['overview']['projectileAttack'] = False
for row in rows:
    if row[0] == behaviorID:
        #print(row[1])
        data[row[1]] = {"initial_value": int(row[2])}
    #pass

#print(obj)

def getKidsKids(obj, parameter, branch):
    obj[parameter] = {}
    try:
        obj[parameter]['name'] = behaviorData[str(parameter)]
        if obj[parameter]['name']['templateID'] == 43:
            data['overview']['hasChargeUp'] = True
            branch = 'chargeup'
        elif obj[parameter]['name']['templateID'] == 27:
            data['overview']['spawnsObject'] = True
        elif obj[parameter]['name']['templateID'] == 1:
            data['overview']['meleeAttack'] = True
        elif obj[parameter]['name']['templateID'] == 4:
            data['overview']['projectileAttack'] = True
    except:
        pass
    obj[parameter]['hasKids'] = False
    obj[parameter]['info'] = {}
    obj[parameter]['kids'] = {}
    #print(obj[parameter]['initial_value'])
    #print(parameter)

    for row in rows:
        if row[0] == int(parameter):

            obj[parameter]['hasKids'] = True
            obj[parameter]['info'][row[1]] = int(row[2])
            #obj[parameter]['kids'][row[1]] = int(row[2])
            #print(obj)




    for param in obj[parameter]['info']:
        if param in actions and obj[parameter]['info'][param] not in used:
            #print(obj[parameter]['kids'])
            used.append(obj[parameter]['info'][param])
            getKidsKids(obj[parameter]['kids'], int(obj[parameter]['info'][param]), branch)
            # pass
            # else:
                #getKidsKids(obj[parameter]['kids'], int(row[2]), True)
                # pass
                #obj[parameter]['kids'][str(row[0])]

        if branch == 'chargeup' and param == 'min damage':
            data['overview']['chargeUpCombo'] = obj[parameter]['info'][param]
        # else:
        #     print(param, branch)
    #used.append(parameter)
    return obj

#
# for parameter in obj:
#     obj[parameter]['hasKids'] = False
#     obj[parameter]['kids'] = {}
#     #print(obj[parameter]['initial_value'])
#     for row in rows:
#         if row[0] == obj[parameter]['initial_value']:
#             obj[parameter]['hasKids'] = True
#             obj[parameter]['kids'][str(row[0])] = {row[1]: int(row[2])}
#             if row[1] in actions:
#                 getKidsKids(obj[parameter]['kids'][str(row[0])], int(row[2]))


getKidsKids(data, behaviorID, "")


def sort(obj):
    obj['overview'] = {
        "meleeCombo": meleeCombo(),
        "projectileCombo": projectileCombo(),
        #"chargeUpIsProjectile": chargeUpIsProjectile(),
    }


    return obj
#print(obj)

# sort(data)

writeFile(data)
