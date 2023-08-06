# -*- coding: utf-8 -*-
# Adapter pformat: Zugriff auf die Standardfunktion pprint.pformat
# Python compatibility:
from __future__ import absolute_import

# Standard library:
from pprint import pformat

# visaplan:
from visaplan.plone.base import Base, Interface


class IPFormat(Interface):
    pass


class Adapter(Base):

    def __call__(self, *args, **kwargs):
        return pformat(*args, **kwargs)

#  vim: ts=8 sts=4 sw=4 si et tw=79
