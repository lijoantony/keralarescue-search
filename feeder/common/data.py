def get_dist_name(dist_search_str):
    if not dist_search_str:
        return

    code_to_name = {
              'tvm': 'Thiruvananthapuram',
              'ptm': 'Pathanamthitta',
              'alp': 'Alappuzha',
              'ktm': 'Kottayam',
              'idk': 'Idukki',
              'mpm': 'Malappuram',
              'koz': 'Kozhikode',
              'wnd': 'Wayanad',
              'knr': 'Kannur',
              'ksr': 'Kasaragod',
              'pkd': 'Palakkad',
              'tcr': 'Thrissur',
              'ekm': 'Ernakulam',
              'kol': 'Kollam'
    }
    if dist_search_str in code_to_name:
        return code_to_name[dist_search_str]

    dist_search_str = dist_search_str.strip().lower()
    for name in code_to_name.values():
        if name.lower() in dist_search_str:
            return name


def get_location_concact(location):
    (camp, addr, region) = location
    string = ''
    if camp:
        string += str(camp).strip()

    if addr and addr != '':
        if string != '':
            string += ', '
        for part in addr.split(','):
            part = part.strip()
            if part.lower() not in string.lower():
                if string != '':
                    string += ', '
                string += part

    if region and region != '':
        if string != '':
            string += ', '
        string += str(region).strip()

    return string