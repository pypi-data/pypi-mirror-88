# Python compatibility:
from __future__ import absolute_import

# visaplan:
from visaplan.plone.tools.zcmlgen import SubpackageGenerator

SubpackageGenerator(__file__, skip='scripts').write()
# SubpackageGenerator(__file__).write()
