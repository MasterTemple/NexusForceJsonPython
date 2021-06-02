import copy


def objects(data):
    reformatted_data = {}
    reformatted_data["object_id"] = data['objectID']
    reformatted_data["components"] = data['components']
    reformatted_data["item_info"] = data['itemInfo']
    reformatted_data['skills'] = []
    if '11' not in data['components'].keys():
        return reformatted_data
    reformatted_data['stats'] = {"life": 0, "armor": 0, "imagination": 0}

    for skill in data['objectSkills']:
        try:
            obj = {
                'imagination_cost': data['objectSkills'][skill]['imaginationcost'],
                'cooldown': data['objectSkills'][skill]['cooldown'],
                'cooldown_group': data['objectSkills'][skill]['cooldowngroup'],
                'name': data['objectSkills'][skill]['info']['name'],
                'full_description': data['objectSkills'][skill]['info']['rawDescription'],
            }
            try:
                obj['charge_up'] = data['objectSkills'][skill]['info']['ChargeUp']
            except:
                pass
            try:
                obj['damage_combo'] = data['objectSkills'][skill]['info']['damageCombo']
            except:
                pass
            try:
                obj['description'] = data['objectSkills'][skill]['info']['Description']
            except:
                pass

            reformatted_data['skills'].append(obj)
        except:
            pass

    try:
        reformatted_data['preconditions'] = data['itemComponent']['preconditionDescriptions']
    except:
        reformatted_data['preconditions'] = {}


    try:
        reformatted_data['stats']['life'] = data['stats']['lifeBonusUI']
    except:
        reformatted_data['stats']['life'] = 0
    try:
        reformatted_data['stats']['armor'] = data['stats']['armorBonusUI']
    except:
        reformatted_data['stats']['armor'] = 0
    try:
        reformatted_data['stats']['imagination'] = data['stats']['imBonusUI']
    except:
        reformatted_data['stats']['imagination'] = 0


    try:
        reformatted_data['rarity'] = data['itemComponent']['rarity']
    except:
        reformatted_data['rarity'] = 0

    try:
        if data['itemComponent']['isWeapon'] == True:
            reformatted_data['is_weapon'] = 1
        else:
            reformatted_data['is_weapon'] = 0
    except:
        reformatted_data['is_weapon'] = 0

    try:
        reformatted_data['is_two_handed'] = data['itemComponent']['isTwoHanded']
    except:
        reformatted_data['is_two_handed'] = 0

    try:
        reformatted_data['level_requirement'] = data['itemComponent']['levelRequirement']
    except:
        reformatted_data['level_requirement'] = 0

    if len(data['itemComponent']['equipLocationNames']) > 0:
        reformatted_data['equip_locations'] = data['itemComponent']['equipLocationNames']
    else:
        reformatted_data['equip_locations'] = ['Consumable']
    try:
        if data['itemComponent']["sellPrice"] is not None:
            reformatted_data['sell_price'] = data['itemComponent']["sellPrice"]
        else:
            reformatted_data['sell_price'] = 0
    except:
        reformatted_data['sell_price'] = 0

    try:
        if data['itemComponent']["buyPrice"] is not None:
            reformatted_data['buy_price'] = data['itemComponent']["buyPrice"]
        else:
            reformatted_data['buy_price'] = 0
    except:
        reformatted_data['buy_price'] = 0
    try:
        if data['itemComponent']["altCurrencyType"] is not None:
            reformatted_data['alt_currency_type'] = data['itemComponent']["altCurrencyType"]
        else:
            reformatted_data['alt_currency_type'] = 0
    except:
        reformatted_data['alt_currency_type'] = 0

    try:
        if data['itemComponent']["altCurrencyCost"] is not None:
            reformatted_data['alt_currency_cost'] = data['itemComponent']["altCurrencyCost"]
        else:
            reformatted_data['alt_currency_cost'] = 0
    except:
        reformatted_data['alt_currency_cost'] = 0

    try:
        if data['itemComponent']["commendationCurrencyType"] is not None:
            reformatted_data['commendation_currency_type'] = data['itemComponent']["commendationCurrencyType"]
        else:
            reformatted_data['commendation_currency_type'] = 0
    except:
        reformatted_data['commendation_currency_type'] = 0

    try:
        if data['itemComponent']["commendationCurrencyCost"] is not None:
            reformatted_data['commendation_currency_cost'] = data['itemComponent']["commendationCurrencyCost"]
        else:
            reformatted_data['commendation_currency_cost'] = 0
    except:
        reformatted_data['commendation_currency_cost'] = 0

    try:
        reformatted_data['stack_size'] = data['itemComponent']['stackSize']
    except:
        reformatted_data['stack_size'] = 1
    try:
        reformatted_data['overview'] = data['overview']
    except:
        pass


    if len(data['buyAndDrop']['VendorIDs']) > 0:
        reformatted_data['is_sold'] = 1
        reformatted_data['vendors'] = []
        for each_vendor in data['buyAndDrop']['Vendors']:
            if each_vendor['displayName'] is not None:
                vendor = {
                    "id": each_vendor['id'],
                    "name": each_vendor['displayName'],
                }
                reformatted_data['vendors'].append(vendor)
    else:
        reformatted_data['is_sold'] = 0

    if len(data['earn'].keys()) > 0:
        reformatted_data['is_earned'] = 1
        reformatted_data['missions'] = []
        for each_mission in data['earn'].keys():
            mission = {
                "mission_id": each_mission,
                "defined_type": data['earn'][each_mission]['defined_type'],
                "defined_subtype": data['earn'][each_mission]['defined_subtype'],
                "missionName": data['earn'][each_mission]['missionName'],
                "mission_description": data['earn'][each_mission]['missionDescription'],
                "is_mission": data['earn'][each_mission]['isMission'],
                "rewardCount": data['earn'][each_mission]['rewardCount']
            }
            reformatted_data['missions'].append(mission)
    else:
        reformatted_data['is_earned'] = 0

    if len(data['buyAndDrop']['EnemyIDs']) > 0:
        reformatted_data['is_dropped'] = 1
        reformatted_data['drops'] = []
        for each_drop in data['buyAndDrop']['LootMatrixIndexes'].keys():
            # try:
            #print(each_drop)
            try:
                data['buyAndDrop']['LootMatrixIndexes'][each_drop]['minToDrop']
            except:
                data['buyAndDrop']['LootMatrixIndexes'][each_drop]['minToDrop'] = data['buyAndDrop']['LootMatrixIndexes'][each_drop]['maxToDrop']
            if data['buyAndDrop']['LootMatrixIndexes'][each_drop]['minToDrop'] == data['buyAndDrop']['LootMatrixIndexes'][each_drop]['maxToDrop']:
                drop = {
                    "percent": data['buyAndDrop']['LootMatrixIndexes'][each_drop]['overallChance']['percent'],
                    "fraction": {
                        "numerator": data['buyAndDrop']['LootMatrixIndexes'][each_drop]['minToDrop'],
                        "denominator": data['buyAndDrop']['LootMatrixIndexes'][each_drop]['overallChance']['howManyToKill'] * (data['buyAndDrop']['LootMatrixIndexes'][each_drop]['minToDrop']),
                    }
                }
            else:
                drop = {
                    "percent": data['buyAndDrop']['LootMatrixIndexes'][each_drop]['overallChance']['percent'],
                    "fraction": {
                        "numerator": data['buyAndDrop']['LootMatrixIndexes'][each_drop]['minToDrop']+data['buyAndDrop']['LootMatrixIndexes'][each_drop]['maxToDrop'],
                        "denominator": data['buyAndDrop']['LootMatrixIndexes'][each_drop]['overallChance']['howManyToKill'] * (data['buyAndDrop']['LootMatrixIndexes'][each_drop]['maxToDrop'] - data['buyAndDrop']['LootMatrixIndexes'][each_drop]['minToDrop']+1),
                    }
                }
            for package in data['buyAndDrop']['LootMatrixIndexes'][each_drop]['PackageComponent'].keys():
                try:
                    drop["type"] = 'Package',
                    drop["name"] = data['buyAndDrop']['LootMatrixIndexes'][each_drop]['PackageComponent'][package]['displayName']
                    drop["id"] = package
                    drop["type"] = drop["type"][0]
                    drop["name"] = drop["name"][0]
                    reformatted_data['drops'].append(copy.deepcopy(drop))
                except:
                    pass
            for enemy in data['buyAndDrop']['LootMatrixIndexes'][each_drop]['DestructibleComponent'].keys():
                try:
                    drop["type"] = 'Enemy',
                    drop["name"] = data['buyAndDrop']['LootMatrixIndexes'][each_drop]['DestructibleComponent'][enemy]['enemyNames']['displayName'],
                    drop["id"] = data['buyAndDrop']['LootMatrixIndexes'][each_drop]['DestructibleComponent'][enemy]['enemyID'],

                    drop["type"] = drop["type"][0]
                    drop["name"] = drop["name"][0]
                    drop["id"] = drop["id"][0]
                    reformatted_data['drops'].append(copy.deepcopy(drop))
                except:
                    pass
            for activity in data['buyAndDrop']['LootMatrixIndexes'][each_drop]['ActivityComponent']:
                try:
                    drop["type"] = 'Activity'
                    drop["name"] = activity

                    reformatted_data['drops'].append(copy.deepcopy(drop))
                except:
                    pass


            # except:
            #     pass

    else:
        reformatted_data['is_dropped'] = 0

    return reformatted_data