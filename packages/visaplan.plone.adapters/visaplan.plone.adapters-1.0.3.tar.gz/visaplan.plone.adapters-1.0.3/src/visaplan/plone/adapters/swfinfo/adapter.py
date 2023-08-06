# Python compatibility:
from __future__ import absolute_import

from six.moves import range

# Standard library:
import os
import struct
import zlib

# Zope:
from Products.CMFCore.utils import getToolByName

# Plone:
from plone.memoize import ram

# visaplan:
from visaplan.plone.base import Base, Interface


def cache_key(method, self):

    context = self.context
    pc = getToolByName(context, 'portal_catalog')

    return (pc.getCounter(), context.UID())


class ISWFInfo(Interface):
    pass


class Adapter(Base):

    @ram.cache(cache_key)
    def __call__(self):
        """Parses the header information from an SWF file."""
        context = self.context
        blob_ = context.getField('file').get(context).blob
        blob_._p_deactivate()
        fshelper = blob_._p_jar._storage.fshelper

        input = fshelper.getBlobFilename(blob_._p_oid, blob_._p_serial)

        if not os.path.exists(input):
            return {'height': 0, 'width': 0}
        input = open(input, 'rb')

        def read_ui8(c):
            return struct.unpack('<B', c)[0]

        def read_ui16(c):
            return struct.unpack('<H', c)[0]

        def read_ui32(c):
            return struct.unpack('<I', c)[0]

        header = {}

        # Read the 3-byte signature field
        chunk = input.read(3)
        if len(chunk) < 3:
            signature = None
        else:
            signature = ''.join(struct.unpack('<3c', chunk))
        if signature not in ('FWS', 'CWS'):
            return {'width': 0, 'height': 0}

        # Compression
        header['compressed'] = signature.startswith('C')

        # Version
        header['version'] = read_ui8(input.read(1))

        # File size (stored as a 32-bit integer)
        header['size'] = read_ui32(input.read(4))

        # Payload
        buffer = input.read(header['size'])
        if header['compressed']:
            # Unpack the zlib compression
            buffer = zlib.decompress(buffer)

        # Containing rectangle (struct RECT)

        # The number of bits used to store the each of the RECT values are
        # stored in first five bits of the first byte.
        nbits = read_ui8(buffer[0]) >> 3

        current_byte, buffer = read_ui8(buffer[0]), buffer[1:]
        bit_cursor = 5

        for item in 'xmin', 'xmax', 'ymin', 'ymax':
            value = 0
            for value_bit in range(nbits-1, -1, -1):  # == reversed(range(nbits))
                if (current_byte << bit_cursor) & 0x80:
                    value |= 1 << value_bit
                # Advance the bit cursor to the next bit
                bit_cursor += 1

                if bit_cursor > 7:
                    # We've exhausted the current byte, consume the next one
                    # from the buffer.
                    current_byte, buffer = read_ui8(buffer[0]), buffer[1:]
                    bit_cursor = 0

            # Convert value from TWIPS to a pixel value
            header[item] = value / 20

        header['width'] = header['xmax'] - header['xmin']
        header['height'] = header['ymax'] - header['ymin']

        header['frames'] = read_ui16(buffer[0:2])
        header['fps'] = read_ui16(buffer[2:4])

        input.close()

        dict_ = {}
        dict_['width'] = header['width']
        dict_['height'] = header['height']

        return dict_
