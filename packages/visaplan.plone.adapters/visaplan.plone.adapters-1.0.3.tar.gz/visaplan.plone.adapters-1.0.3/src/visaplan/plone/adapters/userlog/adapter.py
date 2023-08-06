# -*- coding: utf-8 -*- vim: ts=8 sts=4 sw=4 si et tw=79
# Python compatibility:
from __future__ import absolute_import

# Zope:
from zope.interface import implements

# visaplan:
from visaplan.plone.base import Base, Interface

# Local imports:
# Dieser Adapter:
from .config import DIVIDE, USERLOG
from .utils import sorted_items

# Logging / Debugging:
from visaplan.plone.tools.log import getLogSupport, make_textlogger

logger, debug_active, DEBUG = getLogSupport()


class IUserLog(Interface):
    def __call__(msg, **kwargs):
        """
        Schreibe einen Eintrag ins "User-Logbuch"
        """

    def registered(**kwargs):
        """
        Protokolliere die Registrierung des übergebenen Users
        """

    def confirmed(**kwargs):
        """
        Der übergebene User hat seine Anmeldung bestätigt
        """

    def locked(**kwargs):
        """
        Der übergebene User wurde administrativ gesperrt
        """

    def unlocked(**kwargs):
        """
        Der übergebene User wurde administrativ entsperrt
        """

    def createdbyadmin(**kwargs):
        """
        Der übergebene User wurde administrativ angelegt.
        Der Name des Admin-Accounts kann im Schlüssel 'by' angegeben werden.
        """

    def deleted(username, uid=None):
        """
        der uebergebene Benutzer wurde geloescht
        """

    def deletedProfile(username, uid=None):
        """
        das uebergebene Profil wurde geloescht
        """

writer = make_textlogger(fn=USERLOG,
                         sorting_filter=sorted_items,
                         divide=DIVIDE)


class Adapter(Base):
    implements(IUserLog)

    def __call__(self, msg, **kwargs):
        u"""
        Schreibe einen Eintrag ins "User-Logbuch"
        (Nachricht, zeilenweise die Formularfelder,
        und abschließend eine Leerzeile)
        """
        return writer(msg, **kwargs)

    def registered(self, **kwargs):
        """
        Protokolliere die Registrierung des übergebenen Users
        """
        self('User registered', **kwargs)

    def confirmed(self, **kwargs):
        """
        Der übergebene User hat seine Anmeldung bestätigt
        """
        self('User confirmed', **kwargs)

    def locked(self, **kwargs):
        """
        Der übergebene User wurde administrativ gesperrt
        """
        self('User locked', **kwargs)

    def unlocked(self, **kwargs):
        """
        Der übergebene User wurde administrativ entsperrt
        """
        self('User unlocked', **kwargs)

    def createdbyadmin(self, **kwargs):
        """
        Der übergebene User wurde administrativ angelegt.
        Der Name des Admin-Accounts kann im Schlüssel 'by' angegeben werden.
        """
        self('User created', **kwargs)

    def deleted(self, username, uid=None):
        """
        der uebergebene Benutzer wurde geloescht
        """
        self('User deleted', username=username, uid=uid)

    def deletedProfile(self, username, uid=None):
        """
        das uebergebene Profil wurde geloescht
        """
        self('Profile deleted', username=username, uid=uid)
