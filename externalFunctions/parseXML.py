def getMissionInfo(id, root):
    name = 'Missions_'+str(id)+'_name'
    inProgress = 'MissionText_'+str(id)+'_in_progress'
    mission = {}
    for child in root[1]:
        if child.attrib['id'] == name:
            #print(child[0].text)
            mission['name'] = child[0].text
        if child.attrib['id'] == inProgress:
            #print(child[0].text)
            mission['description'] = child[0].text
    return mission

def getAchievementInfo(id, root):
    name = 'Missions_'+str(id)+'_name'
    inProgress = 'MissionText_'+str(id)+'_description'
    mission = {}
    for child in root[1]:
        if child.attrib['id'] == name:
            #print(child[0].text)
            mission['name'] = child[0].text
        if child.attrib['id'] == inProgress:
            #print(child[0].text)
            mission['description'] = child[0].text
    return mission


def preconditions(preconditionIDs):
    import xml.etree.ElementTree as ET
    tree = ET.parse('./work/locale.xml')
    root = tree.getroot()
    ##Preconditions_224_FailureReason
    preconditions = {}

    for i in preconditionIDs:
        name = 'Preconditions_'+str(i)+'_FailureReason'
        for child in root[1]:
            if child.attrib['id'] == name:
                #print(child[0].text)
                preconditions[i] = child[0].text
    return preconditions


def getSkillInfo(skillID):
    #from externalFunctions import parseXML as missionInfo
    import xml.etree.ElementTree as ET
    #tree = ET.parse('./../work/locale.xml')
    tree = ET.parse('./work/locale.xml')

    root = tree.getroot()
    #data['earn'] = {}
    #SkillBehavior_655_name
    name = 'SkillBehavior_'+str(skillID)+'_name'
    description = 'SkillBehavior_'+str(skillID)+'_descriptionUI'

    skill = {}
    for child in root[1]:
        if child.attrib['id'] == name:
            #print(child[0].text)
            skill['name'] = child[0].text
        if child.attrib['id'] == description:
            #print(child[0].text)
            skill['rawDescription'] = child[0].text

    if '%(DamageCombo)' in skill['rawDescription']:

        # print(skill['rawDescription'][skill['rawDescription'].find('%(DamageCombo)')+len('%(DamageCombo)'):skill['rawDescription'].rfind('%(')])
        skill['damageCombo'] = (skill['rawDescription'][skill['rawDescription'].find('%(DamageCombo)')+len('%(DamageCombo)'):skill['rawDescription'].rfind('%(')])
        if skill['damageCombo'] == '':
            skill['damageCombo'] = (skill['rawDescription'][skill['rawDescription'].find('%(DamageCombo)')+len('%(DamageCombo)'):])

    if '%(Description)' in skill['rawDescription']:
        # print(skill['rawDescription'][skill['rawDescription'].find('%(Description)')+len('%(Description)'):skill['rawDescription'].rfind('%(')])
        skill['Description'] = (skill['rawDescription'][skill['rawDescription'].find('%(Description)')+len('%(Description)'):skill['rawDescription'].rfind('%(')])
        #print(skill['Description'])
        if skill['Description'] == '':
            skill['Description'] = (skill['rawDescription'][skill['rawDescription'].find('%(Description)')+len('%(Description)'):])

    if '%(ChargeUp)' in skill['rawDescription']:
        # print(skill['rawDescription'][skill['rawDescription'].find('%(ChargeUp)')+len('%(ChargeUp)'):skill['rawDescription'].rfind('%(')])
        skill['ChargeUp'] = (skill['rawDescription'][skill['rawDescription'].find('%(ChargeUp)')+len('%(ChargeUp)'):skill['rawDescription'].rfind('%(')])
        if skill['ChargeUp'] == '':
            skill['ChargeUp'] = (skill['rawDescription'][skill['rawDescription'].find('%(ChargeUp)')+len('%(ChargeUp)'):])
    return skill

#
# skill = getSkillName(655)
# #print(skill)
# import json
# print(json.dumps(skill, indent=4, sort_keys=True))
