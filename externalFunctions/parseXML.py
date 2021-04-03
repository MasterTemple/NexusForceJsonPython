

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

