def fixPfp(npcData):
    if npcData['iconURL'] == "https://github.com/MasterTemple/lu_bot/blob/master/src/unknown.png?raw=true" and npcData['components'][16] is not None and npcData['components'][73] is None:
        npcData['iconURL'] = 'https://xiphoseer.github.io//lu-res/mesh//overhead_indicators//icon_vendor.png?raw=true'
    if npcData['iconURL'] == "https://github.com/MasterTemple/lu_bot/blob/master/src/unknown.png?raw=true" and npcData['components'][16] is None and npcData['components'][73] is not None:
        npcData['iconURL'] = 'https://xiphoseer.github.io//lu-res/mesh//overhead_indicators//icon_mission_turn_in.png?raw=true'
    if npcData['iconURL'] == "https://github.com/MasterTemple/lu_bot/blob/master/src/unknown.png?raw=true" and npcData['components'][16] is None and npcData['components'][73] is None:
        #npcData['iconURL'] = 'x'
        print(npcData['npcID'], "has problems with it's pfp")
    if npcData['iconURL'] == "https://github.com/MasterTemple/lu_bot/blob/master/src/unknown.png?raw=true" and npcData['components'][16] is not None and npcData['components'][73] is not None:
        npcData['iconURL'] = 'https://xiphoseer.github.io//lu-res/mesh//overhead_indicators//icon_mission_turn_in.png?raw=true'
    return npcData
