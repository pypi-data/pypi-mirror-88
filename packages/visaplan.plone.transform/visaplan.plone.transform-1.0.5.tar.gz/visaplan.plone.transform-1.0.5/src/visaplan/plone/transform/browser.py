# -*- coding: utf-8 -*- äöü
# Python compatibility:
from __future__ import absolute_import, print_function

import six
from six.moves import map, range

# Standard library:
# ------------------------------------- [ (alte) Methode 'regex' ... [
import re
from collections import Counter, defaultdict
from hashlib import md5
from time import time

# Plone:
from plone.memoize import ram

# 3rd party:
from bs4 import BeautifulSoup

# visaplan:
from visaplan.kitchen.spoons import (
    extract_content,
    parsed_text,
    split_paragraphs,
    stripped_soup,
    )
from visaplan.plone.base import BrowserView, Interface, implements
from visaplan.plone.infohubs import make_hubs
from visaplan.plone.tools.forms import dict_from_form, sorted_flaglist
from visaplan.tools.classes import RecursiveMap
from visaplan.tools.coding import safe_decode

# Local imports:
from .dispatcher import ID_FACTORY
from .kitchen import (
    CAPTION_PREFIX,
    TYPE2TEMPLATE,
    append_needed_scripts,
    check_uid_images,
    extract_uid,
    fix_bogus_markup,
    fix_bogus_markup2,
    fix_braces,
    fix_subs,
    inject_indexes,
    load_needed_scripts,
    make_id_factory,
    mark_uid_images,
    resolve_and_scale_images,
    resolve_uid_images,
    resolve_uid_links,
    sanitize_marginals,
    transform_booklinks,
    transform_files,
    transform_images,
    transform_links,
    transform_preprocess,
    transform_tables,
    )
from .utils import sanitize_html, shortened_copy

# Logging / Debugging:
from visaplan.plone.tools.log import getLogSupport
from visaplan.tools.debug import pp

# ------------------------------------- ] ... (alte) Methode 'regex' ]


LOGGER, debug_active, DEBUG = getLogSupport('transform')
del debug_active
ERROR = LOGGER.error
INFO = LOGGER.info

# Local imports:
from .config import DEBUG_ACTIVE, MAX_ITERATIONS

# Logging / Debugging:
from pdb import set_trace

# für settings-Browser:
KEY_REPLACE_IMAGES = 'replace-missing-images'


def cache_key(method, self, text):

    if self.context.getAdapter('devmode')():
        return (str(text), time())

    return str(text)

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

# -------------------------------------------------- [ Interface ... [
class ITransform(Interface):

    def get(self, text):
        """
        Transformation mit Hilfe von BeautifulSoup
        """

    # offenbar nicht mehr verwendet; Löschkandidat!
    def isFileImageVisible(self):
        """ """

    def get4Ajax(self, text):
        """
        Kopie der get-Methode für Texte, die per Ajax nachladbar sein sollen
        (aber nicht zwangsläufig so nachgeladen werden!)
        """

    def audit(self):
        """
        Zur Untersuchung und Behebung von Problemen im redaktionellen
        Seiteninhalt
        """
# -------------------------------------------------- ] ... Interface ]


# -------------------------------------- [ Debugging/Dekoratoren ... [
if DEBUG_ACTIVE:
    def call_and_result(f):
        def wrapper(self, *args, **kwargs):
            print('*** %s() ...' % f.__name__)
            soup1 = args[0]
            vorher = str(soup1)
            f(self, *args, **kwargs)
            nachher = str(soup1)
            if nachher == vorher:
                info('*** ... %s(): keine Aenderungen', f.__name__)
            else:
                info('*** ... %s(): text geaendert, %d Zeichen Laengenunterschied',
                     f.__name__,
                     len(nachher) - len(vorher),
                     )
        return wrapper

    def teller(name):
        def f(*args):
            print('+++ %s: %s' % (name, ', '.join(args)))
        return f

    def print_indented(txt):
        for line in txt.strip().split('\n'):
            print('    ' + line.rstrip())

    def report_replacement(method, soup_old, soup_new, dic=None):
        print()
        print('[ @@translate.%(method)s: Ersetze ... [' % locals())
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
        print('] ... @@translate.%(method)s ]' % locals())
        print()
else:
    def call_and_result(f):
        return f

    def teller(name):
        def f(*args, **kwargs):
            pass
        return f
# -------------------------------------- ] ... Debugging/Dekoratoren ]


# ---------------------------------------------------- [ Browser ... [
class Browser(BrowserView):

    implements(ITransform)

    #@ram.cache(cache_key)
    def get(self, text, tocs_enabled=False):
        """
        Transformation mit Hilfe von BeautifulSoup
        """
        context = self.context
        if text is None:
            ERROR('%(context)r: text is None', locals())
            return
        soup1 = BeautifulSoup(text, from_encoding='utf-8')
        hub, info = make_hubs(context)
        info['_remove_links'] = False
        em = False  # export mode; wenn Profil angegeben und gefunden
        if tocs_enabled:
            # Exportprofil übergeben?
            profile_id = info['request_var'].get('pid')
            if profile_id:
                try:
                    pid = int(profile_id)
                    dic = hub['export'].getRawProfile(pid)
                    if dic is not None:
                        info['_profile'] = dic
                        em = True
                except ValueError as e:
                    ERROR('invalid profile id (%(pid)r)!',
                          locals())
        if not em:
            info['_profile'] = None
        counter = Counter()

        if DEBUG_ACTIVE:
            print(soup1.prettify())

        # Reparaturen, wie Bereinigung vorwitziger HTML-Kommentare usw.:
        transform_preprocess(soup1, hub, info, counter)

        for i in range(MAX_ITERATIONS):
            done = True
            # siehe auch ...                                  ... Templates:
            if transform_tables(soup1, hub, info, counter):   # kss-table-view
                done = False

            if transform_images(soup1, hub, info, counter):   # kss-image-view
                done = False

            if transform_files(soup1, hub, info, counter):    # (js-unitracc*-view)
                done = False

            if transform_booklinks(soup1, hub, info, counter):# (keine)
                done = False

            if transform_links(soup1, hub, info, counter):    # (keine)
                done = False

            if done:
                break

        if em:  # export mode
            fix_bogus_markup(soup1, hub, info, counter)
            # vor der Generierung etwaiger Indexe zu erledigen:
            sanitize_marginals(soup1, hub, info, counter)
            fix_bogus_markup2(soup1, hub, info, counter)
            # nun die Indexe:
            inject_indexes(soup1, hub, info, counter)
            # hier ggf. auch Löschung externer Links (_remove_links):
            resolve_uid_links(soup1, hub, info, counter)
            # so ähnlich, aber für src-Attribute:
            resolve_and_scale_images(soup1, hub, info, counter)
            # für Videos, Formeln etc.:
            load_needed_scripts(soup1, hub, info, counter)
            # derzeit nötige Reparatur:
            fix_braces(soup1, hub, info, counter)
            fix_subs(soup1, hub, info, counter)
        else:
            resolve_uid_images(soup1, hub, info, counter)
            append_needed_scripts(soup1, hub, info, counter)

        is_single, elem_or_seq = extract_content(soup1)
        if is_single:
            text = six.text_type(elem_or_seq)
        else:
            text = u''.join(map(six.text_type, elem_or_seq))
        if em and text.startswith(u'html'):
            # Workaround, um Scheitern der PDF-Generierung zu vermeiden;
            # doctype ergänzen ('<!html>' --> HTML 5)
            text = sanitize_html(text, LOGGER)

        return text

    def get4Ajax(self, text):
        """
        Kopie der get-Methode für Texte, die per Ajax nachladbar sein sollen
        (aber nicht zwangsläufig so nachgeladen werden!)

        Unterschiede:
        - keinerlei Export-Funktionalitäten (wie Verzeichnisse etc.)
        - Ein etwaiger html.body-Rahmen wird entfernt
        - Benötigte Skripte werden hinten angefügt, z.B. für MathJax.

        Nota bene:
        - Es wird derzeit *nicht* garantiert, daß genau ein HTML-Element
          zurückgegeben wird.
        - Es wird angenommen, daß diese Methode (oder alternativ get) maximal
          einmal pro Seite aufgerufen wird; sprich: bei mehrmaligem Aufruf
          werden ggf. die benötigten Skripte mehrfach eingebunden.
        """
        context = self.context
        if text is None:
            ERROR('%(context)r: text is None', locals())
            return
        # soup1 = BeautifulSoup(text, from_encoding='utf-8')
        soup1 = BeautifulSoup(safe_decode(text))
        hub, info = make_hubs(context)
        info['_remove_links'] = False
        info['_profile'] = None
        counter = Counter()

        if DEBUG_ACTIVE:
            print(soup1.prettify())

        # Reparaturen, wie Bereinigung vorwitziger HTML-Kommentare usw.:
        transform_preprocess(soup1, hub, info, counter)

        for i in range(MAX_ITERATIONS):
            done = True
            # siehe auch ...                                  ... Templates:
            if transform_tables(soup1, hub, info, counter):   # kss-table-view
                done = False

            if transform_images(soup1, hub, info, counter):   # kss-image-view
                done = False

            if transform_files(soup1, hub, info, counter):    # (js-unitracc*-view)
                done = False

            if transform_booklinks(soup1, hub, info, counter):# (keine)
                done = False

            if transform_links(soup1, hub, info, counter):    # (keine)
                done = False

            if done:
                break

        resolve_uid_images(soup1, hub, info, counter)
        append_needed_scripts(soup1, hub, info, counter)

        return stripped_soup(soup1)  # ... get4Ajax

    def _getObject2Change(self, context):
        """
        Es genügt nicht, die ggf. zu ändernden Inhalte zu kennen -
        man muß auch wissen, wohin sie geschrieben werden sollen ...
        """
        # Code inspiriert von @@export._getRawContent
        pt = context.portal_type
        if pt != 'Folder':
            return context
        stage = self.context.getBrowser('stage')
        for brain in stage.getAsBrains('book-start-page', context.UID()):
            o = brain.getObject()
            if o.portal_type != 'Folder':
                return o

    def _get_image_uid_map(self):
        context = self.context
        portal = context.getAdapter('portal')()
        settings = portal.getBrowser('settings')
        return RecursiveMap(settings.get(KEY_REPLACE_IMAGES, {}))

    def _set_image_uid_map(self, dic):
        context = self.context
        portal = context.getAdapter('portal')()
        settings = portal.getBrowser('settings')
        return settings._set(KEY_REPLACE_IMAGES, dict(dic))

    def audit(self):
        """
        Zur Untersuchung und Behebung von Problemen im redaktionellen
        Seiteninhalt
        """
        # TODO:
        # - Sichern der Auswahl implementieren (9.7.2015: ???)
        # - Auditieren anderer Felder als text
        #   - gegenwärtig liefert die Methode isAuditable --> False
        #     für jeden Inhaltstyp, der dieses Feld nicht hat
        # - Prüfoptionen:
        #   - Ziffern in sup/sub-Elemente durch entsprechende Unicode-Zeichen
        #     ersetzen
        context = self.context
        portal = context.getAdapter('portal')()
        settings = portal.getBrowser('settings')
        obj = self._getObject2Change(context)
        getAdapter = context.getAdapter
        # set_trace()
        request = context.REQUEST
        hub, info = make_hubs(context)
        message = hub['message']
        if obj is None:
            ERROR('audit(%(context)r): No editable object found',
                  locals())
            message('No editable object found!',
                    'error')
            return request.RESPONSE.redirect('view')

        form = request.form
        pp(('Formulardaten:', dict(form)))
        # set_trace()
        grc = hub['export']._getRawContent
        available_actions = ('parse',
                             'missing_images',
                             'split_paragraphs',
                             )
        actions = sorted_flaglist(form.get('action', []),
                                  available_actions,
                                  ('parse',
                                   ))
        options = set([tup[0]
                       for tup in actions
                       if tup[1]
                       ]).difference(set(['parse']))
        res = {}
        res['actions'] = [{'name': tup[0],
                           'active': tup[1],
                           } for tup in actions
                           ]
        res['fields'] = []
        res['missing_images'] = {'tuples': [],
                                 'dicts': [],
                                 }
        missing_images = res['missing_images']['dicts']
        CLS_GOOD = 'border-blue'
        CLS_SUSPICIOUS = 'border-red'
        CLS_NEUTRAL = 'border-gray'
        choice = form.get('choice')
        given_field = form.get('field')

        substmap_changed = False
        substmap_changes = 0
        substmap_errors = 0
        if 'missing_images' in options:
            substmap = self._get_image_uid_map()
            substmap_additions = dict_from_form(form, 'replace')
            if substmap_additions:
                # irgendwelche Änderungen?
                for newk, newv in substmap_additions.items():
                    try:
                        if substmap[newk] == newv:
                            continue
                    except KeyError:
                        substmap_changes += 1
                substmap.update(substmap_additions)
                for k, v in substmap_additions.items():
                    v2 = substmap[k]
                    if v2 is None:
                        substmap_errors += 1
                        message("Can't replace UID %(k)s with %(v)s"
                                ' (deadlock!)' % locals(),
                                'error')
                pp(('substmap_additions:', substmap_additions))
                if not substmap_errors:
                    substmap_changed = True
            res['missing_images']['substmap'] = substmap
        else:
            substmap = {}

        # ------------------------------------- [ Codierung ... [
        # - Besser utf-8 annehmen als die unzuverlässige Ratefunktion zu
        #   nutzen!
        # - Ratefunktion nur verwenden, wenn explizit 'auto' gewählt.
        from_encoding = form.get('from_encoding')
        soupkw = {}
        if from_encoding:
            from_encoding = from_encoding.lower().strip()
        if not from_encoding:
            from_encoding = 'utf-8'
        elif from_encoding == 'auto':
            from_encoding = None
        if from_encoding is not None:
            soupkw.update({'from_encoding': from_encoding})
        # ------------------------------------- ] ... Codierung ]

        # ------------------ [ Schleife über Speicherfelder ... [
        for field in ['text']:
            keys = ['raw', 'html.parser']
            row = {'name': field,
                   'parsers': keys,
                   }
            parsed = {}
            print('objekt %(obj)r' % locals())
            raw = grc(obj, field, maxdepth=0)
            if raw is None:
                # ungetestet:
                message('Field ${field} not found!',
                        'error',
                        mapping=locals())
                continue
            raw = raw.strip()
            md5_hash = md5(raw).hexdigest()
            row['md5_hash'] = md5_hash
            parsed1 = parsed_text(raw, 'html.parser', **soupkw)
            parsed2 = parsed_text(raw, 'lxml', **soupkw)
            parsed = {# nicht wirklich geparst, aber trotzdem:
                      'raw': raw,
                      # den in jedem Fall:
                      'html.parser': parsed1,
                      }
            gimme_both = parsed1 != parsed2
            klass = {'raw': (not gimme_both and parsed1 == raw)
                            and CLS_GOOD or CLS_NEUTRAL,
                     'html.parser': CLS_GOOD,
                     }
            if gimme_both:
                keys.append('lxml')
                parsed['lxml'] = parsed2
                if len(parsed2) < len(parsed1):
                    klass.update({
                        'html.parser': CLS_GOOD,
                        'lxml': CLS_SUSPICIOUS,
                        })
                else:
                    klass.update({
                        'html.parser': CLS_SUSPICIOUS,
                        'lxml': CLS_GOOD,
                        })
            # ------------- [ immer soup-dict erzeugen ... [
            soups = []
            soup = {}
            for key in keys:
                # hier immer lxml verwenden ...
                # print 'key=%(key)s, soupkw=%(soupkw)s ...' % locals()
                soup[key] = BeautifulSoup(parsed[key], **soupkw)
                if not from_encoding:
                    from_encoding = soup[key].original_encoding
                soups.append(soup[key])
            hub[ID_FACTORY] = make_id_factory(*soups)
            del soups
            # ------------- ] ... immer soup-dict erzeugen ]
            # ----- [ immer Piktogrammfehler ermitteln ... [
            missing_images_found = \
                    mark_uid_images(soup['raw'], hub, info)
            # ----- ] ... immer Piktogrammfehler ermitteln ]

            # ----------- [ Optionale Transformationen ... [
            # ------------- [ Fehlende Piktogramme ... [
            if 'missing_images' in options:
                info['uid-substmap'] = substmap
                done = set()
                done_ids = defaultdict(list)
                for key in keys:
                    if key != 'raw':
                        # Bilder ohne bekannten Ersatz generieren:
                        for tup in check_uid_images(soup[key],
                                                    hub, info):
                            id, uid, tail = tup
                            tup1 = (uid, tail)
                            done_ids[tup1].append(id)
                            if tup1 in done:
                                continue
                            done.add(tup1)
                            INFO('missing image: %(ign)s', locals())
                            dic = {'uid': uid,
                                   'tail': tail,
                                   'replace-by': substmap.get(uid),
                                   }

                            pp((('missing_images:', missing_images),
                                ('tup1:', tup1),
                                ))
                            # Reihenfolge erhalten:
                            missing_images.append(dic)
                            pp(('missing_images +=', dic))
                for dic in missing_images:
                    tup1 = dic['uid'], dic['tail']
                    dic['ids'] = ' '.join(done_ids[tup1])
                if 0:\
                res['missing_images']['dicts'].extend([
                    {'uid': tup[0],
                     'tail': tup[1],
                     } for tup in missing_images
                    ])
                res['missing_images']['choices'] = sorted(substmap.values())
            elif missing_images_found:
                message('$(missing_images_found) missing images to fix!',
                        'error',
                        mapping=locals())
            # ------------- ] ... Fehlende Piktogramme ]

            # ----------- [ Leerzeilen zu Absätzen ... [
            if 'split_paragraphs' in options:
                for key in keys:
                    if key != 'raw':
                        root = soup[key]  # die ganze Suppe durchsuchen
                        split_paragraphs(root, soup[key])
            # ----------- ] ... Leerzeilen zu Absätzen ]
            # ----------- ] ... Optionale Transformationen ]

            transformed = {}
            for key in keys:
                if key == 'raw':
                    # parsed['raw'] wurde nicht aktualisiert -
                    # aber möglicherweise die Suppe gewürzt:
                    txt = stripped_soup(soup[key])
                    transformed[key] = self.get(txt)
                else:
                    parsed[key] = stripped_soup(soup[key])
                    transformed[key] = self.get(parsed[key])

            # ---------------- [ Auswahl zum Speichern ... [
            usable = set(keys)
            usable.difference_update(set(['raw']))
            if choice:
                if given_field != field:
                    continue
                # set_trace()
                message = hub['message']
                and_then = 'code-audit'
                if choice in usable:
                    # pp(dict(form))
                    given_md5 = form.pop('md5', None)
                    # pp(dict(form))
                    if given_md5 == md5_hash:
                        dic = {field: parsed[choice],
                               }
                        # set_trace()
                        obj.processForm(values=dic)
                        message('Changes saved')
                        tmp = form.get('next')
                        if tmp in ('code-audit', 'edit', 'view'):
                            and_then = tmp
                    elif given_md5:
                        message('Object was changed meanwhile; '
                                'please repeat!',
                                'error')
                    if 'missing_images' in options:
                        if substmap_errors:
                            message("Couldn't change substitution map!",
                                    'error')
                        elif substmap_additions:
                            self._set_image_uid_map(substmap)
                            message('Substitution map updated.')
                else:
                    message('Sorry - invalid choice; please try again!',
                            'error')
                return request.RESPONSE.redirect(and_then)
            # ---------------- ] ... Auswahl zum Speichern ]

            equal = (parsed1 == raw.strip()
                     and not gimme_both
                     )
            show_form = (not equal
                         or ('missing_images' in options
                             and missing_images_found
                             )
                         )
            row.update({
                'parsers': keys,
                'parsed': parsed,
                'transformed': transformed,
                'klass': klass,
                'equal': equal,
                'show-form': show_form,
                })
            res['fields'].append(row)
        # ------------------ ] ... Schleife über Speicherfelder ]
        pp((u'Komplette Daten (gekuerzt):',
            shortened_copy(res, ['parsed', 'transformed']),
            ))

        res['from_encoding'] = from_encoding
        return res

# ------------------------------------- [ (alte) Methode 'regex' ... [

    # offenbar nicht mehr verwendet; Löschkandidat!
    def isFileImageVisible(self):
        """
        TH: mutmaßlich obsolet
        """
        context = self.context
        if context.getContentType() == 'application/x-shockwave-flash':
            return True

    # offenbar nicht mehr verwendet; Löschkandidat!
    def formatNumber(self, structureNumber, counter):
        """
        Entsprechende neue Funktion: kitchen.make_caption_prefix
        """
        if not structureNumber and not counter:
            return ':&nbsp;'

        return '%s - %s:&nbsp;' % (structureNumber, counter)

    # Doctests: siehe ./oldfuncs.py
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
# ---------------------------------------------------- ] ... Browser ]
