# -*- coding: utf-8 -*-
"""
Adapter uidorint: UID oder Ganzzahl zurückgeben

Gibt ein dict zurück, mit folgenden Schlüsseln:
    uid - wenn eine UID übergeben wurde
    number - wenn eine Ganzzahl übergeben wurde
    prefix - wenn ein Präfix wie 'rel-' oder 'uid-' enthalten war
"""
# Python compatibility:
from __future__ import absolute_import

from six import text_type as six_text_type

# visaplan:
from visaplan.plone.base import Base, Interface
from visaplan.plone.tools.forms import uid_or_number


class IUidOrInt(Interface):
    pass


class Adapter(Base):

    def __call__(self, **kwargs):
        """
        Standardverhalten: die Request-Variable 'uid' auswerten
        """
        if 'val' in kwargs:
            val = kwargs.pop('val')
        else:
            varname = kwargs.pop('varname', 'uid')
            context = self.context
            request = context.REQUEST
            val = request.get(varname, None)
        try:
            return uid_or_number(val, **kwargs)
        except Exception as e:
            if kwargs.get('strict', False):
                raise
            msg = six_text_type(e)
            if kwargs.get('onerror', 'message'):
                try:
                    context
                except NameError:
                    context = self.context
                context.getAdapter('message')(
                        msg,
                        'error')
            res = uid_or_number(None)
            res['error'] = msg
            return res

#  vim: ts=8 sts=4 sw=4 si et tw=79
