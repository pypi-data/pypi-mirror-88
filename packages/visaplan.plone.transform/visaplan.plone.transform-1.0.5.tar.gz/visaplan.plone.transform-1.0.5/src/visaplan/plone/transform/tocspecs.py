# -*- coding: utf-8 -*- vim: ts=8 sts=4 sw=4 si et tw=0
"""\
tocspecs.py - Verzeichnisdefinitionen parsen
"""

# Python compatibility:
from __future__ import absolute_import

# Standard library:
from string import letters
from token import ENDMARKER, NAME, NEWLINE, OP, STRING, tok_name

# visaplan:
from visaplan.kitchen.spoons import INSERT_POSITIONS
from visaplan.plone.pdfexport.utils import (
    ApiCall,
    ApiFilter,
    ControlStatement,
    gen_restricted_lines,
    )
from visaplan.tools.classes import Mirror, WriteProtected
from visaplan.tools.minifuncs import makeBool

# Local imports:
from .dispatcher import CHECKED_TOPICS

# Logging / Debugging:
# Debugging:
from pdb import set_trace
from visaplan.plone.tools.log import getLogSupport
from visaplan.tools.debug import log_or_trace, pp

logger, debug_active, DEBUG = getLogSupport()
lot_kwargs = {'logger': logger,
              'debug_level': debug_active,
              'trace': 1,
              }

__all__ = (#  Exceptions:
           'UnexpectedToken',
           # 'UnexpectedToken2',
           'ApiFilterTocsOnly',
           'SourceSpec',
           #  Hilfsfunktionen:
           # 'evaluateTocDefinition',
           # 'evaluateAppendixDefinition',
           )

# --------------------------- [ Exception-Klassen ... [
class UnexpectedToken(ValueError):
    """
    Fehler bei Interpretation einer Steueranweisung
    """
    def __init__(self, statement, token, info=None):
        self.mask = ['%(statement)s: unexpected token %(token)s']
        self.mask.append(self.mask[0] + ' (%(info)r expected)')

        self._statement = statement
        self._token = token
        self._info = info

    def __str__(self):
        statement = str(self._statement)
        token = self._token
        info = self._info
        if 0:
            pp((('mask:', mask),
                ('token:', token),
                ('Maskenindex:', int(info is not None)),
                ('Klasse:', self.__class__.__name__),
                ('locals():', locals()),
                ))
        return self.mask[info is not None] % locals()

class UnexpectedToken2(UnexpectedToken):
    """
    wie UnexpectedToken
    """

    def __init__(self, statement, token, info=None):
        """
        info ist ein Text
        """
        UnexpectedToken.__init__(self, statement, token, info)
        self.mask[1] = self.mask[0] + ' (%(info)s expected)'
# --------------------------- ] ... Exception-Klassen ]


# -------------------- [ Klasse ApiFilterTocsOnly ... [
TRACE = 0
class ApiFilterTocsOnly(ApiFilter):
    """
    Reduzierte Version von ApiFilter mit dem Fokus
    auf der Generierung von Verzeichnissen.

    Bei der HTML-Transformation werden keine PDFreactor-API-Aufrufe
    abgesetzt (da der PDFreactor hier nicht verwendet wird); es wird
    aber eine Auswertung vorgenommen:

    - Wenn setAddLinks(False) gewählt ist, aber die Generierung von
      Verzeichnissen konfiguriert, würden neben den externen auch die
      internen Hyperlinks unterdrückt.  Es werden in diesem Fall
      also die externen Links entfernt, damit die internen - für die
      Verzeichnisse - weiterhin generiert werden können.
    """

    def __init__(self,
                 hub,
                 log=None):
        ApiFilter.__init__(self, log=log)
        self._hub = hub
        self._msg = None

    def reset(self):
        ApiFilter.reset(self)
        self._ctrl.update({
            'add_links_value': False,  # Standard für setAddLinks
            'make_tocs': False,
            'toc_commands': [],
            'info_seed': {'tocs': [],
                          'appendixes': [],
                          '_remove_links': False,
                          },
            })

    def __call__(self, text, **kwargs):
        """
        Rufe die geerbte __call__-Methode auf
        und gib die ermittelten Informationen zurück.
        """
        global TRACE
        if TRACE:
            set_trace()
        ok = ApiFilter.__call__(self, text, **kwargs)
        if ok:
            return self._ctrl['info_seed']

    def skip_this(self, stmt):
        """
        Gib True zurück, wenn sich Instanzen dieser ApiFilter-Klasse um das
        übergebene Statement prinzipiell nicht kümmern.
        """
        if isinstance(stmt, ControlStatement):
            return stmt.name == 'strict'
        elif isinstance(stmt, ApiCall):
            return stmt.name != 'setAddLinks'
        # was der Bauer nicht kennt ...:
        return True

    def _call_statement(self, stmt,
                        checkfunc=None):
        """
        Führe das übergebene Statement aus.

        stmt -- ein Statement-Objekt
        checkfunc -- eine Funktion zur Prüfung, ob der übergebene Methodenname
                     zulässig ist. Wird nur beim Aufruf für die im Profil
                     konfigurierten, nicht für die hartcodierten Methoden
                     angegeben.

        Es wird nicht versucht, API-Aufrufe abzusetzen; im Rahmen der
        HTML-Transformation liegt der Fokus auf der Definition zu
        generierender Verzeichnisse.

        stmt - ein Statement-Objekt
        checkfunc -- eine Funktion zur Prüfung, ob der übergebene Methodenname
                     zulässig ist. Wird nur beim Aufruf für die im Profil
                     konfigurierten, nicht für die hartcodierten Methoden
                     angegeben.
                     (im Rahmen der HTML-Transformation ohne Relevanz)
        """
        if self._skip(stmt):
            return
        # set_trace()
        if isinstance(stmt, ApiCall):
            api_call = str(stmt)
            if not self._ctrl['ok']:
                errtext = _('Skipping %(api_call)r')
                self.log(errtext, locals())
                return
            if stmt.name == 'setAddLinks':  # siehe reset()
                # set_trace()
                try:
                    val = makeBool(stmt.args[0])
                    self._ctrl['add_links_value'] = val
                    self._ctrl['info_seed']['_remove_links'] = not val
                except ValueError as e:
                    self.log('Error executing %(stmt)s' % locals())
                    self._ctrl['ok'] = False
                else:
                    self.log('%(stmt)s: add_links_value := %(val)s'
                             % locals())
            else:
                self.log('Ignoring %s', stmt)
        elif isinstance(stmt, ControlStatement):
            if not self._ctrl['ok']:
                return
            # set_trace()
            name = stmt.name
            # Bisher gibt es nur 'strict'.
            # Wenn es mehr werden, muß das evtl.
            # mal generischer gelöst werden:
            if name == 'strict':
                if stmt.args:
                    self._ctrl['strict'] = makeBool(stmt.args[0])
                else:
                    self._ctrl['strict'] = True
                self.log('i strict %s',
                         self._ctrl['strict'] and 'ON' or 'OFF')
            elif name == 'appendix':
                dic = evaluateAppendixDefinition(stmt, self._ctrl['info_seed'])
                self._ctrl['info_seed']['appendixes'].append(dic)
            elif name == 'toc':
                dic = evaluateTocDefinition(stmt, self._ctrl['info_seed'])
                self._ctrl['info_seed']['tocs'].append(dic)

    def msg(self, txt, type='info', mapping={}):
        """
        Rufe den Message-Adapter auf (wenn übergeben)
        """
        try:
            self._hub['message'](txt, type, mapping=mapping)
        except TypeError:
            pass
# -------------------- ] ... Klasse ApiFilterTocsOnly ]


# --------------------- [ evaluateTocDefinition() ... [
# ------------------------ [ Daten ... [
# verboten, da Leerzeichen vor dem . nicht ersichtlich
# (aber für CSS signifikant):
FORBIDDEN_OPERATORS = frozenset('.:')
STRING_DELIMITERS = frozenset(('"', "'"))
# ------------------------ ] ... Daten ]

def evaluateTocDefinition(stmt, dic):
    """
    Interpretiere das übergebene toc-Statement.
    Die Einträge des inputlist-Schlüssels sind (bislang: einfache) CSS-Selektoren.

    Beispiel:
    >>> txt = "toc (h2, h3, h4) afterbegin of body"
    >>> lst = list(gen_restricted_lines(txt))
    >>> statement = lst[0]
    >>> sorted(evaluateTocDefinition(statement, {}).items())
    [('anchor', 'body'), ('inputlist', ['h2', 'h3', 'h4']), ('insert_position', 'afterbegin')]

    Ein Wrapper zu Testzwecken:

    >>> def eTD(txt):
    ...     stmt = list(gen_restricted_lines(txt))[0]
    ...     return sorted(evaluateTocDefinition(stmt, {}).items())
    >>> eTD("toc (h2, h3, h4) afterbegin of body")
    [('anchor', 'body'), ('inputlist', ['h2', 'h3', 'h4']), ('insert_position', 'afterbegin')]

    Die Angabe der Position ist optional; der Vorgabewert ist
    "beforebegin of 'div#content'", also vor dem Inhalt:

    >>> stmt2 = list(gen_restricted_lines("toc ('h2', h3)"))[0]
    >>> sorted(evaluateTocDefinition(stmt2, {}).items())
    [('anchor', 'div.toc'), ('inputlist', ['h2', 'h3']), ('insert_position', 'afterbegin')]
    """
    stmt.tell()
    stage = 0
    prevtype, prevval = None, None
    infokey = stmt.name
    inputlist = []
    ldic = {'inputlist': [],
            # Inhaltsverzeichnis standardmäßig vor dem Inhalt plazieren:
            'insert_position': 'beforebegin',
            'anchor': 'div#content',
            'headline_text': 'Table of Contents',
            'headline_translate': True,
            }
    # set_trace()
    for tok in stmt.tokens[1:]:
        thistype, thisval = tok[:2]
        if thistype == OP:
            if thisval in FORBIDDEN_OPERATORS:
                raise UnexpectedToken(stmt, tok)
        if stage in (0, 7):
            if thistype == OP and thisval == '(':
                stage = 10
            elif thistype == STRING:
                ldic['headline_text'] = _token_value(thistype, thisval)
                stage = 10
            elif thistype == NAME:
                if thisval in ('translated', 'untranslated'):
                    ldic['headline_translate'] = thisval == 'translated'
                elif thisval in ('without',):
                    ldic['headline_text'] = None
                else:
                    raise UnexpectedToken(stmt, tok)
                stage = 6
            else:
                raise UnexpectedToken(stmt, tok, '(')
        elif stage == 6:   # "headline" folgt
            if thistype == NAME and thisval == 'headline':
                if ldic['headline_text'] is None:
                    stage = 0
                else:
                    stage = 7
            else:
                raise UnexpectedToken(stmt, tok, 'headline')
        elif stage == 10:  # Listeneintrag folgt
            if thistype in (NAME, STRING):
                ldic['inputlist'].append(_token_value(thistype, thisval))
                stage = 20
            elif thistype == OP and thisval == '(':
                pass
            elif thistype == OP and thisval == ')':
                # ',)' tolerieren:
                stage = 30
            else:
                raise UnexpectedToken2(stmt, tok, 'string or symbol')
        elif stage == 20:  # Komma oder Listenende folgt
            if thistype == OP:
                if thisval == ',':
                    stage = 10
                elif thisval == ')':
                    stage = 30
                else:
                    raise UnexpectedToken(stmt, tok, ')')
            else:
                raise UnexpectedToken(stmt, tok, ')')
        elif stage == 30:  # Position folgt
            if thistype == NAME:
                if thisval in INSERT_POSITIONS:
                    ldic['insert_position'] = thisval
                    stage = 40
                elif thisval in ('after', 'before'):
                    stage = 31
                    tmp = thisval
                else:
                    raise UnexpectedToken2(stmt, tok, 'position')
            else:
                raise UnexpectedToken2(stmt, tok, 'position')
        elif stage == 31:
            if thistype == NAME and thisval in ('begin', 'end'):
                ldic['insert_position'] = tmp + thisval
                stage = 40
            else:
                raise UnexpectedToken2(stmt, tok, 'begin or end')
        elif stage == 40:
            if thistype == NAME and thisval == 'of':
                stage = 50
            else:
                raise UnexpectedToken(stmt, tok, 'of')
        elif stage == 50:
            if thistype == NAME:
                ldic['anchor'] = thisval
            elif thistype == STRING:
                if thisval:
                    ldic['anchor'] = _token_value(thistype, thisval)
                else:
                    raise UnexpectedToken2(stmt, tok, 'non-empty anchor')
            else:
                raise UnexpectedToken2(stmt, tok, 'anchor')
            stage = 99
        elif stage == 99:
            if thistype == OP and thisval in (';',):
                pass
            else:
                raise UnexpectedToken2(stmt, tok, "end or ';'")
        else:
            raise ValueError('Unexpected stage %(stage)r'
                             % locals())
        prevtype, prevval = thistype, thisval
    return ldic
# --------------------- ] ... evaluateTocDefinition() ]


# ---------------- [ evaluateAppendixDefinition() ... [
@log_or_trace(**lot_kwargs)
def evaluateAppendixDefinition(stmt, dic):
    """
    Interpretiere die übergebene Anhangsdefinition.
    Die Einträge des inputlist-Schlüssels sind SourceSpec-Instanzen.

    Zur Demonstration zunächst ein handlicher Wrapper:

    >>> def eAD(txt):
    ...     stmt = list(gen_restricted_lines(txt))[0]
    ...     return sorted(evaluateAppendixDefinition(stmt, {}).items())

    Ausführliches Beispiel:

    >>> eAD("appendix (images, media) beforeend of body")
    [('anchor', 'body'), ('inputlist', [<SourceSpec(images plain auto)>, <SourceSpec(media plain auto)>]), ('insert_position', 'beforeend')]

    Die Angabe der Position ist optional; der Vorgabewert ist
    "afterend of 'div#content'", also nach dem Inhalt:

    >>> eAD("appendix (images)")
    [('anchor', 'div.appendix'), ('inputlist', [<SourceSpec(images plain auto)>]), ('insert_position', 'afterbegin')]
    """
    stage = 0
    prevtype, prevval = None, None
    infokey = stmt.name
    ldic = {'inputlist': [],
            # Anhang standardmäßig nach dem Inhalt plazieren:
            'insert_position': 'afterend',
            'anchor': 'div#content',
            'headline_text': 'Appendix',
            'headline_translate': True,
            }
    input_list = ldic['inputlist']
    src_spec = None
    for tok in stmt.tokens[1:]:
        thistype, thisval = tok[:2]
        if thistype == OP:
            if thisval in FORBIDDEN_OPERATORS:
                raise UnexpectedToken(stmt, tok)
        if stage in (0, 7):
            if thistype == OP and thisval == '(':
                stage = 10
                src_spec = SourceSpec()
            elif thistype == STRING:
                ldic['headline_text'] = _token_value(thistype, thisval)
                stage = 10
            elif thistype == NAME:
                if thisval in ('translated', 'untranslated'):
                    ldic['headline_translate'] = thisval == 'translated'
                elif thisval in ('without',):
                    ldic['headline_text'] = None
                else:
                    raise UnexpectedToken(stmt, tok)
                stage = 6
            else:
                raise UnexpectedToken(stmt, tok, '(')
        elif stage == 6:   # "headline" folgt
            if thistype == NAME and thisval == 'headline':
                if ldic['headline_text'] is None:
                    stage = 0
                else:
                    stage = 7
            else:
                raise UnexpectedToken(stmt, tok, 'headline')
        elif stage == 10:  # Listeneintrag folgt
            if thistype in (NAME, STRING):
                src_spec.record(_token_value(thistype, thisval))
            elif thistype == OP and thisval in (')', ',', '('):
                if src_spec:
                    input_list.append(src_spec)
                if thisval in (',', '('):
                    src_spec = SourceSpec()
                else:
                    # ',)' tolerieren:
                    stage = 30
            else:
                raise UnexpectedToken2(stmt, tok, 'string or symbol')
        elif stage == 30:  # Position folgt
            if thistype == NAME:
                if thisval in INSERT_POSITIONS:
                    ldic['insert_position'] = thisval
                    stage = 40
                elif thisval in ('after', 'before'):
                    stage = 31
                    tmp = thisval
                else:
                    raise UnexpectedToken2(stmt, tok, 'position')
            else:
                raise UnexpectedToken2(stmt, tok, 'position')
        elif stage == 31:
            if thistype == NAME and thisval in ('begin', 'end'):
                ldic['insert_position'] = tmp + thisval
                stage = 40
            else:
                raise UnexpectedToken2(stmt, tok, 'begin or end')
        elif stage == 40:
            if thistype == NAME and thisval == 'of':
                stage = 50
            else:
                raise UnexpectedToken(stmt, tok, 'of')
        elif stage == 50:
            if thistype == NAME:
                ldic['anchor'] = thisval
            elif thistype == STRING:
                if thisval:
                    ldic['anchor'] = _token_value(thistype, thisval)
                else:
                    raise UnexpectedToken2(stmt, tok, 'non-empty anchor')
            else:
                raise UnexpectedToken2(stmt, tok, 'anchor')
            stage = 99
        elif stage == 99:
            if thistype == OP and thisval in (';',):
                pass
            else:
                raise UnexpectedToken2(stmt, tok, "end or ';'")
        else:
            raise ValueError('Unexpected stage %(stage)r'
                             % locals())
        prevtype, prevval = thistype, thisval
    return ldic
# ---------------- ] ... evaluateAppendixDefinition() ]


# ---------------------- [ dict-Klasse SourceSpec ... [
# ------------------------ [ Daten ... [
SOURCESPEC_KEY = WriteProtected()
for key in CHECKED_TOPICS:
    SOURCESPEC_KEY[key] = 'objects'
assert 'index' in SOURCESPEC_KEY
for key in ('plain',
            'sorted',
            'grouped',
            ):
    SOURCESPEC_KEY[key] = 'sorting'
for key in ('auto',
            'force',
            'on',  # wie force
            # auch wenn nicht leer:
            'off',
            ):
    SOURCESPEC_KEY[key] = 'ifempty'
SOURCESPEC_KEY.freeze()
KNOWN_KEYS = frozenset(list(SOURCESPEC_KEY.values()) +
                       # Schlüssel mit allgemeineren Werten:
                       ['headline_text',  # ggf. None, wenn unterdrückt
                        ])
UNALIAS = Mirror({'on': 'force',
                  })
# ------------------------ ] ... Daten ]

class SourceSpec(dict):
    """
    Hilfsklasse zum Sammeln von Angaben zu *einem* Anhang

    >>> spec = SourceSpec('images sorted auto')
    >>> spec
    <SourceSpec(images sorted auto)>

    Das Objekt läßt sich als Dictionary verwenden und in ein solches
    umwandeln:

    >>> dic = dict(spec)
    >>> sorted(dic.keys())
    ['ifempty', 'objects', 'sorting']

    >>> sorted(spec.items())
    [('ifempty', 'auto'), ('objects', 'images'), ('sorting', 'sorted')]

    Standardwerte - für alles außer den Objekttypen:

    >>> spec.reset()
    >>> spec
    <SourceSpec(plain auto)>
    """


    def __init__(self, s=None):
        self.reset()
        if s:  # für Doctests:
            for value in s.split():
                self.record(value)

    def reset(self):
        self.clear()
        self.update({'sorting': 'plain',
                     'ifempty': 'auto',
                     })
        self._dirty = False

    def record(self, value):
        """
        Nimm eine Zeichenkette entgegen (aus einem bekannten Pool von
        Möglichkeiten) und ordne sie der passenden Eigenschaft zu.
        """
        try:
            key = SOURCESPEC_KEY[value]
            self[key] = UNALIAS[value]
            self._dirty = True
        except KeyError:
            raise ValueError('%(self)r: value %(value)r not supported' % locals())

    def _liz(self):
        liz = []
        for key in ('objects', 'sorting', 'ifempty',
                    ):
            val = self[key]
            if val is not None:
                liz.append(val)
        return liz

    def __repr__(self):
        return '<%s(%s)>' % (self.__class__.__name__,
                             ' '.join(self._liz()))

    def __str__(self):
        return "%s('%s')" % (self.__class__.__name__,
                             ' '.join(self._liz()))

    def __getitem__(self, key):
        try:
            return dict.__getitem__(self, key)
        except KeyError:
            if key in KNOWN_KEYS:
                return None
            raise

    def __nonzero__(self):
        """
        Wahrheitswert des Objekts
        """
        if self['objects']:
            return True
        if self._dirty:
            raise ValueError('%(self)r is not complete'
                             % locals())
        return False
# ---------------------- ] ... dict-Klasse SourceSpec ]


def _token_value(ty, va):
    if ty not in (NAME, STRING):
        return va
    if not va:
        return va
    if va[0] in STRING_DELIMITERS:
        return va[1:-1]
    return va


if __name__ == '__main__':
    # Standard library:
    import doctest
    doctest.testmod()
