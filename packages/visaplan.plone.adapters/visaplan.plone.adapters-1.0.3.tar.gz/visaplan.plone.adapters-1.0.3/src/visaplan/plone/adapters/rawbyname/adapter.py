# -*- coding: utf-8 -*- äöü
# Python compatibility:
from __future__ import absolute_import, print_function

# visaplan:
from visaplan.plone.base import Base, Interface

# Logging / Debugging:
import logging

logger = logging.getLogger('unitracc->rawbyname')
# visaplan:
from visaplan.plone.tools.cfg import get_debug_active

# Logging / Debugging:
import pdb
from visaplan.tools.debug import asciibox, pp

debug_active = get_debug_active('rawbyname')

# wenn False, sind Debugging-Funktionalitäten incl. etwaiger
# pdb.set_trace-Aufrufe abgeschaltet
DEBUG = 0 and debug_active


class IRawByName(Interface):
    pass


class Adapter(Base):

    def __call__(self, name):
        context = self.context
        try:
            if DEBUG:
                localdebug = 0
                if hasattr(context, 'Schema'):
                    keys = list(context.Schema().keys())
                    pp((('%(context)r.Schema().keys():' % locals(), keys),
                        ('Name %(name)r enthalten:' % locals(), name in keys),
                        ))
                    if name not in keys:
                        localdebug = 1
                else:
                    print('%r hat kein Attribut %r' % (context, 'Schema'))
                    localdebug = 1
                if localdebug:
                    pdb.set_trace()
            field = context.getField(name)
        except AttributeError as e:
            logger.error('%(context)r.getField(%(name)r):', locals())
            logger.exception(e)
            print(asciibox('Adapter rawbyname: %s(%s)'
                           % (e.__class__.__name__, e)))
            pp((('context:', context),
                ('...field...-Attribute:',
                 [a for a in dir(context)
                    if 'field' in a.lower()
                    ]),
                 ))
            if DEBUG:
                pdb.set_trace()
            raise
        else:
            # print 'field:', field
            # (z. B. <Field text(text:rw)>)
            if field is not None:
                try:
                    return field.getRaw(context)
                except AttributeError as e:
                    logger.error('%(context)r.getField(%(name)r):', locals())
                    logger.exception(e)
                    raise
            else:
                logger.error('%(context)r has no field %(name)r', locals())
