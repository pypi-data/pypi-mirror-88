# -*- coding: utf-8 -*- vim: ts=8 sts=4 sw=4 si et tw=79
# Python compatibility:
from __future__ import absolute_import

# Standard library:
from datetime import date
from time import strftime

# Zope:
from zope.interface import implements
from Products.CMFCore.utils import getToolByName

# visaplan:
from visaplan.plone.base import Base, Interface

# Local imports:
# Andere Adapter:
from ..userlog.config import GROUPLOG
# Dieser Adapter:
from .utils import sorted_items

# Logging / Debugging:
from visaplan.plone.tools.log import getLogSupport, make_textlogger

logger, debug_active, DEBUG = getLogSupport()


class IGroupLog(Interface):
    def __call__(msg, **kwargs):
        """
        Schreibe eine Zeile ins "Gruppen-Logbuch"
        """

writer = make_textlogger(fn=GROUPLOG,
                         sorting_filter=sorted_items,
                         lock=True,
                         debug=debug_active)


class Adapter(Base):
    implements(IGroupLog)

    def __call__(self, msg, **kwargs):
        u"""
        Schreibe einen Eintrag ins "Gruppen-Logbuch"
        (Nachricht, zeilenweise die Formularfelder,
        und abschließend eine Leerzeile)
        """
        if 'by' not in kwargs:
            kwargs['by'] = self._get_user_info()
        return writer(msg, **kwargs)

    def _get_user_info(self):
        """
        Ermittle den während des aktuellen Requests aktiven Benutzer
        """
        val = None
        try:
            return self._user_info
        except AttributeError:
            context = self.context
            pm = getToolByName(context, 'portal_membership')
            if not pm.isAnonymousUser():
                auth_member = pm.getAuthenticatedMember()
                auth_id = str(auth_member)
                auth_fullname = auth_member.getProperty('fullname', auth_id) or auth_id or ''
                tup = (auth_id, auth_fullname)
                val = '%s (%s)' % tup
            self._user_info = val
            return val

    def created(self, **kwargs):
        """
        Die übergebene Gruppe wurde administrativ angelegt.
        Der Name des Admin-Accounts kann im Schlüssel 'by' angegeben werden.
        """
        self('Group created', **kwargs)

    def deleted(self, **kwargs):
        """
        die übergebene Gruppe wurde geloescht
        """
        self('Group deleted', **kwargs)

    def missing(self, **kwargs):
        """
        die übergebene Gruppe konnte nicht gefunden werden
        """
        self('Group not found', **kwargs)

    def added(self, **kwargs):
        """
        Ein Mitglied wurde einer Gruppe hinzugefügt
        """
        self('Member added', **kwargs)

    def removed(self, **kwargs):
        """
        Ein Mitglied wurde aus einer Gruppe entfernt
        """
        self('Member removed', **kwargs)

    def scheduled_addition(self, **kwargs):
        """
        Die Zuweisung eines neuen Gruppenmitglieds wurde geplant
        """
        self('Member scheduled for addition', **kwargs)

    def scheduled_removal(self, **kwargs):
        """
        Die Beendigung einer Gruppenmitgliedschaft wurde geplant
        """
        self('Member scheduled for removal', **kwargs)

    def rescheduled(self, **kwargs):
        """
        Die Gruppenmitgliedschaft wurde neu geplant
        """
        self('Membership rescheduled', **kwargs)

    def row_updated(self, **kwargs):
        """
        Für die Bearbeitung in der Mitglieder- oder Gruppenverwaltung:
        Es werden - je nach Datenlage - verschiedene Texte geschrieben
        """
        today = kwargs.pop('today', None)
        if today is None:
            today = date.today()
        start = kwargs.get('start')
        ends = kwargs.get('ends')
        active = kwargs.get('active')
        if start is None:
            if ends is None:
                if active is None:
                    return self('???', **kwargs)
                if active:
                    return self.added(**kwargs)
                else:
                    return self.removed(**kwargs)
            elif ends > today:
                return self.scheduled_removal(**kwargs)
            else:
                return self.removed(**kwargs)
        elif start > today:
            return self.scheduled_addition(**kwargs)
        elif ends is None:
            # start ist nicht None und <= today:
            return self.added(**kwargs)
        elif ends <= today:
            # ends ist nicht None:
            return self.removed(**kwargs)
        else:
            return self.added(**kwargs)
