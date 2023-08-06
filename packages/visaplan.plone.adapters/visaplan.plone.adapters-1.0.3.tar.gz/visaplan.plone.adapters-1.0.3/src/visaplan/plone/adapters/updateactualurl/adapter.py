# Python compatibility:
from __future__ import absolute_import

# visaplan:
from visaplan.plone.base import Base, Interface


class IUpdateActualUrl(Interface):
    pass


class Adapter(Base):

    def __call__(self, url):
        context = self.context
        context.REQUEST['ACTUAL_URL'] = url
