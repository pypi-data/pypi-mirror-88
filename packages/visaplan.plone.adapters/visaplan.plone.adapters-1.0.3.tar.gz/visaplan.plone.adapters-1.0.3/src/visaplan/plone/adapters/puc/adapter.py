# Python compatibility:
from __future__ import absolute_import

# Zope:
from Products.CMFCore.utils import getToolByName

# visaplan:
from visaplan.plone.base import Base, Interface


class IPortalUserCatalog(Interface):
    pass


class Adapter(Base):

    def __call__(self):
        return getToolByName(self.context, 'portal_user_catalog')
