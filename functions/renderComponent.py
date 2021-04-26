def getInfo(conn, data, comp_id):

    cur = conn.cursor()
    cur.execute("SELECT id, icon_asset FROM RenderComponent")
    rows = cur.fetchall()
    icon_path = None
    for row in rows:
        if row[0] == comp_id:
            icon_path = row[1]
            break

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

