# -*- coding: utf-8 -*- vim: ts=8 sts=4 sw=4 si et tw=0
"""\
kitchen.py - Hier wird Suppe verarbeitet ...

Neuimplementierung der HTML-Transformationen auf der Basis von BeautifulSoup
(bs4) und lxml.

Es wurde sich zunächst an den existierenden Methoden (transformCamelCase)
orientiert und deren Transformationen nachgebaut; es ist damit die Hoffnung
verbunden, daß Erweiterungen und Korrekturen zukünftig einfacher werden.
"""

# Python compatibility:
from __future__ import absolute_import, print_function

from six.moves import range

__all__ = (# Allgemeine Transformationen:
           'transform_images',
           'transform_files',
           'transform_tables',
           'transform_links',
           'transform_booklinks',
           'transform_preprocess',
           # für Export:
           'fix_bogus_markup',
           'fix_bogus_markup2',
           'sanitize_marginals',
           'make_id_factory',
           'inject_indexes',
           'resolve_uid_links',
           'resolve_uid_images',
           'load_needed_scripts',
           'fix_braces',
           'fix_subs',
           # erweiterte Skriptunterstützung:
           'append_needed_scripts',  # wie load_needed_scripts
           # für Korrekturen (audit):
           'mark_uid_images',   # markieren
           'check_uid_images',  # korrigieren
           # Extraktionsfunktionen:
           'extract_uid',
           # Daten:
           'CAPTION_PREFIX',
           'TYPE2TEMPLATE',
           )

# Python compatibility:
from six.moves.urllib.parse import parse_qs, urlparse

# Standard library:
from collections import defaultdict
from json import dumps as json_dumps
from string import whitespace

# Zope:
from AccessControl import Unauthorized

# 3rd party:
from bs4 import BeautifulSoup, Comment, NavigableString

# visaplan:
from visaplan.kitchen.forks import (
    appendix_dots,
    convert_dimension_styles,
    extract_linktext,
    get_numeric_px,
    inject_number,
    styledict,
    )
from visaplan.kitchen.spoons import (  # get_strippable_container, strip_empty_successor,
    INSERT_POSITIONS,
    ChapterCounter,
    add_class,
    append_class,
    change_text,
    check_class,
    contents_stripped,
    extract_uid,
    extract_uid_and_tail,
    fence_texts,
    fix_webdivs,
    gen_id_and_name,
    get_id_or_name,
    get_single_element,
    has_all_classes,
    has_any_class,
    has_class,
    insertAdjacentElement,
    interesting_successor,
    is_block_element,
    is_block_with_p,
    is_empty,
    make_classes_generator,
    make_find_expression,
    make_levelfunc,
    make_script,
    make_tag,
    remove_class,
    split_paragraphs,
    strip_linebreaks,
    top_elements,
    )
from visaplan.tools.classes import Proxy
from visaplan.tools.coding import safe_decode
from visaplan.tools.dicts import updated
from visaplan.tools.html import BLOCK_ELEMENT_NAMES, entity
from visaplan.tools.minifuncs import gimme_None

# Local imports:
from .sniff import (
    has_transformed_image,
    is_block,
    is_cooked_animation,
    is_cooked_formula,
    is_cooked_video,
    is_marginal,
    is_marginal_div,
    often_empty,
    )
from .utils import (
    extract_2uids,
    extractImageAlignment,
    image_stepup,
    join_path_and_tail,
    )

# Logging / Debugging:
from visaplan.plone.tools.log import getLogSupport

LOGGER, debug_active, DEBUG = getLogSupport()
ERROR = LOGGER.error
INFO = LOGGER.info
WARN = LOGGER.warning

# Local imports:
from .config import WATCH_ME

# Logging / Debugging:
from pdb import set_trace
from visaplan.tools.debug import log_or_trace, pp, trace_this

lot_kwargs = {'debug_level': debug_active,
              'logger': LOGGER,
              }


# visaplan:
# ---------------------------- [ Exportfunktionalität ... [
from visaplan.kitchen.ids import id_factory
from visaplan.plone.pdfexport.PDFreactor import PDFreactor
from visaplan.tools.minifuncs import makeBool
from visaplan.tools.minifuncs import translate_dummy as _

# Local imports:
from .dispatcher import (
    APPENDIX_DISPATCHER,
    ID_FACTORY,
    DirectoryDispatcher,
    make_headline_element,
    make_toc_entry,
    )
from .tocspecs import ApiFilterTocsOnly

# ---------------------------- ] ... Exportfunktionalität ]


# ------------------------------------------------------ [ Daten ... [
# portal_type -> Template (mit Objekt als aufrufendem Kontext):
TYPE2TEMPLATE = {# 'UnitraccImage': 'kss-image-view',
                 'UnitraccFile':       'kss-file-view',
                 'UnitraccAnimation':  'js-unitraccanimation-view',
                 'UnitraccVideo':      'js-unitraccvideo-view',
                 'UnitraccAudio':      'js-unitraccaudio-view',
                 'UnitraccFormula':    'js-unitraccformula-view',
                 # bisher nicht über portal_type angesteuert:
                 # 'UnitraccTable': 'kss-table-view',
                 # aus visaplan.plone.animations:
                 'FolderishAnimation': 'embed',
                 }
CAPTION_PREFIX = {'UnitraccVideo':     'unitracc-video',
                  'UnitraccAnimation': 'unitracc-animation',
                  'UnitraccFile':      'unitracc-file',
                  'UnitraccAudio':     'unitracc-audio',
                  'UnitraccBinary':    'unitracc-file',
                  'UnitraccFormula':   'unitracc-formula',
                  'UnitraccTable':     'unitracc-table',
                  }
CAPTION_PREFIX_INFOKEY = 'caption-prefix'
COLON_AND_SPACE = ':%(nbsp)s' % entity
ONCLICK_VALUE = ('''window.open(this.href,'','resizable=yes,'''
        '''location=no,menubar=no,scrollbars=yes,status=no,toolbar=no,'''
        '''fullscreen=no,dependent=no,status,width=600,height=800');'''
        '''return false;''')
FEATURES_APPLIED = False
BOOKLINK_MAP = {
        'book-link-image': {
            'numbers_from': 'picturenumber',
            'ckey': _('Fig.'),  # aber --> assert_features
         },
        'book-link-page': {
            'numbers_from': None,
            'ckey': _('Chapter'),
         },
        'book-link-table': {
            'numbers_from': 'numbertag',
            'ckey': _('Table'),
         },
        'book-link-animation': {
            'numbers_from': 'numbertag',
            'ckey': _('Animation'),
         },
        'book-link-video': {
            'numbers_from': 'numbertag',
            'ckey': _('Video'),
         },
        'book-link-formula': {
            'numbers_from': 'picturenumber',
            'ckey': _('Formula'),
         },
        'book-link-audio': {
            'numbers_from': None,
            'ckey': _('Audio'),
         },
        # in transformBookLinks nicht erwähnt:
        'book-link-literature': {
            'numbers_from': None,
            'ckey': _('Literature'),
         },
        }
for key, dic in BOOKLINK_MAP.items():
    dic['class'] = key
BOOKLINK_CLASSES = frozenset(BOOKLINK_MAP.keys())
END_BRACE = {'(': ')',
             '[': ']',
             # (noch?) nicht verwendet:
             '{': '}',
             '<': '>',
             }
LIGHTBOX_TYPE = defaultdict(lambda: 'image')
if 0 and 'Javascript-Code gefixt und getestet':\
LIGHTBOX_TYPE.update({
    'UnitraccVideo': 'video',
    'UnitraccAnimation': 'swf',
    })
BRACKET_CLASSES = frozenset(['no-breaket', 'unitracc-breaket'])
# zur Übersetzungszeit noch nicht bekannt:
DEFAULT_BRACKET_CLASS = None # FEATURESINFO['bracket_default']
del key, dic
# ---------------------------- [ Exportfunktionalität ... [
ForAttributeCheckingOnly = PDFreactor()
# ---------------------------- ] ... Exportfunktionalität ]
SOFT_HYPHEN = entity['shy']
APPENDIX_NUMBERS_SWITCH = 1
KNOWN_NO_TEMPLATE = frozenset(['UnitraccGlossary',
                               'UnitraccTable',
                               'Folder',
                               ])
# Klassen von Elementen, die gerne mal leer generiert werden:
USUAL_SUSPECTS = set(['attribute-title', 'attribute-text'])
NAME_OR_ID = set(['name', 'id'])

# -------------------------- [ PDFreactor-Workarounds ... [
# Stand: PDFreactor 7.0.7375, 15.01.2015
#   page-break-before: left ersetzen, wenn Zähler zurückgesetzt werden soll
#   (die eingefügte Seite gehört zum erzeugenden Bereich)
WA_INJECT_BLANK_PAGES = ('#toc', '#content')
# Es gibt derzeit noch keine CSS-standardisierte Methode,
# Marginalien auf rechten/linken Seiten jeweils außen zu plazieren:
WA_REFLECT_MARGINALS = ('.marginalia',)
# -------------------------- ] ... PDFreactor-Workarounds ]

# http://docs.mathjax.org/en/latest/dynamic.html#loading-mathjax-dynamically
MATHJAX_CDN_URL = "//cdn.mathjax.org/mathjax/latest/MathJax.js"
MATHJAX_CONFIG_TEXT = r"""
MathJax.Hub.Config({"
  menuSettings: {zoom: "Click"
                 },
  tex2jax: {inlineMath: [['$*$','$*$'],
                         ['\\\\(','\\\\)']
                         ],
            balanceBraces: true
            }
});
"""
# http://docs.mathjax.org/en/latest/config-files.html:
MATHJAX_CONFIG_CHOICE = "TeX-AMS_HTML"
MATHJAX_CONFIG_CHOICE = "TeX-HTMLorMML"
MATHJAX_CONFIG_CHOICE = "TeX-AMS-MML_HTMLorMML"
MATHJAX_URL_WITH_CONFIG = (
    "%(MATHJAX_CDN_URL)s?config=%(MATHJAX_CONFIG_CHOICE)s"
    ) % globals()
MATHJAX_NONHEAD_TEXT = r"""
$(document).ready(function () {
  var head = document.getElementsByTagName("head")[0], script;
  script = document.createElement("script");
  script.type = "text/javascript";
  script.src  = "%(MATHJAX_CDN_URL)s?config=%(MATHJAX_CONFIG_CHOICE)s";
  head.appendChild(script);
});
""" % globals()
# ------------------------------------------------------ ] ... Daten ]


# -------------------------------- [ Debugging-Unterstützung (1) ... [
if WATCH_ME:
    def watch(f):
        f_name = f.__name__
        def inner(soup, hub, info, counter):
            res = f(soup, hub, info, counter)
            lst = list(soup.find_all(class_='watch-me'))
            LOGGER.info('%s: %d watched elements%s',
                        f_name, len(lst), len(lst) and ' ...' or '')
            if lst:
                for elem in lst:
                    LOGGER.info(str(elem))
                LOGGER.info('... %s', f_name)
        inner.__name__ = f_name + '_inner'
        return inner
else:
    def watch(f):
        return f
# -------------------------------- ] ... Debugging-Unterstützung (1) ]


# ------------------------------------------- [ Transformationen ... [
"""
Die Transformationsfunktionen arbeiten mit den per Referenz übergebenen
Objekten soup, hub, info und counter:

    soup    - der HTML-Baum, von BeautifulSoup erzeugt
    hub     - zum einfachen Zugriff auf Browser, Adapter und View-Methoden
              (siehe oben);
              statt context.getBrowser('name') reicht z. B. hub['name']
    info    - sammelt Informationen über den (während der Verarbeitung
              unveränderlichen) Kontext
              (siehe oben)
    counter - Zähler
"""

@watch
def transform_preprocess(soup, hub, info, counter):
    """
    Bereinigung von Fehlern wie z. B. vorwitzigen HTML-Kommentaren
    (*vor* der weiteren Verarbeitung)
    """
    found = 0
    for comment in soup.findAll(text=is_comment):
        if comment.string.strip() == '.question':
            found += 1
            comment.extract()
    if found:
        LOGGER.warning('%s: %d ".question"-Kommentare entfernt',
                       info['context'],
                       found)
    # Präfix für jede uid nur einmal berechnen (sonst gibt es Numerierungsfehler):
    info[CAPTION_PREFIX_INFOKEY] = defaultdict(gimme_None)
    # ---------------------- [ Exportprofil vorhanden? ... [
    if info['_profile'] is not None:  # nicht mehr: profile_id
        api_lines = (info['_profile']['pdfreactor_api_calls'] or '').strip()
        if api_lines:
            dic = ApiFilterTocsOnly(hub=hub)(api_lines,
                                             unused=ForAttributeCheckingOnly)
            if dic:
                info.update(dic)
            else:
                hub['message']('Error parsing API calls',
                               messageType='error')
        else:
            info['tocs'] = []
            info['appendixes'] = []
    # ---------------------- ] ... Exportprofil vorhanden? ]


@watch
def transform_images(soup, hub, info, counter):  # ---- [ transform_images ... [
    """
    Verarbeite alle img-Elemente, die per UID eingebunden sind;
    außer einfachen Bildern können diese auch Animationen, Videos und Formeln
    repräsentieren.
    """
    assert_features(hub, info)
    FLAG_CLASS = intern('transformed-image')
    changes = 0
    fact = info['print_px_factor']  # Skalierungsfaktor für width-/height-Angaben
    for item in soup.find_all('img'):
        if check_class(item, FLAG_CLASS):
            continue
        dic = get_imgtag_info(item, info)
        uid = dic.get('uid')
        # bei Bildern ohne UID ist nichts zu tun:
        if uid is None:
            continue

        brain = hub['getbrain'](uid)
        if brain is None:
            continue

        imgpath = info['uid2path'][uid]
        assert imgpath  # 'uid %(uid)r lacks an imgpath!' % locals()

        b_pt = brain.portal_type
        b_mt = brain.getContentType  # mime type
        # NUMMERN
        ckey = count_key(b_pt, b_mt)
        # --------------------------------------------- ... transform_images ...
        if ckey == 'Formula':
            if brain.getMathjax:
                # später weiterverarbeiten (--> transform_booklinks):
                replacement = '<a class="unitracc-formula" href="/resolveuid/%(uid)s">Formula</a>' % dic
                fly = BeautifulSoup(replacement).a
                append_class(fly, FLAG_CLASS)
                item.replace_with(fly)
                continue

        elif ckey in ('Video', 'Animation'):
            dic['onclick'] = imgpath + '/view?contentOnly=True'

        dic['imageAlignment'] = extractImageAlignment(dic['classes'])
        dic['caption'] = str(brain.getCaption)
        dic['legend'] = str(brain.getLegend)
        if 'no-lightbox' not in dic['classes']:
            lbtype = LIGHTBOX_TYPE[b_pt]
            dic['lightbox_value'] = 'lightbox[%(lbtype)s]' % locals()
        else:
            dic['lightbox_value'] = 'no-lightbox'

        # --------------------------------------------- ... transform_images ...
        tmp = info[CAPTION_PREFIX_INFOKEY][uid]
        if tmp is not None:
            dic['number'] = tmp
        # wenn keine Bildunterschrift, gibt es auch keine Nummer:
        elif 'image-caption' not in dic['classes']:
            pass
        elif info['isBook']:
            counter[ckey] += 1
            DEBUG('transform_images (isBook): make_caption_prefix')
            info[CAPTION_PREFIX_INFOKEY][uid] = \
            dic['number'] = make_caption_prefix(hub['translate'](ckey),
                                                info['st_num'], counter[ckey])
        elif info['isStructual']:
            DEBUG('transform_images (isStructual): make_caption_prefix')
            info[CAPTION_PREFIX_INFOKEY][uid] = \
            dic['number'] = make_caption_prefix(hub['translate'](ckey))

        # dic aus get_imgtag_info, und hier ergänzt:
        convert_dimension_styles(item, dic)

        # das div-Element benötigt u. U. doch ein style-Attribut, um die Breite
        # festzulegen:
        width = None
        attrs = item.attrs
        if 'width' in dic:
            width = int(dic['width'])
        elif 'scaling' in dic:
            scaling = dic['scaling']
            if scaling is not None:
                try:
                    width = scaling.split('x')[0]
                except (IndexError, TypeError) as e:
                    ERROR('UID %(uid)r: Error %(e)r splitting the scaling %(scaling)r!',
                          locals())
                else:
                    attrs['width'] = width
                    width = int(width)
        if width is not None:
            if fact != 1:
                width = int(width * fact)
                attrs['width'] = str(width)
                height = get_numeric_px(attrs.get('height'))
                if height:
                    attrs['height'] = str(height * fact)
            dic['outer_width_style'] = 'width: %dpx' % (width+4,)

        dic['img_elem'] = str(item)
        # Das src-Attribut des img-Elements selbst wird vorerst noch
        # (da evtl. Kriterium für weitere Transformationen)
        # in einem späteren Aufruf modifiziert:
        assert 'href' not in dic
        dic['href'] = imgpath + '/image'
        replacement = hub['kss-image-view'](**dic)

        # die Fliege ersetzt die Suppe, die sie gefressen hat:
        fly = BeautifulSoup(replacement).div
        append_class(fly, FLAG_CLASS)
        item.replace_with(fly)
        changes += 1
    return changes
    # ------------------------------------------------- ] ... transform_images ]


@watch
def transform_files(soup, hub, info, counter):  # ------ [ transform_files ... [
    """
    Es werden Hyperlinks verarbeitet, die per UID auf *eingebettete*
    Inhalte verweisen (üblicherweise Animationen und Videos; Bilder werden
    als img-Elemente notiert).  Bei Vorhandensein einer book-link-Klasse
    (siehe BOOKLINK_CLASSES) wird nicht eingebettet, sondern der Hyperlink
    bearbeitet; siehe --> transform_booklinks().

    In Abhängigkeit vom Typ des verwiesenen Objekts wird eine View-Methode
    aufgerufen, die genau ein Container-HTML-Element erzeugen sollte,
    das anstelle des notierten Hyperlinks eingefügt wird.
    """
    FLAG_CLASS = intern('transformed-file')
    wo_template = defaultdict(int)
    changes = 0
    for item in soup.find_all('a'):
        dic = get_atag_info(item)
        if has_booklink_class(dic, info):
            # Verarbeitung durch transform_booklinks
            continue

        if 'contains-preview-img' in dic['classes']:  # aus kss-image-view.pt
            # Bild anzeigen, nicht das enthaltene Video etc.
            continue

        uid = dic.get('uid')
        # bei Links ohne UID ist nichts zu tun:
        if uid is None:
            continue

        # Doppelverarbeitung verhindern:
        if FLAG_CLASS in dic['classes']:
            continue

        # ---------------------------------------------- ... transform_files ...
        brain = hub['getbrain'](uid)
        if brain is None:
            continue

        # Letztlich muß das Objekt seine Methode aufrufen;
        # da kann man es auch schonmal wecken ...
        o = brain._unrestrictedGetObject()
        if not o:
            continue

        o_pt = o.portal_type
        # der mime_type wird bisher nicht verwendet, daher nicht ermittelt:
        ckey = count_key(o_pt, '', True)

        captionPrefix = None
        if ckey is not None:
            captionPrefix = info[CAPTION_PREFIX_INFOKEY][uid]
            if captionPrefix is not None:
                pass
            elif info['isBook']:
                counter[ckey] += 1
                DEBUG('transform_files (isBook): make_caption_prefix')
                info[CAPTION_PREFIX_INFOKEY][uid] = \
                captionPrefix = make_caption_prefix(hub['translate'](ckey),
                                                    info['st_num'], counter[ckey])
            elif info['isStructual']:
                DEBUG('transform_files (isStructual): make_caption_prefix')
                info[CAPTION_PREFIX_INFOKEY][uid] = \
                captionPrefix = make_caption_prefix(hub['translate'](ckey))

        # ---------------------------------------------- ... transform_files ...
        t_id = TYPE2TEMPLATE.get(o_pt)
        if t_id:
            fly = None
            try:
                method = o.unrestrictedTraverse(t_id)
                replacement = method(captionPrefix=captionPrefix)
                fly = get_single_element(replacement)
                if 'None:' in replacement:
                    LOGGER.warning("'None:' contained in %(o)r(%(t_id)r)() result",
                                   locals())

            except Unauthorized as e:
                LOGGER.error('Kein Zugriff auf %(o_pt)r mit UID %(uid)s!', locals())
                fly = get_single_element(hub['placeholder-unauthorized'
                                             ](uid=dic['uid'],
                                               type=o_pt))
                LOGGER.info('%(o_pt)r ersetzt durch Platzhalter', locals())
            except Exception as e:
                LOGGER.error('Fehler bei %(o_pt)r mit UID %(uid)s!', locals())
                LOGGER.exception(e)
                fly = get_single_element(hub['placeholder-error'
                                             ](uid=dic['uid'],
                                               type=o_pt))
                LOGGER.info('%(o_pt)r ersetzt durch Platzhalter', locals())
            # ------------------------------------------ ... transform_files ...
            if fly is not None:
                item.replace_with(fly)
                changes += 1

        elif o_pt == 'UnitraccLiterature':
            add_class(item, 'unitracc-literature')
            changes += 1
        else:
            if o_pt in KNOWN_NO_TEMPLATE:
                wo_template[(o_pt, 'known')] += 1
            else:
                wo_template[(o_pt, 'unknown')] += 1
                if 0:
                    ERROR('No template for type %(o_pt)r\n(%(item)s)', locals())
    if wo_template and 0:
        pp(('transform_files:', dict(wo_template)))
    return changes
    # -------------------------------------------------- ] ... transform_files ]


@watch
#@log_or_trace(trace=1, **updated(lot_kwargs, debug_level=1))
def transform_tables(soup, hub, info, counter):  # ---- [ transform_tables ... [
    """
    Verarbeite alle Hyperlinks, die ein Tabellenobjekt einbetten,
    und ersetze sie durch den vom Template 'kss-table-view' erzeugten Code.

    a.unitracc-table --> div.area-table
    """
    # CHECKME: läßt sich diese Funktionalität in transform_files integrieren?
    first = True
    FLAG_CLASS = intern('transformed-table')

    # Problem: Zugriffsfehler beim unangemeldeten Zugriff auf eingebettete Tabellen,
    #          die in der Mediathek abgelegt sind.
    #          Bei Bildern funktioniert das; aber ähnlicher wäre transform_files ...
    # Beobachten: klappt es bei Animationen, Videos usw.?
    sm = None
    try:
        for item in soup.find_all('a'):
            dic = get_atag_info(item)
            if 'unitracc-table' not in dic['classes']:
                continue
            uid = dic['uid']
            if uid is None:
                continue

            if FLAG_CLASS in dic['classes']:
                continue

            if first:
                get_object = hub['rc'].lookupObject
                # derselbe für alle hier verarbeiteten Funde:
                ckey = count_key('UnitraccTable', '', True)
                assert ckey is not None
                ckey_readable = hub['translate'](ckey)
                captionPrefix = None
                t_id = 'kss-table-view'  # gf: templates/kss-table-view.pt

                sm = hub['securitymanager']
                sm(userId='system')
                sm.setNew()

                first = False

            # --------------------------------------------- ... transform_tables ...
            # Es wird das Objekt benötigt, um die View-Methode aufrufen zu können:
            o = get_object(uid)
            if o is None:
                LOGGER.error('UID %(uid)r: Tabelle nicht gefunden!', locals())
                continue

            # Dies (is...) bleibt über den kompletten Vorgang hinweg unverändert:
            captionPrefix = info[CAPTION_PREFIX_INFOKEY][uid]
            if captionPrefix is not None:
                pass
            elif info['isBook']:
                counter[ckey] += 1
                DEBUG('transform_tables (isBook): make_caption_prefix')
                info[CAPTION_PREFIX_INFOKEY][uid] = \
                captionPrefix = make_caption_prefix(ckey_readable,
                                                    info['st_num'],
                                                    counter[ckey])
            elif info['isStructual']:
                DEBUG('transform_tables (isStructual): make_caption_prefix')
                info[CAPTION_PREFIX_INFOKEY][uid] = \
                captionPrefix = make_caption_prefix(ckey_readable)

            # --------------------------------------------- ... transform_tables ...
            DEBUG('Tabelle #%(uid)s --> Prefix %(captionPrefix)r', locals())
            try:
                # pro Objekt geholt, also nicht aus Hub;
                # ./templates/kss-table-view.pt:
                method = o.restrictedTraverse('kss-table-view')
                replacement = method(captionPrefix=captionPrefix)
                fly = BeautifulSoup(replacement).div
            except Unauthorized as e:
                LOGGER.error('Kein Zugriff auf Tabelle mit UID %(uid)s!', dic)
                # ./templates/placeholder-unauthorized.pt:
                fly = get_single_element(hub['placeholder-unauthorized'
                                             ](uid=uid,
                                               type='table'))
                LOGGER.info('Tabelle ersetzt durch Platzhalter')
            except Exception as e:
                LOGGER.error('Fehler bei Tabelle mit UID %(uid)s!', dic)
                LOGGER.exception(e)
                # ./templates/placeholder-error.pt:
                fly = get_single_element(hub['placeholder-error'
                                             ](uid=uid,
                                               type='table'))
                LOGGER.info('Tabelle ersetzt durch Platzhalter')
            else:
                append_class(fly, FLAG_CLASS)
            item.replace_with(fly)
            continue
            # noch nicht erfolgreich getestet; keine Rechenzeit verschwenden:
            pa = get_strippable_container(fly, include_start=True)
            if pa is not None:
                if strip_empty_successor(pa):
                    print('Quatsch entfernt')
                else:
                    print('Keinen Quatsch gefunden')
            else:
                print('Kein Quatschkandidat gefunden')
    finally:
        if sm is not None:
            sm.setOld()
        return not first
    # ------------------------------------------------- ] ... transform_tables ]


@watch
def transform_links(soup, hub, info, counter):
    """
    Verpasse allen verbliebenen a-Elementen, die die Klasse
    'content-only' haben, ein längliches onclick-Attribut.

    Muß nach --> transform_booklinks aufgerufen werden!
    """
    # ----------- [ Export ... [
    if info['_remove_links']:
        return
    # ----------- ] ... Export ]

    # eine FLAG_CLASS ist nicht nötig

    for item in soup.find_all('a'):
        attrs = item.attrs
        if 'content-only' not in attrs.get('class', []):
            continue
        # onclick schon vorhanden, oder kein href:
        if attrs.get('onclick') or not attrs.get('href'):
            continue

        attrs['onclick'] = ONCLICK_VALUE


def assert_features(hub, info):
    """
    Stelle sicher, daß die Festlegungen aus dem unitraccfeature-Browser
    übernommen wurden
    """
    global FEATURES_APPLIED
    if not FEATURES_APPLIED:
        features = hub['unitraccfeature'].all()
        BOOKLINK_MAP['book-link-image'
                     ]['ckey'] = features['text_fig_dot']
        FEATURES_APPLIED = True

@watch
def transform_booklinks(soup, hub, info, counter):
    """
    Verarbeite die a-Elemente, die eine Klasse "book-link-..." haben
    und mit resolveuid auf ein Unitracc-Inhaltsobjekt verweisen.

    Mit der Klasse "content-only" wird der Titel ausgelesen;
    vorbehaltlich der Klasse "no-breaket" (Name historisch bedingt) wird eine
    Klammerung gesetzt:
    - [eckige Klammern], wenn der Titel ermittelt wird und nicht selbst schon
      entsprechend geklammert ist;
    - (runde Klammern), wenn der Titel *nicht* ermittelt wird.

    >>> a_elem = '<a class="book-link-page unitracc-breaket" href="./resolveUid/3a8cba99f7929f01aa4435416d3af527#e57642bdab607084f202845729298f75">(Abschnitt 5.2.1)</a>'
    >>> txt = '<body><p>'+a_elem+'</p></body>'
    >>> soup = BeautifulSoup(txt)

    """
    FLAG_CLASS = intern('transformed-booklink')
    assert_features(hub, info)

    the_body = soup.body
    make_tooltip_divs = the_body and info['_make_tooltip_divs']
    # Tooltip-Divs: dem Body als letztes Element einen Container hinzufügen
    if make_tooltip_divs:
        tooltips = []
        if '_tooltip_uids' in info:
            tooltip_uids = info['_tooltip_uids']
        else:
            tooltip_uids = info['_tooltip_uids'] = {}

    # make_id = hub[ID_FACTORY]

    for item in soup.find_all('a'):
        attrs = item.attrs
        dic = get_atag_info(item)
        # Alles hier wird durch CSS-Klassen gesteuert;
        # ohne Klassen gibt es nichts zu tun:
        if not dic['classes']:
            continue

        bl_dic = {}
        targetUid = None
        for cls in dic['classes']:
            try:
                bl_dic = BOOKLINK_MAP[cls]
            except KeyError:
                pass
            else:
                break

        # die Verarbeitung muß nicht erfolgreich gewesen sein:
        if check_class(item, FLAG_CLASS):
            continue

        new_title = None
        # insbesondere bei älteren Inhalten ist
        # 'unitracc-breaket' nicht zuverlässig vorhanden;
        # transformBookLinks verwendete es trotzdem
        add_brackets = apply_brackets(dic, info)
        if 'content-only' in dic['classes']:
            if not dic['href']:
                continue

            uid, targetUid = extract_2uids(dic['href'], info)
            brain = hub['getbrain'](uid)
            if brain is not None:
                brain_title = brain.Title
                new_title = embrace(brain_title,
                                    add_brackets and '[',
                                    bl_dic.get('ckey', brain.id),
                                    hub)
                item.string = new_title
                # Tooltip-Debugging ...
                # item['title'] = 'title ist '+ brain.Title
                # item.href = None
                # add_class(item, 'apply-tooltip')
                if make_tooltip_divs:
                    ttid = 'tooltip-' + uid
                    try:
                        if tooltip_uids[uid]:
                            item['data-tooltipid'] = ttid
                            continue
                    except KeyError:
                        # UID hier erstmals behandelt:
                        txt = safe_decode(brain.getRawText)
                        if txt:
                            tt = soup.new_tag('div', id=ttid)
                            tt.append(make_tag(soup, 'h3', brain_title))
                            paragraphs = top_elements(txt)
                            if paragraphs:
                                if paragraphs[1:] or paragraphs[0].name != 'div':
                                    ham = make_tag(soup, 'div')
                                    for elem in paragraphs:
                                        ham.append(elem)
                                else:
                                    ham = paragraphs[0]
                                tt.append(ham)
                            tooltips.append(tt)
                            # item.insert_after(tt)
                            item['data-tooltipid'] = ttid
                            tooltip_uids[uid] = True
                        else:
                            tooltip_uids[uid] = False
                else:
                    item['data-uid'] = uid
            continue

        if not bl_dic:
            continue

        # NUMMERN hier aus Browser-Methoden (numbertag oder picturenumber)
        args = [hub['translate'](bl_dic['ckey'])]
        if info['isBook']:
            num = None
            # buchartig: Numerierung erzeugen
            args.append(info['st_num'])
            numbers_source = bl_dic['numbers_from']
            if numbers_source is not None:
                # Nur wenn es eine Nummernquelle gibt, wird der Link-Text
                # ersetzt:
                needle_uid, haystack_uid = extract_2uids(dic['href'], info)
                if needle_uid and (needle_uid == haystack_uid):
                    haystack_uid = info['my_uid']
                    # Lokal eingebettetes Bild:
                    if numbers_source == 'picturenumber':
                        # Die Nummer wurde (wenn Ausgabe mit Bildunterschrift)
                        # in --> transform_images vergeben
                        num = info[CAPTION_PREFIX_INFOKEY][uid] or 0
                if num is None:
                    # wenn 0, dann *hat* das Objekt keine Nummer!
                    # (ohne Bildunterschrift eingebettetes Bild)
                    browser = hub[numbers_source]
                    num = browser.get(haystack_uid, needle_uid, bl_dic['class'])
                if num:
                    args.append(num)
                    new_title = embrace(make_booklink_text(*args),
                                        add_brackets and '(',
                                        bl_dic['ckey'],
                                        hub)
            if num is None:
                if add_brackets:
                    new_title = embrace(item.string,
                                        '(',
                                        bl_dic['ckey'],
                                        hub)
                else:
                    continue
        else:
            # nicht buchartig: keine Nummern, kein Doppelpunkt
            args.extend([add_brackets and '(',
                         bl_dic['ckey'],
                         hub])
            new_title = embrace(*args)
        if new_title:
            item.string = new_title
    if make_tooltip_divs and tooltips:
        container = soup.find(id='tooltip-container')
        if container is None:
            attrs = {'id': 'tooltip-container',
                     'style': 'display: none',
                     }
            if 0:
                del attrs['style']
            container = soup.new_tag('div', **attrs)
            the_body.append(container)
        for elem in tooltips:
            container.append(elem)


def _name_and_string(elem, name, s):
    # pp(['fix_braces:', sorted(locals().items())])
    return name == elem.name and s == elem.string


def _log_counter(method, counter, keys):
    for key in keys:
        val = counter[key]
        if val:
            DEBUG('%(method)s, %(key)s: %(val)d', locals())

def _fixcnt_keys():
    return ('-match-next-',
            '-mismatch-next-',
            '-match-prev-',
            '-mismatch-prev-',
            )

def fix_braces(soup, hub, info, counter):
    r"""
    Irgendwo im Prozeß ist Leerraum entstanden um a, em und strong-Elemente!

    >>> txt = '''<p> (siehe\n<b>Tab. 1</b>\n). </p>'''
    >>> txt
    '<p> (siehe\n<b>Tab. 1</b>\n). </p>'
    >>> soup = BeautifulSoup(txt)
    >>> fix_braces(soup, None, None, None)
    ('fix_braces:', {'-match-next-': 1, '-match-prev-': 1, 'b': 1})
    >>> soup.p
    <p> (siehe
    <b>Tab. 1</b>). </p>
    """
    if counter is None:
        print_cnt = True
        counter = defaultdict(int)
    elif counter == 0:
        print_cnt = False
        counter = defaultdict(int)
    else:
        print_cnt = False
    for elem in soup.find_all(['a', 'em', 'strong', 'span',
                               'b', 'i',
                               ]):
        DBG = 0 and _name_and_string(elem, 'em', u'Blending silo')
        if DBG:
            set_trace()
        prev_s = elem.previous_sibling
        prev_text = prev_s and prev_s.string
        prev_linebreak = prev_text and prev_text[-1] == '\n'
        next_s = elem.next_sibling
        next_text = next_s and next_s.string
        next_linebreak = next_text and next_text[0] == '\n'

        try:
            if prev_linebreak:
                prev_text = prev_text.rstrip()
                if prev_text.endswith('('):
                    change_text(prev_s, prev_text)
                    counter[elem.name] += 1
                counter['-match-prev-'] += 1
            else:
                counter['-mismatch-prev-'] += 1
        except (TypeError, IndexError):
            counter['-mismatch-prev-'] += 1

        try:
            if next_linebreak:
                next_text = next_text.lstrip()
                if next_text.startswith(')'):
                    change_text(next_s, next_text)
                    counter[elem.name] += 1
                counter['-match-next-'] += 1
            else:
                counter['-mismatch-next-'] += 1
        except (TypeError, IndexError):
            counter['-mismatch-next-'] += 1

    if print_cnt:
        _log_counter('fix_braces', counter, _fixcnt_keys())


def fix_subs(soup, hub, info, counter):
    r"""
    Irgendwo im Prozeß ist Leerraum entstanden um sub-Elemente!

    >>> txt = '''<p>CaCO\n<sub>3</sub>\n-Gehalt</p>'''
    >>> txt
    '<p>CaCO\n<sub>3</sub>\n-Gehalt</p>'
    >>> soup = BeautifulSoup(txt)
    >>> fix_subs(soup, None, None, None)
    ('fix_subs:', {'-match-next-': 1, '-match-prev-': 1})
    >>> soup.p
    <p>CaCO<sub>3</sub>-Gehalt</p>
    """
    cnt = defaultdict(int)
    for elem in soup.find_all(['sub', 'sup']):
        DBG = 0 and _name_and_string(elem, 'sub', u'3')
        if DBG:
            set_trace()
        prev_s = elem.previous_sibling
        prev_text = prev_s and prev_s.string
        next_s = elem.next_sibling
        next_text = next_s and next_s.string

        try:
            if prev_text[-1] == '\n':
                change_text(prev_s, prev_text[:-1])
                cnt['-match-prev-'] += 1
            else:
                cnt['-mismatch-prev-'] += 1
        except (TypeError, IndexError):
            cnt['-mismatch-prev-'] += 1
        try:
            if next_text[0] == '\n':
                change_text(next_s, next_text[1:])
                cnt['-match-next-'] += 1
            else:
                cnt['-mismatch-next-'] += 1
        except (TypeError, IndexError):
            cnt['-mismatch-next-'] += 1

    if cnt:
        _log_counter('fix_subs', cnt, _fixcnt_keys())


def fix_bogus_markup(soup, hub, info, counter):
    """
    Räume schlechtes Markup auf, das u.a. die Seitenumbruchsteuerung sabotiert.

    Üblicherweise redaktionell entstehende Katastrophen:
    - Sequenzen von <br><br> innerhalb von Absätzen bereinigen
      (stattdessen Absatz aufsplitten)
      - auch Absätze in div-Elementen erzeugen?
    - <br>-Elemente nach (optionalem) Leerraum und Blockelementen entfernen

    Entsteht u. U. durch Template-Textersetzung:
    - leere div-Elemente entfernen
    """
    cnt = defaultdict(int)
    for elem in soup.find_all('div'):
        if is_empty(elem):
            try:
                adict = dict(elem.attrs)
            except AttributeError:
                adict = {}
            classes = [cls
                       for cls in adict.pop('class', [])
                       if not cls in USUAL_SUSPECTS
                       ]

            # ------------- [ leeres clearfix-div ... [
            try:
                classes.remove('clearfix')
                clearfix = True
            except ValueError:
                clearfix = False
            prev_s = elem.previous_sibling
            prev_name = prev_s and prev_s.name
            prev_elem = prev_name and prev_s or None

            delete_this = False
            if not adict:
                if clearfix and prev_name in BLOCK_ELEMENT_NAMES:
                    add_class(prev_elem, 'clearfix')
                    delete_this = True
                elif clearfix:
                    pass
                else:
                    delete_this = True
            if delete_this:
                LOGGER.debug('fix_bogus_markup (1): Entferne %s',
                             elem.extract())
                cnt['del-clearfix-after-block'] += 1
            # ------------- ] ... leeres clearfix-div ]

            next_s = elem.next_sibling
            next_name = next_s and next_s.name
            next_elem = next_name and next_s or None

            delete_this = False
            if not classes:
                keys = set(adict.keys())
                if len(keys) == 1 and keys.intersection(NAME_OR_ID):
                    key = keys.pop()
                    if next_elem and key not in next_elem.attrs:
                        next_elem.attrs[key] = adict[key]
                        delete_this = True
            if delete_this:
                LOGGER.debug('fix_bogus_markup (2): Entferne %s',
                             elem.extract())
                cnt['del-rejoined-name-or-id'] += 1

    for elem in soup.find_all('div', class_='document-page'):
        children = contents_stripped(elem)
        if len(children) != 1:
            continue
        child = children[0]
        if not has_class(child, 'document-page-attributes'):
            continue
        grandchildren = contents_stripped(child)
        if len(grandchildren) != 1:
            continue
        grandchild = grandchildren[0]
        if not has_class(grandchild, 'attribute-title'):
            continue
        add_class(elem, 'contains-single-headline')
        cnt['marked-single-headlines'] += 1
    if cnt and 0:
        pp(('fix_bogus_markup:', dict(cnt),))


def fix_bogus_markup2(soup, hub, info, counter):
    """
    Räume schlechtes Markup auf, das u.a. die Seitenumbruchsteuerung sabotiert.
    Teil 2: nach dem Aufräumen der Marginalien
    """
    # <br><br> bereinigen; Absätze erzeugen:
    split_paragraphs(soup.body or soup, soup,
                     is_block=is_block)
    anything = 0
    inspected = 0
    with_string = 0
    DEBUG('looking for empty blocks ...')
    for elem in soup.find_all(is_block_element):
        s = elem.string
        inspected += 1
        if s is not None:
            with_string += 1
            s1 = s.strip()
            if not s1:
                counter['empty-blocks'] += 1
                anything += 1
                DEBUG('empty block: %(elem)s', locals())
            else:
                l1 = len(s1)
                if l1 < 3:
                    counter[('nearly-empty-blocks', l1)] += 1
                    anything += 1
                    DEBUG('nearly empty block: %(elem)s', locals())
    DEBUG('%(inspected)d blocks inspected; %(with_string)d blocks have strings.', locals())
    DEBUG('%(anything)d empty blocks found', locals())
    if not anything:
        for elem in soup.find_all('div', class_='attribute-title'):
            DEBUG('non-empty block: %(elem)s', locals())

    # strip_linebreaks ist offenbar noch fehlerhaft:
    return
    # Unter den hierdurch nicht erzeugten bzw. bereinigten Absätzen kann es
    # noch welche geben, die mit einem <br> beginnen oder enden,
    # ggf. mit Leerraum; außerdem leere Absätze ...
    for elem in soup.find_all('p'):
        strip_linebreaks(elem, remove_empty=True)
    return
    # ... und Text, der "neben" Absätzen steht:
    if 1:
        removed = 0
        for elem in soup.find_all(often_empty):
            # Der Filter often_empty darf nur Elemente liefern,
            # für die is_empty sinnvoll ist!
            if is_empty(elem):
                removed += 1
                print('*' *40, 'entferne:', elem.extract())
        # (momentan werden hier noch leere Absätze erzeugt)
        for elem in soup.find_all('div', class_='attribute-text'):
            if fence_texts(elem, soup,
                           is_block=is_block):
                print('#'*40, 'fence_texts +++ '*3)
                print(elem)
        if 1:
            for elem in soup.find_all(is_block_with_p):
                if fence_texts(elem, soup,
                               is_block=is_block):
                    print('#'*40, 'fence_texts ... '*3)
                    print(elem)
        hoppla = 0
        for elem in soup.find_all(often_empty):
            # Der Filter often_empty darf nur Elemente liefern,
            # für die is_empty sinnvoll ist!
            if is_empty(elem):
                hoppla += 1
                print(elem.extract())
        print(removed, ' leere Dingse wurden entfernt.')
        if hoppla:
            print('#'*79)
            print(('fence_texts hat offenbar %d leere Absaetze'
                   ' erzeugt!'
                   % (hoppla,)))
            print('#'*79)
    # Marginalien-DIVs möglichst dem nächsten Block einverleiben -
    # aber natürlich keinem leeren
    # (weshalb dies *nach* der Entfernung leerer Blöcke geschehen muß!)
    for elem in soup.find_all(is_marginal_div):
        sink = interesting_successor(elem)
        if (sink is not None
            and sink.name in ('p', 'div')
            and not is_marginal(sink)
            ):
            elem.name = 'span'
            sink.insert(0, elem.extract())


def sanitize_marginals(soup, hub, info, counter):
    """
    Räume die Marginalspalte auf:

    - Jegliche Bilder in der Marginalspalte sind kleine Piktogramme, die
      keinesfalls in einer Lightbox vergrößert betrachtet oder in einem
      Bildverzeichnis aufgeführt werden sollen
    - div.web mit Inhalt "-" ersetzen durch weiches Trennzeichen
    - span-Elemente (verträglicher, z. B. in Absätzen) werden in div gewandelt
    """
    for container in soup.find_all(is_marginal):
        remove_class(container, 'marginal')
        add_class(container, 'marginalia')
        # Unitracc, Güteschutz:
        # Bilder in Marginalien erhalten;
        # TODO: Steuerungsmöglichkeit, am besten im Exportprofil;
        #       Vorgabewert evtl. konfigurierbar
        continue
        for div in container.find_all(has_transformed_image):
            img = None
            for a in div.find_all('a'):
                try:
                    img = a.img.extract()
                except AttributeError:
                    continue
                else:
                    title = a.attrs.get('title')
                    if title:
                        img.attrs['title'] = title
                    break
            if img is not None:
                div.replace_with(img)
    # Bislang nur in Marginalien gefunden, aber wer weiß ...
    fix_webdivs(soup, counter)


# ------------------------- [ für Export: Indexe injizieren ... [
def has_headline_span(elem):
    for subel in elem.children:
        try:
            if has_any_class(subel, ('chapter-number', 'headline-text')):
                return True
        except AttributeError:
            pass
    return False


def make_id_factory(*soups):
    """
    Lies alle id- und name-Attribute aus und gib eine id_factory
    zurück, die diese als belegt erkennt.

    Wenn mehrere Suppen gelesen werden, ist es möglich und sogar
    wahrscheinlich, daß ids doppelt vorkommen; wenigstens die neu
    erzeugten sollen aber eindeutig sein!
    """
    all_ids = set()
    for soup in soups:
        for item in soup.find_all(True):
            # der Einfachheit halber auch die name-Attribute
            # in die Ausschlußliste aufnehmen
            # (wenn auch strenggenommen nur bei a-Elementen relevant):
            for val in gen_id_and_name(item):
                all_ids.add(val)
    return id_factory(all_ids)


# @trace_this
def mark_structure_headlines(soup, hub, info, counter):
    """
    Markiere die Überschriften, die aus der Dokumentstruktur erzeugt wurden
    """
    HTML_HEADLINES = ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']
    generate_interesting = make_classes_generator('^level-[1-9][0-9]*$')
    for div in soup.find_all('div', class_='document-page'):
        interesting = generate_interesting(div)
        # Es sollte jeweils genau eine Klasse in der Liste sein:
        for cls in interesting:
            hX = div.find(HTML_HEADLINES)
            if hX is not None:
                add_class(hX, 'headline-'+cls)


# @trace_this
def inject_indexes(soup, hub, info, counter):
    """
    Injiziere die spezifizierten Verzeichnisse
    """
    if not soup.text:
        return
    # Indexe erzeugen?
    doit = False
    for key in ('appendixes', 'tocs'):
        for spec in info[key]:
            if spec['inputlist']:
                doit = True
                break
    if not doit:
        LOGGER.info('Keine Verzeichnisse konfiguriert')
        return

    mark_structure_headlines(soup, hub, info, counter)
    # --------------------- [ ID-Kollisionen vermeiden ... [
    make_id = hub[ID_FACTORY] = make_id_factory(soup)
    # --------------------- ] ... ID-Kollisionen vermeiden ]

    # ------------------------------------------ [ TOC ... [
    wheel = DirectoryDispatcher(soup, info, hub)
    make_appendix = bool(wheel)

    POSITION_FALLBACK = True
    this_toc = None
    first = True
    for spec in info['tocs']:
        if first:
            first = False
        else:
            raise ValueError('Es wird derzeit nur *ein*'
                             u'Inhaltsverzeichnis unterstützt')

        this_toc = make_tag(soup, 'div', id=make_id('toc', 'toc'))
        headline = make_headline_element(soup, spec, 'h2', hub)
        if headline is not None:
            this_toc.append(headline)
        info['get_level'] = get_level = make_levelfunc(spec['inputlist'])

        # nun einfügen:
        anchor = soup.find(make_find_expression(spec['anchor']))
        if anchor is None and not POSITION_FALLBACK:
            raise ValueError("Couldn't find the insertion position for "
                             "the Table of Contents! (%s)"
                             % (spec['anchor'],))

    if this_toc is None and not make_appendix:
        return  # nichts zu tun

    # Falls Anhang, aber kein Inhaltsverzeichnis:
    if get_level is None:
        get_level = lambda x: 0

    level = 0
    chapter = ChapterCounter()
    chapter_tuple = chapter.tuple()
    prev_headline = None

    for item in soup.find_all(True):
        chapter_found = False
        try:
            level = get_level(item)  # wirft ggf. ValueError
            item.string = item.string.strip()
            comparable_headline = extract_linktext(item)
        except ValueError:
            # Keine Überschrift ...
            if make_appendix:
                # ... aber vielleicht etwas anderes?
                wheel.dispatch(item, chapter_tuple)
        except AttributeError as e:
            continue  # das folgende ist vermutlich obsolet
            # sehr wahrscheinlich: item.string is None
            if item.string is None:
                print('item.string is None:')
            else:
                print(e)
            print_indented(item.prettify())
        else:
            # Sequenzen gleicher Überschriften verhindern
            # (häufig, wenn Ordnertitel derselbe ist wie der Titel
            # der ersten Seite)
            if comparable_headline != prev_headline:
                chapter_found = True
                prev_headline = comparable_headline
            else:
                DEBUG('Removing headline %s', item.extract())

        if chapter_found:
            chapter.count(level)
            chapter_tuple = chapter.tuple()
            item = wheel.register_chapter(chapter_tuple, item)
            theid = get_id_or_name(item)
            if theid is None:
                theid = make_id('section')
                item.attrs['id'] = theid
            this_toc.append(
                    make_toc_entry(item,
                                   level))

    # Nun Inhaltsverzeichnis einfügen:
    if this_toc is not None:
        if anchor is not None:
            insertAdjacentElement(anchor, spec['insert_position'], this_toc)
        else:
            ERROR('ToC: Anchor not found; inserting at beginning of <body>')
            insertAdjacentElement(soup.body, 'afterbegin', this_toc)

    if make_appendix:
        appendix = wheel.elem()
        # mindestens eine Liste wurde wirklich erzeugt:
        if appendix is not None:
            spec = info['appendixes'][0]
            anchor = soup.find(make_find_expression(spec['anchor']))
            # Anhang einfügen:
            if anchor is not None:
                insertAdjacentElement(anchor, spec['insert_position'], appendix)
            elif POSITION_FALLBACK:
                ERROR('Appendix: Anchor not found (%(anchor)r); inserting before end of <body>',
                      spec)
                insertAdjacentElement(soup.body, 'beforeend', appendix)
            else:
                raise ValueError("Couldn't find the insertion position for "
                                 "the appendix! (%s)"
                                 % (spec['anchor'],))

            # Einträge des Anhangs ins Inhaltsverzeichnis:
            if this_toc is not None:
                LEVEL = {'h2': 1,
                         'h3': 2,
                         'h4': 3,
                         }
                subtoc = soup.new_tag('div', **{'class': 'appendix-toc'})
                this_toc.append(subtoc)
                chapter = ChapterCounter()
                for item in appendix.find_all(sorted(LEVEL.keys())):
                    theid = make_id('appendix')
                    item.attrs['id'] = theid
                    if APPENDIX_NUMBERS_SWITCH or not has_headline_span(item):
                        level = LEVEL[item.name]
                        chapter.count(level)
                        tup = chapter.tuple()
                        item = inject_number(soup, tup, item, appendix_dots)
                    subtoc.append(
                            make_toc_entry(item,
                                           level))
    # ------------------------------------------ ] ... TOC ]
    return
# ------------------------- ] ... für Export: Indexe injizieren ]

# ------------------------ [ für Export: Skripte injizieren ... [
def get_subkey(portal_type, item):
    if portal_type != 'UnitraccFormula':
        return None
    print(item)


# @trace_this
def load_needed_scripts(soup, hub, info, counter):
    """
    Nur für Export-Modus (nicht für die Transformation von Einzelschnipseln):
    Lade benötigte Skripte nach, sofern nicht gefunden.
    """
    FLAG_CLASS = intern('transformed-file')
    CNT_ANIMATION = ('UnitraccAnimation', '*')
    CNT_VIDEO = ('UnitraccVideo', '*')
    inject_list = ['/++resource++plone.app.jquery.js',
                   '/jquery-integration.js',
                   ]
    inject_styles = []

    for item in soup.find_all(True):
        if is_cooked_animation(item):
            counter[CNT_ANIMATION] += 1
        elif is_cooked_video(item):
            counter[CNT_VIDEO] += 1

    if info['audit-mode']:
        inject_list.append('/audit.js')
        inject_styles.append('/audit.css')
    else:
        inject_styles.append('/audit-off.css')
    # ------ [ Reihenfolge wie in Registry-Zusammenstellung ... [
    inject_list.append('/++resource++jsi18n.js')  # benötigt für custom.js
    inject_list.append('/custom.js')
    if counter[CNT_ANIMATION]:
        inject_list.extend(['/swfobject.js',
                            ])
    if counter[CNT_VIDEO]:
        inject_list.extend(['/video.js',
                            ])
    # ------ ] ... Reihenfolge wie in Registry-Zusammenstellung ]
    if WA_INJECT_BLANK_PAGES or WA_REFLECT_MARGINALS:
        inject_list.append('/pdf-support.js')
    head = soup.head
    if head:
        script_sources = set()
        for scr in head.find_all('script'):
            src = scr.attrs.get('src')
            if src is not None:
                script_sources.add(src)

        for src in inject_list:
            if not src in script_sources:
                head.append(soup.new_tag('script',
                                         src=src,
                                         type='text/javascript'))
                script_sources.add(src)
        for src in inject_styles:
            head.append(soup.new_tag('link',
                                     rel='stylesheet',
                                     href=src,
                                     type='text/css'))
        # lt. RealObjects:
        if 0:\
        head.append(make_tag(soup, 'script',
                             RO_EPILOGUE,
                             type='text/javascript'))
        if WA_INJECT_BLANK_PAGES:
            head.append('\n')
            selector = json_dumps(', '.join(WA_INJECT_BLANK_PAGES))
            head.append(make_tag(soup, 'script', '\n'
                                 'ups.inject_blank_pages(%(selector)s);'
                                 % locals(),
                                 type='text/javascript'))
        if WA_REFLECT_MARGINALS:
            head.append('\n')
            selector = json_dumps(', '.join(WA_REFLECT_MARGINALS))
            head.append(make_tag(soup, 'script', '\n'
                                 'ups.reflect_margin(%(selector)s);'
                                 % locals(),
                                 type='text/javascript'))

    scripts = list(soup.select('head script'))
    counter['script-tags-in-head'] = len(scripts)
# ------------------------ ] ... für Export: Skripte injizieren ]


# ---------------------------- [ für Ajax: Skripte anhängen ... [
def append_needed_scripts(soup, hub, info, counter):
    """
    Wie --> load_needed_scripts, aber für per Ajax ladbare Seiten;
    es werden <script>-Elemente nicht im <head>, sondern am Ende des <body>
    eingefügt.

    Ein "html>body"-Rahmen wird abschließend vom aufrufenden Code entfernt
    (weil beide in der resultierenden Seite strenggenommen ungültig wären
    und daher Skripte nicht ausgeführt würden).
    """
    inject_list = []
    found_mathjax = False
    for item in soup.find_all(True):
        if is_cooked_formula(item):
            mj_elem = item.find('div', class_='mathjax')
            if mj_elem and mj_elem.string:
                found_mathjax = True
                break

    if soup.find('div', class_='question') is not None:
        inject_list.extend(questionnaire_scripts())

    if not inject_list and not found_mathjax:
        return
    # Skripte vorzugsweise am Ende des <body> einfügen
    # (der üblicherweise zum Schluß mit stripped_soup entfernt wird)
    for name in ('body', 'html',
                 ):
        hook = soup.find(name)
        if hook is not None:
            break
    if hook is not None:
        def add(elem):
            return insertAdjacentElement(hook, 'beforeend', elem)
    else:
        add = soup.append

    for src in inject_list:
        add(make_script(soup, src))
    if found_mathjax:
        # Hier nur der Code zum nochmaligen Anstoßen;
        # MathJax.js{?...} und Konfiguration in allgemeinem
        # Seiten-Code einbinden
        add(make_script(soup,
                        txt='MathJax.Hub.Queue(["Typeset", MathJax.Hub]);'))
# ---------------------------- ] ... für Ajax: Skripte anhängen ]


# ----------------------------- [ für Export: UIDs auflösen ... [
def resolve_uid_links(soup, hub, info, counter):
    """
    Entferne alle nicht-lokalen Links (genauer: lösche ihre href-Attribute)
    (Wird aufgerufen, wenn durch setAddLinks(False) angefordert)

    Eine etwaige Umwandlung von UID- in lokale Hyperlinks muß natürlich
    *vorher* geschehen.
    """
    cnt = defaultdict(int)
    first = False # True: aktiviert Debugging-Ausgaben
    for item in soup.find_all('a'):
        attributes = item.attrs
        attribute_names = list(attributes.keys())
        if attribute_names == ['name']:
            cnt['name-only'] += 1
            continue
        if 'href' not in attribute_names:
            cnt['href-missing'] += 1
            continue
        href_value = attributes['href']
        if not href_value:
            cnt['href-empty'] += 1
            continue
        if href_value.startswith('#'):
            cnt['local'] += 1
            continue
        uid, ignored = extract_2uids(href_value, info)
        if uid:
            if soup.find(id=uid) is not None:
                attributes['href'] = '#'+uid
                cnt['resolveuid-converted'] += 1
                continue
            else:
                cnt['resolveuid-external'] += 1
        else:
            cnt['non-local'] += 1
        if first:
            print(item.prettify())
        if info['_remove_links']:
            del attributes['href']
        if first:
            print(item.prettify())
            first = False


def resolve_uid_images(soup, hub, info, counter):
    """
    Ersetze alle resolveuid-Angaben in src-Attributen von Bildern
    durch den aufgelösten Pfad.

    Siehe auch (für Druckausgaben) --> resolve_and_scale_images
    """
    for item in soup.find_all('img', src=True):
        a_dict = item.attrs
        src = a_dict['src']
        uid, tail = extract_uid_and_tail(src)
        if uid is None:
            continue
        try:
            imgpath = info['uid2path'][uid]
        except (KeyError, AttributeError) as e:
            ERROR('resolve_uid_images: UID %(uid)r not found!', locals())
            # _mark_broken_image(item, uid)
            item.name = 'a'
            add_class(item, 'not-found')
            a_dict.update({'title': a_dict['src'],
                           })
            for key in ('src', 'href',
                        'style', 'alt',
                        ):
                if key in a_dict:
                    del a_dict[key]
            item.append(NavigableString('UID '))
            item.append(make_tag(soup, 'tt', uid))
            item.append(NavigableString(' not found!'))
            continue
        if imgpath is None:
            continue
        a_dict['src'] = join_path_and_tail(imgpath, tail)


def resolve_and_scale_images(soup, hub, info, counter):
    """
    Ersetze alle resolveuid-Angaben in src-Attributen von Bildern
    durch den aufgelösten Pfad.

    Siehe auch --> check_uid_images, mark_uid_images

    Da diese Funktion für den PDF-Export vorgesehen ist, wird für Bilder
    i.d.R. die nächsthöhere (steps = 1) verfügbare Auflösung verwendet.
    """
    # mark_missing = makeBool(info['request_var'].get('audit', 'false'))
    mark_missing = info['audit-mode']
    # TODO: Die folgenden Einträge im Exportprofil konfigurierbar machen:
    steps = info['image-size-steps']  # Bildqualität um <steps> Stufen oder auf 'top' verbessern
    # Skalierungsfaktor info['print_px_factor'] nun in transform_images:
    fact = 1  # Skalierungsfaktor für width-/height-Angaben
    # TODO: hier aufräumen und sämtliche Skalierungsfunktionalität entfernen
    pf = 0
    for item in soup.find_all('img', src=True):
        a_dict = item.attrs
        src = a_dict['src']
        uid, tail = extract_uid_and_tail(src)
        if uid is not None:
            imgpath = info['uid2path'][uid]
            if imgpath is None:
                ERROR('resolve_uid_images(%(uid)s): NOT FOUND',
                      locals())
                counter['image-uid-not-found'] += 1
                if mark_missing:
                    _mark_broken_image(item, uid)
                continue
            INFO('resolve_uid_images(%(uid)s) --> %(mgpath)r',
                 locals())
            # die Attribute width und height sind vorhanden,
            # wenn die Größe des Bilds redaktionell angepaßt wurde
            iraw_width = a_dict.pop('width', '')
            iraw_height = a_dict.pop('height', '')
            iori_width = get_numeric_px(iraw_width)
            iori_height = get_numeric_px(iraw_height)
            if iori_width:
                try:
                    width = int(iori_width * fact)
                    if iori_height:
                        height = int(iori_height * fact)
                    else:
                        height = 'auto'
                except (ValueError, TypeError) as e:
                    ERROR(str(e))
                    ERROR('div for uid %(uid)r: '
                          'width = %(width)r, '
                          'height = %(height)r, '
                          'fact = %(fact)r'
                          'a_dict = %(a_dict)r',
                          locals())
                    continue
                else:
                    # beide neu setzen oder keinen:
                    a_dict['width'] = str(width)
                    if height != 'auto':
                        a_dict['height'] = str(height)
                # ebenfalls nur, wenn Breite und Höhe angegeben:
                if steps:
                    try:
                        tail = image_stepup(tail, steps)
                    except KeyError:
                        pass
            a_dict['src'] = join_path_and_tail(imgpath, tail)
            counter['image-uid-converted'] += 1
            if False and fact == 1:
                continue
            # numerische Breite angegeben; ...
            if width:
                # nun ggf. noch den Container nachziehen
                # und für die Umrandung 4px zugeben:
                depth = 1
                parent = None
                for p in item.find_parents('div'):
                    if has_class(p, 'media'):
                        parent = p
                        break
                    if depth >= 3:
                        break
                    depth += 1
                if parent is None:
                    INFO('div for uid %(uid)r: parent (div.media) not found',
                         locals())
                    continue
                pa_dict = parent.attrs
                if not pf:
                    INFO('%(item)r: parent is %(parent)r', locals())
                    pf = 1
                else:
                    INFO('parent found', locals())

                # das Container-div.media wurde gefunden
                p_styles = styledict(pa_dict.get('style', ''))
                if 'width' in p_styles or 'height' in p_styles:
                    WARN('%(item)r:\nheight and/or width given'
                         ' both in attributes and style',
                         locals())
                praw_width = pa_dict.get('width', '')
                pori_width = get_numeric_px(praw_width)
                if pori_width:
                    if (pori_width == iori_width):
                        tell = INFO
                    else:
                        tell = WARN
                    verb = 'Changing'
                    oldval_info = ' (was %(praw_width)r)' % locals()
                elif praw_width:  # andere als px-Angabe
                    WARN('div for uid %(uid)r: '
                         "Won't change non-pixel "
                         'width style %(praw_width)r',
                         locals())
                    continue
                else:
                    tell = INFO
                    verb = 'Setting'
                    # numerische Pixelbreite, jedenfalls fixen:
                    oldval_info = ''
                p_newwidth = '%dpx' % (width + 4)  # Zugabe für Rand
                p_styles['width'] = p_newwidth
                tell('div for uid %(uid)r: %(verb)s width '
                     'to %(p_newwidth)s%(oldval_info)s',
                     locals())
                pa_dict['style'] = '; '.join([': '.join(tup)
                                              for tup in sorted(p_styles.items())
                                              ])
                if 'height' in p_styles:
                    height = p_styles['height']
                    WARN('div for uid %(uid)r: '
                         'height %(height)r not adjusted!',
                         locals())
# ----------------------------- ] ... für Export: UIDs auflösen ]
# ------------------------------------------- ] ... Transformationen ]


# ---------------------------------- [ Informationen extrahieren ... [
def check_uid_images(soup, hub, info, counter=None):
    """
    Prüfe die per UID eingebundenen Bilder daraufhin, ob sie gefunden
    werden können; generiere 3-Tupel (ID, UID, Suffix), um die
    Korrektur zu unterstützen.

    Wenn das info-Argument einen Schlüssel 'uid-substmap' hat,
    werden nicht gefundene UIDs automatisch ersetzt, sofern ein Ersatz
    bekannt ist.

    Das id-Attribut wird für alle behandelten Elemente neu erzeugt;
    beim Quellcode-Audit ist es wichtig, daß trotz mehrerer Suppen
    die IDs eindeutig sind.

    Siehe auch --> resolve_uid_images
    """
    substmap = info.get('uid-substmap', {})
    review_existing = info.get('review-existing', False)
    make_id = hub[ID_FACTORY]
    for item in soup.find_all('img', src=True):
        src = item.attrs['src']
        uid, tail = extract_uid_and_tail(src)
        if uid is not None:
            brain = hub['getbrain'](uid)
            if brain is not None:
                if review_existing:
                    prefix = 'ok'
                else:
                    continue
            else:
                prefix = 'broken'
            for i in range(5): print()
            try:
                other = substmap[uid]
            except KeyError:
                print('***', uid, 'not found ***')
            else:
                id = make_id(prefix)
                item.attrs['id'] = id
                if other:  # Es gibt einen bekannten Ersatz
                    item.attrs['src'] = '/'.join(('/resolveuid',
                                                  other,
                                                  tail,
                                                  ))
                    print('***', uid, '-->', other+':')
                    print(item)
                    for i in range(5): print()
                    other = None
            yield (id, uid, tail)


def mark_uid_images(soup, hub, info, counter=None):
    """
    Prüfe die per UID eingebundenen Bilder daraufhin, ob sie gefunden
    werden können, und markiere das <img>-Element andernfalls, um die
    Korrektur zu unterstützen.

    Von @@transform.audit auf den rohen Text angewendet (nicht geparst);
    die Fundstellen werden daher nicht mit id-Attributen versehen.

    Siehe auch --> check_uid_images, resolve_uid_images
    """
    cnt = 0
    for item in soup.find_all('img', src=True):
        src = item.attrs['src']
        uid, tail = extract_uid_and_tail(src)
        if uid is not None:
            brain = hub['getbrain'](uid)
            if brain is not None:
                continue
            _mark_broken_image(item, uid)
            cnt += 1
    return cnt


def _mark_broken_image(item, uid, make_id=None):
    add_class(item, 'not-found')
    alt = item.attrs.get('alt', '').strip()
    if not alt:
        item.attrs['alt'] = 'XXX'
    title = item.attrs.get('title', '').strip()
    if not title:
        item.attrs['title'] = 'UID %(uid)s not found' % locals()
    if make_id is not None:
        item.attrs['id'] = make_id('broken')


def get_imgtag_info(tag, info=None):
    """
    Extrahiere Informationen aus dem img-Tag

    >>> html = '<img>'
    >>> tag = BeautifulSoup(html).img
    >>> _si(get_imgtag_info(tag))
    [('classes', []), ('scaling', None), ('src', None), ('uid', None), ('width', 'auto')]

    Der Rückgabewert ist ein dict-Objekt; die Wandlung in eine
    sortierte Liste (siehe _si-Funktion) dient allein Doctest-Zwecken.

    >>> html = '<img src="/honk/resolveUid/abc123?scaling=120x180">'
    >>> tag = BeautifulSoup(html).img
    >>> _si(get_imgtag_info(tag))
    [('classes', []), ('scaling', '120x180'), ('src', '/honk/resolveUid/abc123?scaling=120x180'), ('uid', 'abc123'), ('width', '120px')]

    >>> html = ('<img class="position-7" alt="image" src="./resolveUid/'
    ...   'a884309bfa0b67538a74e7351bcf1b57/@@scaling/get?scaling=360x240">')
    >>> tag = BeautifulSoup(html).img
    >>> _si(get_imgtag_info(tag))
    [('classes', ['position-7']), ('scaling', '360x240'), ('src', './resolveUid/a884309bfa0b67538a74e7351bcf1b57/@@scaling/get?scaling=360x240'), ('uid', 'a884309bfa0b67538a74e7351bcf1b57'), ('width', '360px')]
    """
    src = tag.attrs.get('src')
    classes = tag.attrs.get('class', [])
    info = {'classes': classes,
            'scaling': None,
            'src': src,
            'uid': None,
            }

    scaling = None
    if src:
        parsed = urlparse(src)
        info['uid'], tail = extract_uid_and_tail(parsed.path)
        width = None
        if tail is not None:
            try:
                width = info['named_width'][tail]
            except KeyError:
                pass
            else:
                info['named_size'] = tail
                info['width'] = width
        # Skalierung extrahieren:
        query_dict = parse_qs(parsed.query)
        scaling = query_dict.get('scaling')
        if scaling:
            assert isinstance(scaling, list)
            scaling = scaling[0]
            info['scaling'] = scaling
    return info


def get_atag_info(tag):
    """
    Extrahiere Informationen aus dem übergebenen a-Tag
    """
    classes = tag.attrs.get('class', [])
    href = tag.attrs.get('href')
    info = {'classes': classes,
            'href': href,
            'uid': None,
            }
    if href:
        parsed = urlparse(href)
        info['uid'] = extract_uid(parsed.path)
    return info


# ---------------------------------- ] ... Informationen extrahieren ]


# ------------------------------------ [ weitere Hilfsfunktionen ... [
def count_key(portal_type, mime_type, prefixed=False):
    """
    Gib einen Zählschlüssel für Objekte des übergebenen Portal- und
    MIME-Typs zurück (wird zur Ausgabe auch übersetzt).

    >>> count_key('UnitraccImage', 'any')
    'Fig.'
    >>> count_key('any', 'application/x-shockwave-flash')
    'Animation'
    >>> count_key('UnitraccFormula', 'any')
    'Formula'
    >>> count_key('any', 'video/mpeg-oder-so')
    'Video'

    Bei anderen kommt None zurück:

    >>> count_key('File', 'text/plain')

    Wenn prefixed True ist, werden zum Schluß Unitracc-Portaltypen
    generisch verwertet:

    >>> count_key('UnitraccAnimation', 'any', True)
    'Animation'
    """
    if portal_type == 'UnitraccImage':
        return BOOKLINK_MAP['book-link-image']['ckey']
    elif mime_type == 'application/x-shockwave-flash':
        return 'Animation'
    elif portal_type == 'UnitraccFormula':
        return 'Formula'
    elif mime_type.startswith('video'):
        return 'Video'
    elif not prefixed:
        return None
    elif portal_type.startswith('Unitracc'):
        return portal_type[8:] or None


@log_or_trace(**lot_kwargs)
def make_caption_prefix(s, *numbers):
    r"""
    >>> make_caption_prefix('Bild')
    u'Bild:\xa0'
    >>> make_caption_prefix('Tabelle', 1, 7)
    u'Tabelle 1-7:\xa0'

    Die erste übergebene Zahl ist üblicherweise eine "globale" Angabe
    (Kapitelnummer o.ä.); weitere Zahlen sind jeweils untergeordnet
    und zählen etwa die Bilder, Literaturverweise o.ä. innerhalb des Kapitels.

    "Falsche" Werte führen zur Basisversion:

    >>> make_caption_prefix('Tabelle', 0, 7)
    u'Tabelle:\xa0'

    Es braucht nur eine Zahl angegeben zu werden:
    >>> make_caption_prefix('Kapitel', 7)
    u'Kapitel 7:\xa0'
    """
    if not numbers:
        return ''.join((s, COLON_AND_SPACE))

    res = [s, ' ']
    first = True
    for num in numbers:
        if not num:
            return ''.join((s, COLON_AND_SPACE))
        if first:
            first = False
        else:
            res.append('-')
        res.append(str(num))
    res.append(COLON_AND_SPACE)
    return ''.join(res)


def make_booklink_text(s, *numbers):
    """
    Wie -> make_caption_prefix, aber ohne Doppelpunkt und non-breaking space:

    >>> make_booklink_text('Bild')
    'Bild'
    >>> make_booklink_text('Tabelle', 1, 7)
    'Tabelle 1-7'

    Die erste übergebene Zahl ist üblicherweise eine "globale" Angabe
    (Kapitelnummer o.ä.); weitere Zahlen sind jeweils untergeordnet
    und zählen etwa die Bilder, Literaturverweise o.ä. innerhalb des Kapitels.

    "Falsche" Werte führen zur Basisversion:

    >>> make_booklink_text('Tabelle', 0, 7)
    'Tabelle'

    Es braucht nur eine Zahl angegeben zu werden:
    >>> make_booklink_text('Kapitel', 7)
    'Kapitel 7'
    """
    if not numbers:
        return s

    res = [s, ' ']
    first = True
    for num in numbers:
        if not num:
            return s
        if first:
            first = False
        else:
            res.append('-')
        res.append(str(num))
    return ''.join(res)


def embrace(s, brace, ifempty, hub):
    """
    Umklammere einen String

    s -- der String
    brace -- '(', '[' oder False
    ifempty -- Fallback-Wert für leeren String
    hub -- liefert ggf. den translate-Adapter

    >>> embrace('eine Tabelle', '[', 'Tabelle', {})
    '[eine Tabelle]'

    Wenn die gewünschten Klammern schon da sind, erfolgt keine Änderung:

    >>> embrace('[eine Tabelle]', '[', 'Tabelle', {})
    '[eine Tabelle]'

    >>> embrace('eine Formel', False, 'Formel', {})
    'eine Formel'
    """
    s = s.strip()
    if not s:
        s = hub['translate'](ifempty.strip())
    if brace:
        end_brace = END_BRACE[brace]
        if s.startswith(brace) and s.endswith(end_brace):
            return s
        return s.join((brace, end_brace))
    return s


def has_booklink_class(elemdict, infodict=None):
    """
    elemdict -- wie von get_atag_info zurückgegeben
    infodict -- wenn angegeben, werden auch weitere mit 'book-link' beginnende
                CSS-Klassen erkannt, und es wird ein Fehler protokolliert

    >>> dic1 = {'classes': 'book-link-video content-only no-breaket'.split()}
    >>> has_booklink_class(dic1)
    True
    >>> dic2 = {'classes': 'unitracc-video'.split()}
    >>> has_booklink_class(dic2)
    False
    """
    if set(elemdict['classes']).intersection(BOOKLINK_CLASSES):
        return True
    if infodict is None:
        return False
    for cls in elemdict['classes']:
        if cls.startswith('book-link'):
            uid = infodict['uid']  # Information über den Kontext
            ERROR('unbekannte book-link-Klasse: %(cls)r (resolveuid/%(uid)s)',
                  locals())
            return True
    return False


def apply_brackets(dic, info):
    """
    Soll geklammert werden?

    dic - das dict mit den aus dem Element extrahierten Informationen
    info - Informationen über den Request
    """
    choice = list(set(dic['classes']).intersection(BRACKET_CLASSES))
    if choice[1:]:
        ERROR('mehr als eine breaket-Klasse vergeben! (%s)',
              ' '.join(choice))
        choice = None
    elif choice:
        choice = choice[0]
    if not choice:
        choice = info['bracket_default']
    return choice == 'unitracc-breaket'


def is_comment(elem):
    return isinstance(elem, Comment)


def mathjax_scripts():
    # Skripte, die zur Darstellung von Formeln mit Hilfe von MathJax
    # eingebunden werden müssen
    return ['/++resource++mathjax-config/TeX-AMS-MML_HTMLorMML.js',
            '/++resource++mathjax/MathJax.js',
            ]


def questionnaire_scripts():
    # Skripte, die zur Fragebogenunterstützung benötigt werden
    return ['/++resource++unitracc-resource/questionnaire.js',
            ]
# ------------------------------------ ] ... weitere Hilfsfunktionen ]


# ------------------------------------ [ Debugging-Unterstützung ... [
def print_indented(txt):
    try:
        for line in txt.strip().split('\n'):
            try:
                print('    ' + line.rstrip())
            except UnicodeEncodeError as e:
                print('*** Hoppla! %s (%r)' % (e, line.rstrip(),))
    except UnicodeEncodeError as e:
        print('!!! %s' % (e,))


def report_replacement(method, soup_old, soup_new, dic=None):
    print()
    print('[ (soup) %(method)s: Ersetze ... [' % locals())
    print()
    print_indented(soup_old.prettify())
    print()
    print('durch')
    print()
    print_indented(soup_new.prettify())
    if dic:
        print()
        pp(dic)
    print()
    print('] ... (soup) %(method)s ]' % locals())
    print()


def _si(dic):
    """
    Für Doctest: sorted items
    """
    return sorted(dic.items())
# ------------------------------------ ] ... Debugging-Unterstützung ]


if __name__ == '__main__':
    # Standard library:
    import doctest
    doctest.testmod()
