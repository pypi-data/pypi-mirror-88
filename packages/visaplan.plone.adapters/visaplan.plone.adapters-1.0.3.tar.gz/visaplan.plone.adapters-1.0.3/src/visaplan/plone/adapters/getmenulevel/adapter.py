# -*- coding: utf-8 -*- äöü vim: filetype=python
"""
Adapter unitracc->getmenulevel: Hauptmenü erzeugen

siehe auch (gf):
../../browser/navigation/browser.py
"""
# Python compatibility:
from __future__ import absolute_import

# Standard library:
from pprint import pformat

# Zope:
from zope.interface import implements
from Products.CMFCore.utils import getToolByName

# 3rd party:
from DateTime import DateTime

# visaplan:
from visaplan.plone.base import Base, Interface

# Logging / Debugging:
from visaplan.plone.tools.log import getLogSupport
from visaplan.tools.debug import log_or_trace

logger, debug_active, DEBUG = getLogSupport(defaultFromDevMode=False)

lot_kwargs = {'debug_level': debug_active,
              'logger': logger,
              'log_args': True,
              'log_result': True,
              }


class IGetMenuLevel(Interface):
    pass


class Adapter(Base):
    implements(IGetMenuLevel)
    """
    Argumente:

    brain -- wenn übergeben, ist dies der Ausgangspunkt (ansonsten der Kontext)
    ...
    filter -- wenn True, wird nach Veröffentlichungs- und Ablaufdatum gefiltert
    plain -- filtert nur nach dem Veröffentlichungsstatus

    Es kann nur entweder filter oder plain "aktiviert" werden; Vorgabe ist filter=True.
    """

    @log_or_trace(trace_key='getlevel', **lot_kwargs)
    def __call__(self,
                 brain=None,
                 portal_types=None,
                 filter=True,
                 maxcount=5,
                 plain=None,
                 exclude_uids=[]):

        context = self.context
        pc = getToolByName(context, 'portal_catalog')

        query = {}

        if brain:
            path = brain.getPath()
        else:
            tup = context.getPhysicalPath()
            path = '/'.join(tup)

        if portal_types:
            query['portal_type'] = portal_types

        if filter:
            assert not plain
            time = DateTime()
            query['expires'] = {'query': time, 'range': 'min'}
            query['effective'] = {'query': time, 'range': 'max'}
            query['getExcludeFromNav'] = False
            query['_plan'] = False  # TH: ??? (dokumentieren)
            query['review_state'] = ['inherit',
                                     'published',
                                     'visible',
                                     'restricted',
                                     ]
        elif plain:
            query['getExcludeFromNav'] = False
            query['review_state'] = ['inherit',
                                     'published',
                                     'visible',
                                     'restricted',
                                     ]

        query['sort_on'] = 'getObjPositionInParent'
        query['path'] = {'query': path,
                         'depth': 1}
        if debug_active:
            DEBUG('[ query = \\\n%s\n ]', pformat(query))

        if exclude_uids:
            exclude_uids = set(exclude_uids)
            raw_list = [brain
                        for brain in pc(query)
                        if brain.UID not in exclude_uids
                        ]
        else:
            raw_list = pc(query)
        if maxcount is None:
            return raw_list
        else:
            return raw_list[:maxcount]
