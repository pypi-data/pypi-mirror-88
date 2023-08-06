# -*- coding: utf-8 -*- äöü
# utils-Modul für userlog-Adapter

def sorted_items(dic):
    sortable = []
    # Schlüssel für Gruppierung einfügen:
    for key in dic.keys():
        if key in ('userId',
                   'username',
                   ):
            sortable.append((0, key))
        elif key in ('ip', 'hostname'):
            sortable.append((7, key))
        elif key.endswith('name'):
            sortable.append((1, key))
        elif key == 'email':
            sortable.append((2, key))
        elif key == 'by':
            sortable.append((9, key))
        elif key.endswith('password'):
            # Paßwörter nicht protokollieren!
            continue
        elif dic[key] is None:
            # Schlüssel mit leeren Werten ignorieren
            continue
        else:
            sortable.append((5, key))
    sortable.sort()
    return [(tup[1], dic[tup[1]])
            for tup in sortable
            ]
