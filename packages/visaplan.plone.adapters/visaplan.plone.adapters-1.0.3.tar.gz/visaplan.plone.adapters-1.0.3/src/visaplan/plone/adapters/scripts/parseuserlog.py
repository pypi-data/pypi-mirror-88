#!/usr/bin/env python
# -*- coding: utf-8 -*- äöü vim: ts=8 sts=4 sw=4 si et
# Python compatibility:
from __future__ import absolute_import, print_function

from six.moves import map
from six.moves.urllib.parse import urlparse

# Standard library:
import re
import sys
from collections import Counter, defaultdict
from csv import DictWriter
from os import getcwd, linesep
from os.path import (
    curdir,
    exists,
    isdir,
    isfile,
    join,
    normpath,
    pardir,
    relpath,
    sep,
    splitext,
    )
from string import strip

# 3rd party:
from DateTime import DateTime

try:
    # 3rd party:
    from thebops.optparse import OptionGroup, OptionParser
except ImportError:
    from optparse import OptionParser, OptionGroup

# visaplan:
from visaplan.tools.dicts import subdict
# registers the excel_ssv dialect:
from visaplan.tools.csvfiles import csv_writer

fieldnames = [
    'email', 'firstname', 'lastname', 'username',
    'hostname', 'language',
    'DATE', 'locked', 'terms', 'DATE_LOCKED', 'DATE_CONFIRMED',
    ]

def make_parser():
    p = OptionParser(add_help_option=0,
                     usage="%prog [options] [users.txt] [users.csv]")
    p.  version='%prog 0.1'
    p.set_description('Parse a users.txt "user log file", written by the userlog '
        'adapter (from visaplan.plone.adapters), '
        'and create a CSV file which is suitable for office processing.')

    g = OptionGroup(p, 'Input')
    g.add_option('--input', '-F',
                 action="store",
                 dest="input_file",
                 type="string",
                 help="The file name to read; by default, the following "
                 "directories are searched for a suitable users.txt: "
                 '1) ../var/log/, relative to the dir containing this program; '
                 '2) var/log/, relative to the current working dir; '
                 '3) the current working dir. '
                 'If not given, a 1st positional argument is used.')
    p.add_option_group(g)

    g = OptionGroup(p, 'Filters')
    g.set_description('Currently, all filters are hardcoded.')
    g.add_option('--language', '--lang',
                 action="store",
                 dest="language",
                 type="string",
                 help="The language which was used; currently, this is "
                 'taken from the form_submit text from the self-registration form.'
                 ' (NOT YET IMPLEMENTED)')
    p.add_option_group(g)

    g = OptionGroup(p, 'Skip old entries')
    g.set_description('Currently, all entries before the first one with a '
        'host name information containing "catt" are ignored.  While such a '
        'criterion might be useful for other future cases as well, '
        'one might need something like a date criterion.')
    g.add_option('--ignore-before',
                 action="store",
                 dest="ignore_before",
                 type="string",
                 help="A date to tell which entries are too old to be of any "
                 'interest '
                 ' (NOT YET IMPLEMENTED)'
                 '. If, however, a user e.g. confirms his/her registration after '
                 'this date while having registered before it, the whole informa'
                 'tion needs to be included.')
    p.add_option_group(g)

    g = OptionGroup(p, 'Output')
    g.add_option('--output', '--to',
                 action="store",
                 dest="output_file",
                 metavar='users.csv',
                 type="string",
                 help="The name of the CSV file to write; "
                 "./users.csv by default")
    g.add_option('--force',
                 action="store_true",
                 help='Overwrite existing output')
    p.add_option_group(g)

    g = OptionGroup(p, 'Output format')
    g.add_option('--timezone',
                 action="store",
                 type="string",
                 metavar="UTC",
                 help="time zone name to be used for date/time values; "
                 'if not specified, the unchanged date/time values will be '
                 'written, with their original timezone info included')
    g.add_option('--fields',
                 action="append",
                 type="string",
                 metavar="email,firstname,lastname,language,...",
                 help= "Currently the following fields are written: "
                 + ','.join(fieldnames) + '; '
                 'some of these will become the default. '
                 "(NOT YET IMPLEMENTED) "
                 "TODO: create a callback function to add (optional +prefix) "
                 "or remove (-prefix) entries to/from the list.")
# see: https://docs.python.org/2/library/csv.html#csv-fmt-params
    g.add_option('--csv-dialect',
                 action="store",
                 default='excel_ssv',  # our own: ... semicolon separated
                 metavar="%default",
                 help='The CSV "dialect" to use, by default: "%default". '
                 '(NOT YET IMPLEMENTED)')
    g.add_option('--csv-delimiter',
                 action="store",
                 default=',',
                 metavar=",|;",
                 help='The field delimiter character to use; "%default" '
                 'by default. '
                 '(NOT YET USED) '
                 'Note that MS Excel doesn\'t seem to like the "excel" dialect '
                 'unless the delimiter is changed to the semicolon ";".'
                 )
    g.add_option('--strftime',
                 action="store",
                 help='The strftime format specification for date values'
                 ' (NOT YET IMPLEMENTED)')
    p.add_option_group(g)

    g = OptionGroup(p, 'Everyday options')
    g.add_option('--help', '-h', '-?',
                 action="help",
                 help="Display this help and exit")
    g.add_option('--version', '-V',
                 action="version",
                 help="Display the version and exit")
    p.add_option_group(g)
    return p

ok = 1
def err(txt):
    global ok
    sys.stderr.write('E: ' + txt + linesep)
    ok = 0

def info(txt):
    sys.stderr.write('i: ' + txt + linesep)

def parse_args(p):
    """
    p -- the parser
    """
    o, a = p.parse_args()

    if not o.input_file and a:
        o.input_file = a.pop(0)

    if o.input_file:
        _, ext = splitext(o.input_file)
        if ext.lower() != '.txt':
            err('.txt file expected (%s)' % (o.input_file,))
    else:
        found = False
        dirs = [relpath(join(__file__, pardir, pardir, 'var/log')),
                'var/log',
                curdir]
        for d in dirs:
            fn = normpath(join(d, 'users.txt'))
            if isfile(fn):
                found = True
                o.input_file = fn
                info('Reading %(fn)s' % locals())
                break
            elif exists(fn):
                err('%(fn)s is not a file!' % locals())
        if not found:
            err('No input file found.')

    if not o.output_file and a:
        o.output_file = a.pop(0)

    if o.output_file:
        if isdir(o.output_file):
            o.output_file = normpath(join(o.output_file, 'users.csv'))
        _, ext = splitext(o.output_file)
        if ext.lower() != '.csv':
            err('.csv file expected (%s)' % (o.output_file,))
    else:
        o.output_file = 'users.csv'
    if isfile(o.output_file):
        if not o.force:
            err("Won't overwrite %s (unless --force specified)" % (o.output_file,))
    elif exists(o.output_file):
        err("%s exists and is not a file" % (o.output_file,))

    if a:
        for arg in a:
            err('Unused argument: %(arg)r' % locals())

    if not ok:
        raise SystemExit(1)
    return o, a

cnt = Counter()
users = {}

RE = re.compile(r'^(?P<DATE>[-0-9]+ [:0-9]+ [A-Z]+) '
                r'[(]\w+[)] '
                r'(?P<SUBJECT>User|Profile) '
                r'(?P<ACTION>[^:]+)'
                ':\s*$')
BRACED = re.compile('^(?P<VAL>[^ ]+)'
                    ' +[(]'
                    '(?P<BRACE>[^)]*)'
                   r'[)]\s*$')
DASHES_ONLY = set('-')

def process_entry(dic, skip):
    """
    Der Eintrag ist abgeschlossen (Leerzeile oder Dateiende gefunden);
    nun wird er verarbeitet.

    dic -- ein Dictionary, aus aufeinanderfolgenden Eingabezeilen erzeugt
    skip -- wenn False, werden die Daten jedenfalls verwertet;
            ansonsten werden sie inspiziert und ggf. True zurückgegeben
    """
    subject = dic.get('SUBJECT')
    if not subject:
        cnt['invalid'] += 1
        return
    if subject != 'User':
        cnt[('ignored', subject)] += 1
        return
    username = None
    for key in ('username', 'userId'):
        val = dic.get(key)
        if not val:
            continue
        elif username is not None and val != username:
            cnt[('invalid', 'usernames', val, username)]
        else:
            username = val

    if not username:
        cnt[('invalid', 'username')]
        return

    if 'language' not in dic:
        submit = dic.get('form_submit')
        if submit == 'Register':
            dic['language'] = 'en'
        elif submit == 'Registrieren':
            dic['language'] = 'de'

    # hostnames
    if 'hostname' not in dic:
        key = 'last_referer'
        tmp = dic.get(key)
        if tmp:
            hostname = urlparse(tmp).netloc
            if hostname:
                dic['hostname'] = hostname
                dic['hostname_source'] = key
    elif 'hostname_source' not in dic:
        tmp = BRACED.match(dic['hostname'])
        if tmp:
            tmp = tmp.groupdict()
            dic['hostname'] = tmp['VAL']
            dic['hostname_source'] = tmp['BRACE']

    res = False
    if skip:
        for key in ('hostname',):
            val = dic.get(key)
            if not val:
                continue
            if 'catt' in val:
                res = True
                skip = False
                info('Match for %(val)r (%(key)s)' % locals())
            elif 'staging.unitracc' in val:
                # die wollen wir schon auch wissen ...
                skip = False

    action = dic['ACTION']
    if 'agbs' in dic:
        dic['terms'] = dic.pop('agbs')
        if dic['terms'] == 'False':
            dic['USED'] = False
            cnt['terms unconfirmed'] += 1

    if action in ('created', 'registered'):
        if 'USED' not in dic:
            dic['USED'] = res or not skip
        users[username] = dic
        cnt[action] += 1
    elif action == 'confirmed':
        action_update = {
            'locked': '',
            'DATE_CONFIRMED': dic['DATE'],
            }
        udic = users.get(username)
        if udic is None:
            cnt['jumped-in'] += 1
            udic = dic
            users[username] = udic
        else:
            cnt[action] += 1
        udic.update(action_update)
    elif action == 'deleted':
        info('User %(username)r %(action)s' % locals())
        cnt[action] += 1
        if username in users:
            del users[username]
    elif action in ('locked', 'unlocked'):
        locked = dic.get('locked')
        if not locked:
            locked = dic.get('by')
            if locked:
                locked = action +' by '+locked
            else:
                cnt[(action, 'info missing')] += 1
                locked = '(info missing)'

        action_update = {
            'locked': locked,
            'DATE_LOCKED': dic['DATE'],
            }
        udic = users.get(username)
        if udic is None:
            udic = dic
            users[username] = udic
        else:
            cnt[action] += 1
        udic.update(action_update)
    else:
        err('Unexpected action: %(action)r' % locals())
        cnt[action] += 1

    return res


def refine_dict(dic, timezone):
    if timezone:
        for key, val in dic.items():
            if key.startswith('DATE') and val:
                try:
                    dt = DateTime(val)
                except ValueError:
                    raise
                else:
                    dic[key] = str(dt.toZone(timezone))


def main():
    p = make_parser()
    o, a = parse_args(p)
    with open(o.input_file, 'ru') as read_from, \
         open(o.output_file, 'w') as write_to:
        dic = {}
        i = 0
        entries = 0
        skip = True
        debug_this = False
        expect_title = False
        info('Reading '+o.input_file+' ...')
        for currline in read_from.readlines():
            i += 1
            if i == 86399:
                debug_this = True and 0
            currline = currline.rstrip()
            if not currline:
                if dic:
                    if debug_this:
                        # Logging / Debugging:
                        from pdb import set_trace
                        debug_this = False
                        set_trace()
                    if process_entry(dic, skip):
                        skip = False
                    dic = {}
                    entries += 1
            elif set(currline) == DASHES_ONLY:
                expect_title = True
            elif expect_title:
                assert not dic
                dic = RE.match(currline).groupdict()
                dic['LINE'] = i
                expect_title = False
            elif ':' in currline:
                key, val = list(map(strip, currline.split(':', 1)))
                dic[key] = val
            else:
                err('Invalid line (%(i)d: %(currline)s' % locals())
                break

        if dic:
            process_entry(dic, skip)
            entries += 1
        info('%(entries)d entries in %(i)d lines' % locals())

        liz = []
        for username, dic in users.items():
            if dic.get('USED', 0):
                cnt['used'] += 1
                thedict = subdict(dic, keys=fieldnames,
                                  defaults=defaultdict(str, username=username))
                refine_dict(thedict, o.timezone)
                liz.append(thedict)
            else:
                cnt['unused'] += 1
        writer = DictWriter(write_to,
                            dialect='excel_ssv',
                            extrasaction='ignore',  # ignore other data
                            fieldnames=fieldnames)
        writer.writeheader()
        for dic in liz:
            writer.writerow(dic)

        info('%d entries written to %s' % (cnt['used'], o.output_file))

    print('')
    cnt['registered (netto)'] = cnt['registered'] - cnt['terms unconfirmed']
    for key, val in sorted(cnt.items()):
        info('%(val)4d %(key)s' % locals())


if __name__ == '__main__':
    main()
