import sys


excluded_names = None
included_names = None

mode = None
for a in sys.argv:
    if a.startswith('--include='):
        included_names = a[10:].strip().split(',')
    if a.startswith('--exclude='):
        excluded_names = a[10:].strip().split(',')
    if a.startswith('--mode='):
        mode = a[7:]

current_name = None
for l in sys.stdin:
    if l.startswith('-- Name: '):
        current_name = l[9:l.find(';')]
        tp = l[l.find('Type: ') + 6:l.find(';', l.find('Type: '))]
        if 'Type: SEQUENCE' in l:
            # same name as its table
            if mode in ['list']:
                print tp + ':', current_name
        else:
            if mode in ['list']:
                print tp + ':', current_name
    if l.startswith('-- Data for Name: '):
        current_name = l[18:l.find(';')]
        if mode in ['list']:
            print 'DATA:', current_name


    is_active = True
    if included_names is not None:
        is_active = current_name in included_names
    if excluded_names is not None:
        is_active = current_name not in excluded_names

    if not is_active:
        continue
    if mode in [None, 'filter']:
        print l,

