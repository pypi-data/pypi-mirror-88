# -*- coding: utf-8 -*- äöü
# utils-Modul für userlog-Adapter

def sorted_items(dic):
    flavour = dic.pop('flavour', 'DB')
    ignored_keys = []
    group_keys = ['group_id']
    member_keys = ['member_id']
    if flavour == 'DB':
        group_keys.append('group_id_')
        member_keys.append('member_id_')
        ignored_keys = ['id']
    elif flavour in ('curse', 'course'):
        raise ValueError('Felder für flavour "course" noch nicht definiert!')
    else:
        raise ValueError('Felder für flavour %(flavour)r noch nicht definiert!'
                         % locals())

    sortable = []
    # Schlüssel für Gruppierung einfügen:
    for key in dic.keys():
        if key in ignored_keys:
            continue
        if key in group_keys:
            sortable.append((0, key))
        elif key == 'group_title':
            sortable.append((10, key))
        elif key in member_keys:
            sortable.append((20, key))
        elif key.startswith('member'):
            sortable.append((30, key))
        elif key.startswith('active'):
            sortable.append((62, key))
        elif key == 'start':
            sortable.append((50, key))
        elif key == 'ends':
            sortable.append((60, key))
        elif key in ('ip', 'hostname'):
            sortable.append((70, key))
        elif key == 'by':
            sortable.append((80, key))
        elif key == 'done':  # erledigt?
            sortable.append((90, key))
        elif key.endswith('password'):
            # Paßwörter nicht protokollieren!
            # (sollten bei Gruppen ohnehin nicht vorkommen ...)
            continue
        elif dic[key] is None:
            # Schlüssel mit leeren Werten ignorieren
            continue
        else:
            sortable.append((70, key))
    sortable.sort()
    return [(tup[1], dic[tup[1]])
            for tup in sortable
            ]
