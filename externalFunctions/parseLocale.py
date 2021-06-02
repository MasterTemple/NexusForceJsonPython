def getMissionInfo(id, root):
    import json
    with open('work/config.json') as f:
        config = json.load(f)
    with open(config['path']+'/references/Locale.json', encoding="utf8") as f:
        locale = json.load(f)

    name = 'Missions_'+str(id)+'_name'
    inProgress = 'MissionText_'+str(id)+'_in_progress'
    mission = {}
    try:
        mission['name'] = locale[name]
    except KeyError:
        mission['name'] = "Unavailable"
    try:
        mission['description'] = locale[inProgress]
    except KeyError:
        mission['description'] = "Unavailable"

    return mission

def getAchievementInfo(id, root):
    import json
    with open('work/config.json') as f:
        config = json.load(f)
    with open(config['path']+'/references/Locale.json', encoding="utf8") as f:
        locale = json.load(f)
    name = 'Missions_'+str(id)+'_name'
    inProgress = 'MissionText_'+str(id)+'_description'
    mission = {}
    try:
        mission['name'] = locale[name]
    except KeyError:
        mission['name'] = "Unavailable"
    try:
        mission['description'] = locale[inProgress]
    except KeyError:
        mission['description'] = "Unavailable"

    return mission


def preconditions(preconditionIDs):
    import json
    with open('work/config.json') as f:
        config = json.load(f)
    with open(config['path']+'/references/Locale.json', encoding="utf8") as f:
        locale = json.load(f)

    preconditions = {}

    for i in preconditionIDs:
        preconditions[i] = locale['Preconditions_'+str(i)+'_FailureReason']

    return preconditions


def getSkillInfo(skillID):
    import json
    with open('work/config.json') as f:
        config = json.load(f)
    with open(config['path']+'/references/Locale.json', encoding="utf8") as f:
        locale = json.load(f)

    name = 'SkillBehavior_'+str(skillID)+'_name'
    description = 'SkillBehavior_'+str(skillID)+'_descriptionUI'

    skill = {}
    try:
        skill['name'] = locale[name]
    except:
        pass
    try:
        skill['rawDescription'] = locale[description]
    except:
        pass

    try:
        if '%(DamageCombo)' in skill['rawDescription']:

            # print(skill['rawDescription'][skill['rawDescription'].find('%(DamageCombo)')+len('%(DamageCombo)'):skill['rawDescription'].rfind('%(')])
            skill['damageCombo'] = (skill['rawDescription'][skill['rawDescription'].find('%(DamageCombo)')+len('%(DamageCombo)'):skill['rawDescription'].rfind('%(')])
            if skill['damageCombo'] == '':
                skill['damageCombo'] = (skill['rawDescription'][skill['rawDescription'].find('%(DamageCombo)')+len('%(DamageCombo)'):])
    except:
        pass
    try:
        if '%(Description)' in skill['rawDescription']:
            # print(skill['rawDescription'][skill['rawDescription'].find('%(Description)')+len('%(Description)'):skill['rawDescription'].rfind('%(')])
            skill['Description'] = (skill['rawDescription'][skill['rawDescription'].find('%(Description)')+len('%(Description)'):skill['rawDescription'].rfind('%(')])
            #print(skill['Description'])
            if skill['Description'] == '':
                skill['Description'] = (skill['rawDescription'][skill['rawDescription'].find('%(Description)')+len('%(Description)'):])
    except:
        pass

    try:
        if '%(ChargeUp)' in skill['rawDescription']:
            # print(skill['rawDescription'][skill['rawDescription'].find('%(ChargeUp)')+len('%(ChargeUp)'):skill['rawDescription'].rfind('%(')])
            skill['ChargeUp'] = (skill['rawDescription'][skill['rawDescription'].find('%(ChargeUp)')+len('%(ChargeUp)'):skill['rawDescription'].rfind('%(')])
            if skill['ChargeUp'] == '':
                skill['ChargeUp'] = (skill['rawDescription'][skill['rawDescription'].find('%(ChargeUp)')+len('%(ChargeUp)'):])
    except:
        pass
    return skill


def getKitName(kitID):
    import json
    with open('work/config.json') as f:
        config = json.load(f)
    with open(config['path']+'/references/Locale.json', encoding="utf8") as f:
        locale = json.load(f)
    name = 'ItemSets_'+str(kitID)+'_kitName'

    try:
        return locale[name]
    except:
        return name



def getKitAbility(skillID):
    import json
    with open('work/config.json') as f:
        config = json.load(f)
    with open(config['path']+'/references/Locale.json', encoding="utf8") as f:
        locale = json.load(f)

    name = 'SkillBehavior_'+str(skillID)+'_descriptionUI'
    return locale[name]


