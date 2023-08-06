# Python compatibility:
from __future__ import absolute_import

# Standard library:
import os
import sys
from optparse import OptionParser

# Zope:
from App.config import getConfiguration

# visaplan:
from visaplan.plone.base import Base, Interface

# Local imports:
from .flvlib import __versionstr__, helpers, tags

# Logging / Debugging:
import logging


class IFlvInfo(Interface):
    pass


class Adapter(Base):

    def _storage_path(self):
        """ """
        return getConfiguration().product_config.get('flv', {})['flv_dir'] + os.sep

    def __call__(self, uid, prefix='_flash_file'):
        """Extract metadata form flv file """
        context = self.context
        path = self._storage_path() + uid + prefix

        if os.path.exists(path):
            fp = open(path, 'rb')
            flv = tags.FLV(fp)
            tag_generator = flv.iter_tags()
            for i, tag in enumerate(tag_generator):
                if tag.name == 'onMetaData':
                    return tag.variable
        return {'width': 0, 'height': 0}
