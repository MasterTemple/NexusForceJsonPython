def getInfo(conn, data, comp_id):

    cur = conn.cursor()
    cur.execute("SELECT id, icon_asset FROM RenderComponent WHERE id=?", (comp_id,))
    row = cur.fetchone()
    #icon_path = None
    icon_path = row[1]

    if icon_path is not None:
        icon_path = icon_path.replace('.DDS', '.png')
        icon_path = icon_path.replace('.dds', '.png')
        icon_path = icon_path.replace("\\\\", "/")
        icon_path = icon_path.replace("\\", "/")
        icon_path = icon_path.replace(' ', "%20")
        icon_path = icon_path.lower()
        data['iconURL'] = icon_path[6:len(icon_path)]
    else:
        data['iconURL'] = 'unknown'

    return data

