# -*- coding: utf-8 -*- äöü
# Konfigurationsmodul für userlog/grouplog
# Python compatibility:
from __future__ import absolute_import

# Standard library:
from os import linesep, readlink
from os.path import islink

# Zope:
from App.config import getConfiguration

# visaplan:
from visaplan.plone.tools.cfg import get_raw_config  # , split_filename

# Logging / Debugging:
from visaplan.plone.tools.log import getLogSupport

logger, debug_active, DEBUG = getLogSupport(fn=__file__)


def get_configuration(product='userlog'):
    """
    Ermittle die Konfiguration; gib ein dict zurück
    """
    confdict = get_raw_config(product)

    zopeconf = getConfiguration()
    try:
        USERLOG = zopeconf.environment['USERLOG']
        if islink(USERLOG):
            logger.info('%r is a symbolic link' % USERLOG)
            try:
                USERLOG = readlink(USERLOG)
            except ImportError:
                pass
        logger.info('USERLOG (environment) ist %r' % USERLOG)
    except KeyError:
        USERLOG = None
    users_file = None
    if USERLOG is not None:
        users_file = confdict.get('users_file')
        if users_file:
            if users_file == USERLOG:
                logger.info('USERLOG (environment) wird nicht mehr benoetigt')
            else:
                logger.warning('USERLOG (environment) %(USERLOG)r '
                        'uebersteuert durch Produktkonfiguration!',
                        locals())
        else:
            logger.warning('Bitte Produktkonfiguration ergaenzen:'
                '\n    <product-config %(product)s>'
                '\n    users_file  %(USERLOG)s'
                '\n    groups_file ...'
                '\n    </product-config>',
                locals())
            confdict['users_file'] = users_file = USERLOG
    if users_file:
        logger.info('Logging users to %(users_file)s', locals())
    else:
        confdict['users_file'] = None
        logger.warning('Logging users OFF', locals())
    groups_file = confdict.get('groups_file')
    if 'groups_file' not in confdict:
        if users_file:
            tail = 'users.txt'
            if users_file.lower().endswith(tail):
                confdict['groups_file'] = users_file[:-len(tail)]+'groups.txt'
            else:
                confdict['groups_file'] = None
        else:
            confdict['groups_file'] = None
    elif not groups_file:
        confdict['groups_file'] = None
    if groups_file:
        logger.info('Logging groups to %(groups_file)s', locals())
    else:
        logger.warning('Logging groups OFF', locals())
    return confdict


COMPLAINT = 'USERLOG nicht konfiguriert! (zope.conf, <environment>)'
DIVIDE = linesep + (79 * '-') + linesep

CONFDICT = get_configuration()
USERLOG = CONFDICT['users_file']
GROUPLOG = CONFDICT['groups_file']
