#!/usr/bin/env python3
import sys
from pprint import pprint

from pgparse.model import PGDump


def main():
    excluded_names = None
    included_names = None

    mode = None
    for a in sys.argv:
        if a.startswith('--include='):
            included_names = a[10:].strip().split(',')
        if a.startswith('--exclude='):
            excluded_names = a[10:].strip().split(',')
        if a.startswith('--mode='):
            mode = a[7:].lower()

    if not mode:
        mode = 'help'

    dump = PGDump.parse(sys.stdin)

    if mode == 'help':
        print('usage: pg-parse --mode=[summary|filter|help]')

    elif mode == 'summary':
        pprint(dump.get_section_types())

    elif mode == 'filter':
        def filter_sections(section):
            if included_names is not None:
                if section.name not in included_names:
                    return False
            if excluded_names is not None:
                if section.name in excluded_names:
                    return False
            return True

        for s in dump.sections:
            if filter_sections(s):
                print(s.get_full_section())

    else:
        print('Invalid mode given')


if __name__ == '__main__':
    main()
