def makePretty(data):
    data = equipLocation(data)
    return data

def equipLocation(data):
    data['itemComponent']['equipLocationNames'] = []

    for i in data['itemComponent']['equipLocation']:
        if 'special_l' in data['itemComponent']['equipLocation']:
            data['itemComponent']['equipLocationNames'].append('Left Hand')
        elif 'special_r' in data['itemComponent']['equipLocation']:
            data['itemComponent']['equipLocationNames'].append('Right Hand')
        elif 'hair' in data['itemComponent']['equipLocation']:
            data['itemComponent']['equipLocationNames'].append('Headgear')
        elif 'clavicle' in data['itemComponent']['equipLocation']:
            data['itemComponent']['equipLocationNames'].append('Neck/Back')
        elif 'chest' in data['itemComponent']['equipLocation']:
            data['itemComponent']['equipLocationNames'].append('Torso')
        elif 'legs' in data['itemComponent']['equipLocation']:
            data['itemComponent']['equipLocationNames'].append('Pants')
        else:
            data['itemComponent']['equipLocationNames'].append(data['itemComponent']['equipLocation'][i])

    return data

