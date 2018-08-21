def get_dist_name(code):
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
    return code_to_name[code]
