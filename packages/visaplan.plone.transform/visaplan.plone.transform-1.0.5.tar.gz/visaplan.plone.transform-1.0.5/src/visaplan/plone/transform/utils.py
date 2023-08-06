# -*- coding: utf-8 -*- vim: ts=8 sts=4 sw=4 si et tw=0
"""\
utils.py - utils-Modul für den transform-Browser

Die hier implementierten Funktionen basieren nur auf
Standard-Python-Funktionalitäten (also z. B. nicht auf BeautifulSoup)
und sind daher einfacher unabhängig zu testen.
"""

# Python compatibility:
from __future__ import absolute_import

from six import string_types as six_string_types
from six.moves import range
from six.moves.urllib.parse import urlsplit, urlunsplit

# Standard library:
from copy import deepcopy

__all__ = (# beide verschoben nach ...tools.spoons:
           # 'extract_uid',
           # 'extract_uid_and_tail',
           'join_path_and_tail',
           'extract_2uids',
           'extractImageAlignment',  # erzeugt von:
           'make_alignment_extractor',
           'make_stepup',
           'image_stepup',
           )

def make_stepup(prefix='image', seq=None):
    """
    >>> stepup = make_stepup()
    >>> stepup('image_thumb', 1)
    'image_mini'
    >>> stepup('image_thumb', 2)
    'image_preview'
    >>> stepup('image_thumb', 'top')
    'image'
    """
    if seq is None:
        seq = ['large',
               'preview',
               'mini',
               'thumb',
               'tile',
               'icon',
               'listing',
               ]
    prev = prefix
    nextupper = {}
    for item in seq:
        item = prefix + '_' + item
        nextupper[item] = prev
        prev = item

    def stepup(item, steps):
        if not steps:
            return item
        if steps == 'top':
            return prefix
        for i in range(steps):
            if item == prefix:
                return item
            item = nextupper[item]
        return item

    return stepup
image_stepup = make_stepup()


def join_path_and_tail(path, tail):
    """
    path -- der Pfad eines Objekts
    tail -- üblicherweise aus einem Aufruf von -> extract_uid_and_tail

    >>> join_path_and_tail('/temp/image.png', 'image?honk#bonk')
    '/temp/image.png/image?honk#bonk'
    """
    urllist = list(urlsplit(tail))
    if urllist[2]:
        urllist[2] = '/'.join((path, urllist[2]))
    else:
        urllist[2] = path
    return urlunsplit(urllist)


def _ru_seg_index(segments):
    """
    Helferlein für extract_2uids: gib den ersten Index zurück, der
    'resolveUid', '@@resolveuid' o.ä enthält; wirf ggf. einen ValueError

    >>> s2 = '/resolveuid/TARGETTARGETTARGETTARGETTARGETTA'
    >>> _ru_seg_index(s2.split('/'))
    1

    Die Funktion interessiert sich nur für den eigentlichen Pfad ...
    Wenn - mit # abgetrennt - eine zweite UID angegeben wird,
    ist dies die 'uid', und der erste Wert ist die 'haystack_uid':

    >>> s3 = ('/resolveuid/TARGETTARGETTARGETTARGETTARGETTA'
    ...                  '#UIDUIDUIDUIDUIDUIDUIDUIDUIDUIDUI')
    >>> _ru_seg_index(s3.split('/'))
    1

    ... und erwartet aktuell eine Liste, die in Kleinschreibung konvertiert wurde:

    >>> s3_1 = ('./resolveUid/3a8cba99f7929f01aa4435416d3af527')
    >>> _ru_seg_index(s3_1.split('/'))
    Traceback (most recent call last):
    ...
    ValueError: No [@@]resolveuid segment in ['.', 'resolveUid', '3a8cba99f7929f01aa4435416d3af527']!

    '@@resolveuid' wird aber erkannt:
    >>> s3_2 = ('./@@resolveuid/3a8cba99f7929f01aa4435416d3af522'
    ...                       '#e57642bdab607084f202845729298f75')
    >>> _ru_seg_index(s3_2.split('/'))
    1

    Sonstige Verweisziele zeitigen einen ValueError:

    >>> s6 = '/irgend/wo/hin'
    >>> _ru_seg_index(s6.split('/'))
    Traceback (most recent call last):
    ...
    ValueError: No [@@]resolveuid segment in ['', 'irgend', 'wo', 'hin']!

    """
    for i, seg in zip(range(len(segments)), segments):
        if seg in ('resolveuid', '@@resolveuid'):
            return i
    raise ValueError('No [@@]resolveuid segment in %(segments)r!' % locals())


def extract_2uids(path, info):
    """
    Ersetzt die bisherige Methode _getUid, die allerdings einen String
    erwartete, der ein ganzes a-Element enthält.

    path -- der Wert eines href-Attributs
    info -- ein dict-Objekt, das unter dem Schlüssel 'my_uid' die UID des
            Kontexts enthält

    Gib ein 2-Tupel (uid, haystack_uid) zurück.

    Bei seitenlokalen Links verweist 'haystack_uid' auf den Kontext.
    Die angegebene UID wird dabei auf 32 Zeichen eingekürzt:

    >>> info = {'my_uid': ('context' * 5)[:32]}
    >>> s1 = '#abc12345abc12345abc12345abc12345-uid'
    >>> extract_2uids(s1, info)
    ('abc12345abc12345abc12345abc12345', 'contextcontextcontextcontextcont')

    "Normale resolveuid-Links" zeitigen zwei identische Werte:

    >>> s2 = '/resolveuid/TARGETTARGETTARGETTARGETTARGETTA'
    >>> extract_2uids(s2, info)
    ('targettargettargettargettargetta', 'targettargettargettargettargetta')

    Wenn - mit # abgetrennt - eine zweite UID angegeben wird,
    ist dies die 'uid', und der erste Wert ist die 'haystack_uid':

    >>> s3 = ('/resolveuid/TARGETTARGETTARGETTARGETTARGETTA'
    ...                  '#UIDUIDUIDUIDUIDUIDUIDUIDUIDUIDUI')
    >>> extract_2uids(s3, info)
    ('uiduiduiduiduiduiduiduiduiduidui', 'targettargettargettargettargetta')

    Aus dem richtigen Leben:

    >>> s3_1 = ('./resolveUid/3a8cba99f7929f01aa4435416d3af527'
    ...         '#e57642bdab607084f202845729298f75')
    >>> extract_2uids(s3_1, info)
    ('e57642bdab607084f202845729298f75', '3a8cba99f7929f01aa4435416d3af527')

    Auch die BrowserView-Schreibweise mit '@@' wird nun erkannt:
    >>> s3_2 = ('./@@resolveuid/3a8cba99f7929f01aa4435416d3af522'
    ...                       '#e57642bdab607084f202845729298f75')
    >>> extract_2uids(s3_2, info)
    ('e57642bdab607084f202845729298f75', '3a8cba99f7929f01aa4435416d3af522')

    Ein # in einem späteren Segment ist natürlich irrelevant:

    >>> s4 = '/resolveuid/abc12345abc12345abc12345abc12345/#'
    >>> extract_2uids(s4, info)
    ('abc12345abc12345abc12345abc12345', 'abc12345abc12345abc12345abc12345')

    Ein etwaiges Suffix der UID bleibt in 'uid' erhalten,
    in 'haystack_uid' nicht:

    >>> s5 = '/resolveuid/TARGETTARGETTARGETTARGETTARGETTA-uid'
    >>> extract_2uids(s5, info)
    ('targettargettargettargettargetta-uid', 'targettargettargettargettargetta')

    Sonstige Verweisziele zeitigen leere Strings:

    >>> s6 = '/irgend/wo/hin'
    >>> extract_2uids(s6, info)
    ('', '')
    """
    uid, haystack_uid = ('', '')
    # seitenlokaler Link:
    if path.startswith('#'):
        lst = path.split('#', 2)
        return lst[1][:32], info['my_uid']
    if path:
        segments_lower = path.lower().split('/')
        try:
            i = _ru_seg_index(segments_lower)
            if 0 <= i < len(segments_lower):
                uid = segments_lower[i+1]
        except ValueError:
            pass
        else:
            lst = uid.split('#')
            if lst[1:]:
                return (lst[1], lst[0][:32])
            else:
                return (uid, uid[:32])
    return (uid, haystack_uid)


def make_alignment_extractor(whitelist=frozenset(['remove-padding-top',
                                                  'remove-padding-right',
                                                  'remove-padding-bottom',
                                                  'remove-padding-left',
                                                  ]),
                             blacklist=frozenset(['image-center',
                                                  # keine Positionierungen:
                                                  'image-caption',
                                                  'image-legend',
                                                  ]),
                             default_alignment='media-inline'):
    """
    Erzeuge eine Funktion extractImageAlignment:
    Extrahiere die relevanten Klassen aus der übergebenen (dabei nicht
    modifizierten) Liste, benenne sie ggf. um, und gib einen String zurück.

    whitelist - Klassen, die unverändert extrahiert (und nicht als
                alignment-Klassen erkannt) werden
    blacklist - Klassen, die nicht extrahiert werden, obwohl sie mit
                'media-' beginnen
    default_alignment - eine Klasse als Vorgabe für die alignment-Klassen
                        (wenn keine solche extrahiert)

    Anmerkung zum default_alignment:
        Die Transformation durch den transform-Browser behandelt derzeit
        (16.5.2018, Rev. 21326) eingebettete img-Objekte ohne Positionierung
        nicht korrekt; dies war aber eine verbreitete Praxis für Bilder, die
        einzeln oder mit manuell angegebener Unterschrift in einer
        Layout-Spalte plaziert wurden.
        Es wird daher als Vorgabewert 'media-inline' vorgesehen, was in diesen
        Fällen das korrekte Ergebnis zeitigt.
        Wenn sich dies bewährt, ist auch ein (wiederholbarer) Migrationsschritt
        zur entsprechenden Modifikation der redaktionellen Texte denkbar.

    Funktion mit Vorgabewerten erzeugen:
    >>> extractImageAlignment = make_alignment_extractor()

    'image-center' wird entfernt; Vorgabe-Ausrichtung ist 'media-inline':
    >>> thelist = ['image-center']
    >>> extractImageAlignment(thelist)
    'media-inline'

    Andere 'image-'-KLassen werden nach 'media-...' umbenannt;
    'media-'-Klassen und solche zur Steuerung des Paddings werden
    extrahiert:

    >>> thelist.extend(['image-left', 'media-any', 'remove-padding-left'])
    >>> extractImageAlignment(thelist)
    'media-any media-left remove-padding-left'

    Die Eingabeliste blieb dabei unverändert:
    >>> thelist
    ['image-center', 'image-left', 'media-any', 'remove-padding-left']

    Sonstige Klassen werden verworfen:

    >>> thelist = ['media-any', 'left']
    >>> extractImageAlignment(thelist)
    'media-any'
    """
    conflicts = whitelist.intersection(blacklist)
    if conflicts:
        conflicts = sorted(conflicts)
        raise ValueError('%(conflicts)s are both given in whitelist '
                         'and blacklist'
                         % locals())
    if default_alignment is None:
        add_alignment_default = False
    else:
        if not default_alignment.startswith('media-'):
            raise ValueError('default_alignment is expected to start with "media-"'
                             ' (%(default_alignment)r)'
                             % locals())
        elif default_alignment in blacklist:
            blacklist = sorted(blacklist)
            raise ValueError("default_alignment can't be blacklisted"
                             ' (%(default_alignment)r in %(blacklist)s)'
                             % locals())
        add_alignment_default = True

    def extractImageAlignment(classes):
        """
        created by --> make_alignment_extractor()
        """
        res = set()
        add_alignment = add_alignment_default
        for cls in classes:
            if cls in blacklist:
                pass
            elif cls.startswith('media-'):
                res.add(cls)
                add_alignment = False
            elif cls.startswith('image-'):
                res.add('media-' + cls[6:])
                add_alignment = False
            elif cls in whitelist:
                res.add(cls)
        if add_alignment:
            res.add(default_alignment)
        return ' '.join(sorted(res))

    return extractImageAlignment

extractImageAlignment = make_alignment_extractor()


class MockLogger(list):
    """
    für Testzwecke; schreibt 2-Tupel in eine Liste und verhält sich ansonsten als solche.

    >>> logger = MockLogger()
    >>> logger.info('Eine Info (%(eins)s)', {'eins': 'zwei'})
    >>> logger.error('%d Fehler', 3)
    >>> list(logger)
    [('INFO', 'Eine Info (zwei)'), ('ERROR', '3 Fehler')]

    Diese Klasse wurde kopiert ins Modul tools.mock;
    zur einfacheren Testbarkeit bleibt sie hier vorerst erhalten.
    """
    def _cook(self, txt, *args):
        if args:
            if not args[1:] and isinstance(args[0], dict):
                return txt % args[0]
            return txt % args
        else:
            return txt

    def error(self, txt, *args):
        self.append(('ERROR', self._cook(txt, *args)))

    def info(self, txt, *args):
        self.append(('INFO', self._cook(txt, *args)))


def sanitize_html(txt, logger, doctype='html', verbose=False):
    r"""
    Gib bereinigten HTML-Code zurück:

    - Entferne ein etwaiges 'html'-Präfix;
    - ergänze ggf. den übergebenen Doctype

    >>> txt = u'html\n<html><title>Bleistift</title></html>'
    >>> log = MockLogger()
    >>> txt = sanitize_html(txt, log)
    >>> txt
    u'<!DOCTYPE html>\n<html><title>Bleistift</title></html>'
    >>> list(log)
    [('ERROR', u"sanitize_html: invalid text start (u'html\\n<html><title>Bleistift</t')"), ('INFO', u'sanitize_html: injecting <!DOCTYPE html>')]
    >>> del log[:]

    Die erneute Bereinigung des Ergebnisses ändert nichts mehr
    und zeitigt auch keine Log-Einträge:

    >>> txt2 = sanitize_html(txt, log)
    >>> txt2 == txt
    True
    >>> list(log)
    []

    Siehe auch --> tools.spoons.stripped_soup.
    """
    offset = 0
    has_doctype = False
    def err(txt, *args, **kwargs):
        return logger.error(u'sanitize_html: '+txt, *args)
    def info(txt, *args, **kwargs):
        return logger.info(u'sanitize_html: '+txt, *args)
    if txt.startswith(u'html'):
        err('invalid text start (%r)', txt[:30])
        offset = txt.find('<', 4)
        if offset == -1:
            err('start of valid html not found!')
            return u''
    if txt[offset:offset+2] == u'<!':
        end_of_doctype = txt.find(u'>', offset+2)
        if end_of_doctype == -1:
            err('end of doctype not found! (%r)', txt[offset:offset+80])
            return u''
        else:
            if verbose:
                info('doctype found: %r', txt[offset:end_of_doctype+1])
            has_doctype = True
    if doctype:
        if not has_doctype:
            injected = u'<!DOCTYPE %(doctype)s>' % locals()
            info(u'injecting %(injected)s', locals())
            return u'\n'.join((injected,
                              txt[offset:],
                              ))
        else:
            # vorhandenen Doctype erhalten:
            return txt[offset:]
    else:
        return txt[offset:]


def _short_str(s):
    l = len(s)
    if l > 25:
        head = s[:10]
        tail = s[-10:]
        return ' ... '.join((head, tail))
    return s

def _shorten(thingy, shortened_subdicts):
    """
    Kürze das übergebene Dings rekursiv und in-place
    """
    if isinstance(thingy, dict):
        for k, v in thingy.items():
            if isinstance(v, dict):
                if k in shortened_subdicts:
                    for sk, sv in v.items():
                        if isinstance(sv, six_string_types):
                            v[sk] = _short_str(sv)
            elif isinstance(v, list):
                _shorten(v, shortened_subdicts)
    elif isinstance(thingy, list):
        for i in range(len(thingy)):
            item = thingy[i]
            if isinstance(item, (dict, list)):
                _shorten(item, shortened_subdicts)
                thingy[i] = item


def shortened_copy(thingy, shortened_subdicts=[]):
    r"""
    Gib eine gekürzte Kopie zurück.

    >>> ori = {'actions': [{'active': True, 'name': 'parse'},
    ...                    {'active': False, 'name': 'missing_images'}],
    ...        'fields': [{'equal': True,
    ...                    'klass': {'html.parser': 'border-blue', 'raw': 'border-blue'},
    ...                    'md5_hash': 'a42ffae42f44792d2647652cb708cb94',
    ...                    'name': 'text',
    ...                    'parsed': {'html.parser': '<div style="float:right">\n<table border="0" '
    ...                                              '... he in Boden und Fels</li>\n</ul><br/>'}}]}
    >>> cpy = shortened_copy(ori)
    >>> cpy is ori
    False

    Die Schlüssel der <shortened_subdicts> werden gekürzt, um die Konsolenausgabe verdaulich zu halten:

    >>> cpy = shortened_copy(ori, ['parsed', 'transformed'])
    >>> cpy['fields'][0]['parsed']['html.parser']
    '<div style ... </ul><br/>'
    >>> ori['fields'][0]['parsed']['html.parser'][:15]
    '<div style="flo'
    >>> cpy['fields'][0]['parsed'] is ori['fields'][0]['parsed']
    False
    """
    res = deepcopy(thingy)
    if shortened_subdicts:
        _shorten(res, shortened_subdicts)
    return res


if __name__ == '__main__':
    # Standard library:
    import doctest
    doctest.testmod()
