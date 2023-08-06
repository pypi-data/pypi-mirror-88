# -*- coding: utf-8 -*- äöü
"""
Nicht zum Import!
Doctests für die veralteten, RE-basierten Methoden des transform-Browsers,
zur Demonstration der Funktion
"""
# Python compatibility:
# ------------------------------------- [ (alte) Methode 'regex' ... [
from __future__ import absolute_import

# Standard library:
import re

# visaplan:
from visaplan.kitchen.spoons import extract_uid
from visaplan.plone.tools.mock import MockBrowser

# ------------------------------------- ] ... (alte) Methode 'regex' ]


# ------------------------------------- [ (alte) Methode 'regex' ... [
# ACHTUNG: Diese Regulären Ausdrücke werden im transform-Browser nicht
#          mehr verwendet und sind hier *nur noch* vorhanden, weil sie
#          in (veralteten) Methoden verwendet werden, die noch von an-
#          deren Modulen importiert werden.
#          Das wird nicht mehr empfohlen!
#          Bitte generell HTML-Code nur noch mit geeigneten Werkzeugen
#          durchsuchen und ändern, z. B. mit BeautifulSoup!
# nur öffnende Elemente:        1  2   2      1
RE_IMAGE_OPENERS = re.compile(r'(\<(img)[^>]*>)')

# komplette a-Elemente:      1  2 2    3   3    1
RE_A_ELEMENTS = re.compile(r'(\<(a)[^<](.+?)</a>)')

# Attributwerte ermitteln:                    1   1
RE_HREF_VALUES         =    re.compile('href="(.+?)"')
RE_SRC_VALUES          =     re.compile('src="(.+?)"')
# ------------------------------------- ] ... (alte) Methode 'regex' ]

if True:
    b = MockBrowser()

    # (leider) noch verwendet in den Browsern changestate und copystructure:
    def _getUid(self, string_):
        """
        Durchsuche den übergebenen String nach href-Attributen;
        berücksichtige nur den ersten.
        Gib ein 2-Tupel (uid, targetUid) zurück.

        - Wenn die URL mit '#' beginnt (seitenlokal):
          nimm die folgenden 32 Zeichen als 'uid',
          und die UID des Kontexts als 'targetUid'
        - wenn die URL '/resolveuid/' enthält, nimm das folgende Pfadsegment
          als 'targetUid' (wenn es leer oder nicht vorhanden ist, knallt's).

        Die entsprechende neue Funktion heißt extract_2uids.

        >>> _getUid(b, '<a href="#abc123seitenlokalabc123abc123abc">HONK')
        ('abc123seitenlokalabc123abc123abc', 'MockUID_MockUID_MockUID_MockUID_')
        """
        uid = ''
        targetUid = ''
        link = RE_HREF_VALUES.findall(string_)
        if link and link[0].lower().find('resolveuid') != -1:
            splitted = link[0].lower().split('/')
            uid = splitted[splitted.index('resolveuid') + 1]
            if not uid:
                uid = None
            targetUid = uid[:32]
            if uid.find('#') != -1:
                uid = uid[uid.index('#') + 1:]

        #Anker
        if link and link[0].startswith('#'):
            uid = link[0][1:33]
            targetUid = self.context.UID()
        return uid, targetUid

    # (leider) noch verwendet in den Browsern changestate und copystructure:
    def _getImgUid(self, string_):
        link = RE_SRC_VALUES.findall(string_)[0]
        return extract_uid(link)

    # (leider) noch verwendet in den Browsern changestate und copystructure:
    def _getLinks(self, text):
        """ """
        return [item[0]
                for item in RE_A_ELEMENTS.findall(text)
                ]

    # (leider) noch verwendet in den Browsern changestate und copystructure:
    def _getImages(self, text):
        """ """
        return [item[0]
                for item in RE_IMAGE_OPENERS.findall(text)
                ]
# ------------------------------------- ] ... (alte) Methode 'regex' ]
