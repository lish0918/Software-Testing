def extract_author(name):
    if ',' in name:
        surname, firstname = name.split(', ', 1)
    elif ' ' in name:
        firstname, surname = name.rsplit(' ', 1)
    else:
        return name, ''
    return surname, firstname

def extract_authors(name):
    name_list = name.split(' and ')
    return [extract_author(name) for name in name_list]
