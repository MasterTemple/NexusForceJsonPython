def getName(lti):
    import json
    with open('work/LootTableIndexNames.json') as f:
        names = json.load(f)

        data = names['data'][lti]

    return data
