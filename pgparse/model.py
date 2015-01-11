# -*- coding: utf-8 -*-
import sys


class DumpSection(object):
    def __init__(self, name=None, tp=None, details=None, content='', is_data=False, line=None):
        self.name = name
        self.tp = tp
        self.details = details or {}
        self.is_data = is_data
        self.content = content or ''
        self.line = line

    def add_content_line(self, l):
        self.content += l

    def get_full_section(self):
        return '--\n-- {}--\n{}'.format(self.line, self.content)


class PGDump(object):
    def __init__(self):
        self.sections = []

    def add_section(self, s):
        self.sections.append(s)

    def add_line(self, l):
        if not self.sections:
            raise ValueError('No section!')
        self.sections[-1].add_content_line(l)

    def get_section_types(self):
        d = {}
        for s in self.sections:
            if s.is_data:
                continue
            d[s.tp] = d.get(s.tp, 0) + 1
        return d

    @classmethod
    def parse(cls, dump_file):
        dump = PGDump()
        started = False
        for l in dump_file:
            is_data = False
            if l.startswith('-- Name: '):
                l = l[3:]
            elif l.startswith('-- Data for Name: '):
                is_data = True
                l = l[12:]
            elif l.startswith('--') and not l[2:].strip():
                continue  # comment
            elif l.startswith('-- PostgreSQL database dump'):
                # start and end
                s = DumpSection(name='PostgreSQL database dump', tp='PostgreSQL', line=l)
                dump.add_section(s)
                continue
            elif l.startswith('--'):
                print('Unknown start of section: "{}{}"'.format(l[2:15].strip(), '...' if len(l) > 15 else ''),
                      file=sys.stderr)
                continue
            else:
                if started:
                    dump.add_line(l)
                continue

            started = True
            details = {}
            for d in l.split(';'):
                ind = d.find(':')
                if ind > -1:
                    k = d[:ind]
                    v = d[ind + 1:].strip()
                else:
                    k = d
                    v = True
                details[k.strip().lower()] = v
            current_name = details.pop('name')
            tp = details.pop('type', 'none')
            s = DumpSection(name=current_name, tp=tp, details=details, is_data=is_data, line=l)
            dump.add_section(s)
        return dump
