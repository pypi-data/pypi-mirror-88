# -*- coding: utf-8 -*- vim: ts=8 sts=4 sw=4 si et tw=72
"""\
dispatcher.py - Objekte auf Verzeichnisse verteilen
"""

# Python compatibility:
from __future__ import absolute_import, print_function

# Standard library:
from collections import defaultdict

# 3rd party:
from bs4 import BeautifulSoup

# visaplan:
from visaplan.kitchen.forks import (
    appendix_dots,
    extract_linktext,
    inject_number,
    )
from visaplan.kitchen.ids import sibling_id
from visaplan.kitchen.spoons import (
    add_class,
    clone,
    extract_uid,
    find_headline,
    fix_class_arg,
    get_id_or_name,
    has_any_class,
    has_class,
    hyperlinkable_strings,
    make_tag,
    parent_chapters,
    parse_selector,
    )
from visaplan.tools.classes import Proxy, WriteProtected
from visaplan.tools.html import entity

# Local imports:
from .sniff import (
    contains_questions_list,
    is_cooked_animation,
    is_cooked_formula,
    is_cooked_glossary,
    is_cooked_image,
    is_cooked_literature,
    is_cooked_media,
    is_cooked_standard,
    is_cooked_table,
    is_cooked_video,
    is_question,
    is_questions_list,
    )

# Logging / Debugging:
# Logging/Debugging:
import logging

LOGGER = logging.getLogger('unitracc@@transform:kitchen')
ERROR = LOGGER.error
# Logging / Debugging:
from pdb import set_trace
from visaplan.tools.debug import asciibox, pp

DEBUG = defaultdict(lambda: 0)

__all__ = (# der Verteiler:
           'DirectoryDispatcher',
           # sonstige Funktionen:
           'make_headline_element',
           'make_toc_entry',
           # Symbolische Namen für hub-Objekt:
           'APPENDIX_DISPATCHER',
           'ID_FACTORY',
           # Listenklassen:
           'RawDirectory',
           'SortingDirectory',
           'GroupingDirectory',
           'Glossary',
           'SolutionsDirectory',
           'ExerciseDirectory',
           'Index',
           'NullDirectory',
           # sonstige Daten:
           'CHECKED_TOPICS',
           )

# ------------------------------------------------------ [ Daten ... [
# Namen, die im Hub ansonsten nicht vorkommen können:
APPENDIX_DISPATCHER = intern('Appendix dispatcher')
ID_FACTORY = intern('ID factory')

# Reihenfolge, in der die HTML-Knoten auf ihren Typ überprüft werden
# FIXME: in dieser Reihenfolge werden derzeit auch die Indexe erzeugt;
#        es soll aber die Reihenfolge aus dem Exportprofil verw. werden!
CHECKED_TOPICS = (# vorziehen:
                  'exercises',  # Frageliste (W3L-Importe)
                  # Objekttypen ...
                  'formulas',  # manche Formeln liegen als Bilder vor
                  'animations',
                  'videos',
                  'tables',
                  # alle vorstehenden sind manchmal Bilder ...
                  'images',
                  # "Lumpensammler" für nicht speziell gelistete:
                  'media',
                  # keine "Medien":
                  'standards',
                  'literature',  # umfaßt ggf. auch Normen ("standards")
                  'glossary',
                  # und nun zu etwas völlig anderem:
                  'solutions',  # frei gesammelte Fragen
                  # nachgelagert:
                  'index',
                  )
DETECTOR = {'formulas':   is_cooked_formula,
            'animations': is_cooked_animation,
            'videos':     is_cooked_video,
            'tables':     is_cooked_table,
            'images':     is_cooked_image,
            'media':      is_cooked_media,
            'standards':  is_cooked_standard,
            'literature': is_cooked_literature,
            'glossary':   is_cooked_glossary,
            'exercises':  is_questions_list,
            'solutions':  is_question,
            }
SOFT_HYPHEN = entity['shy']
# ------------------------------------------------------ ] ... Daten ]


# ------------------------------------------- [ Objekte erkennen ... [
## --> sniff-Modul

def index_this(elem):
    """
    Vorläufig; wird mutmaßlich überführt in eine Methode der
    Index-Klasse, sobald der Index konfigurierbar wird
    """
    return is_cooked_glossary(elem)
DETECTOR['index'] = index_this
# ------------------------------------------- ] ... Objekte erkennen ]


# ---------------------------------------------- [ Listenklassen ... [
class RawDirectory(object):
    """
    Zur Erstellung eines Verzeichnisses
    """
    def __init__(self, spec, dispatcher):
        """
        spec -- ein SourceSpec-Dictionary
                (Schlüssel: objects, sorting, ifempty)
        """
        self._spec = spec
        self._objects = spec['objects']
        self._sortable_list = []
        self._dispatcher = dispatcher
        # je nach Verzeichnisklasse überladen:
        self._init_counter()

    def _init_counter(self):
        self._counter = 0

    def make_key(self, item, chapter):
        """
        simpler Zähler (Reihenfolge des Vorkommens);
        item und chapter werden nicht verwendet.

        Insbesondere für abgeleitete Klassen ist der Sortierschlüssel
        allerdings auch die Möglichkeit, Informationen zu speichern, die
        dann bei der schlußendlichen Generierung der Einträge verwendet
        werden.
        """
        self._counter += 1
        return self._counter

    def append(self, item, chapter):
        """
        item -- ein Knoten im HTML-Baum
        chapter -- ein Tupel von int-Werten (für etwaige Gruppierung)
        """
        self._sortable_list.append((self.make_key(item, chapter),
                                    item,
                                    ))

    def __nonzero__(self):
        """
        Das Verzeichnis ist "True", wenn es Einträge enthält
        """
        return bool(self._sortable_list)

    def elem(self):
        """
        Gib das einzufügende Wurzelelement zurück, oder None.
        """
        ifempty = self._spec['ifempty']
        if ifempty == 'off':
            return None
        if not self._sortable_list:
            if ifempty == 'auto':
                return None
        # TODO: spezielle Behandlung für erzwungene leere Verzeichnisse
        soup = self._dispatcher._soup
        thedir = self.create_root(soup)
        self._sortable_list.sort()
        self.append_entries(thedir, soup)
        return self._root

    def append_entries(self, thedir, soup):
        """
        Lies die sortierte Liste aus und füge die Einträge dem
        Wurzelelement hinzu.
        """
        for key, elem in self._sortable_list:
            entry = self.create_entry(soup, key, elem)
            if entry is not None:
                thedir.append(entry)
                if has_class(entry, 'unwrap-me'):
                    entry.unwrap()

    def headline_text(self):
        """
        Der Text der Überschrift
        """
        mogrify = self._dispatcher._hub['translate']
        return mogrify('Index of %(objects)s' % self._spec)

    def container_classnames(self):
        """
        Erzeuge eine oder mehrere CSS-Klassen für den Container,
        um passende Formatierung zu ermöglichen
        """
        return ['index-of-%(objects)s' % self._spec,
                'index-type-%s' % self.__class__.__name__,
                ]

    def create_root(self, soup):
        """
        Erzeuge einen Container, der als erstes Element die Überschrift
        enthält; die anderen werden dann angefügt
        """
        kwargs = {'class': self.container_classnames(),
                  }
        self._root = thedir = soup.new_tag('div', **kwargs)
        txt = self.headline_text()
        hN = self._dispatcher._subappendix_el
        headline = make_tag(soup, hN, txt)
        thedir.append(headline)
        return thedir

    def default_linktext(self, elem, key=None):
        """
        Wird verwendet, wenn die bevorzugte Methode zur Ermittlung des
        Link-Texts keinen Erfolg zeitigt
        """
        text = elem.string
        nfo = 1
        if text:
            text = text.strip()
            if text:
                return text
            text = 'sorry; text is empty!'
            nfo += 1
        else:
            text = 'sorry, no text!'
        return text

    def extract_linktext(self, elem, key=None):
        """
        Extrahiere den Link-Text
        """
        func = 0 and self.default_linktext or None
        return extract_linktext(elem,
                                key,
                                func)

    def default_id_prefix(self):
        """
        Für den id-Generator: gib das Präfix für ein id-Attribut zurück.

        Üblicherweise für das übergebene Element (aus dem Text), nicht
        für das dazugehörige Verzeichniselement verwendet.
        """
        return 'item'

    def extract_id(self, elem, prefix=None):
        """
        Extrahiere die vorhandene ID, oder füge eine neue hinzu
        """
        theid = elem.get('id')
        if theid is not None:
            return theid
        if not prefix:
            prefix = self.default_id_prefix()
        theid = self._dispatcher._hub[ID_FACTORY](prefix)
        elem['id'] = theid
        return theid

    def create_entry(self, soup, key, elem):
        """
        key -- der Sortierschlüssel (unterschiedlich je nach
               Verzeichnisklasse, und nicht unbedingt verwendet)
        elem -- das Verweisziel
        """
        if DEBUG[elem.name]:
            set_trace()
        text = self.extract_linktext(elem, key)
        if text:
            wrapper = soup.new_tag('div')
            theid = self.extract_id(elem)
            wrapper.append(make_tag(soup, 'a', text,
                                    href='#'+theid
                                    ))
            return wrapper


class GroupingDirectory(RawDirectory):
    """
    Gruppiert nach Kapiteln
    """

    def _init_counter(self):
        self._counter = defaultdict(int)

    def make_key(self, item, chapter):
        """
        Verwendet nur chapter: fortlaufend je Kapitel
        """
        self._counter[chapter] += 1
        return (chapter, self._counter[chapter])


class SortingDirectory(RawDirectory):
    """
    Sortiert nach Titel
    """

    def make_key(self, item, chapter):
        """
        Verwendet nur item; ansonsten fortlaufend
        """
        self._counter += 1
        return (item.string.strip(), self._counter)


class Glossary(RawDirectory):
    """
    Sortiert nach dem Inhalt; das title-Attribut enthält den jeweiligen
    Erläuterungstext.  Dieser Erklärungstext wird im Glossar ausgegeben
    (und keine Seitennummer; dann wäre es ein Stichwortverzeichnis).

    Es werden Hyperlinks aus dem Text in das Glossar erzeugt, und vom
    Glossar zurück in den Text.

    Es ist möglich, daß derselbe Glossareintrag im selben Dokument
    mehrmals angesprochen wird.  Der Hyperlink im Glossar führt zurück
    zu der Stelle der *ersten* Verwendung.

    Technisch dasselbe wie ein Glossar sind das Literatur- und das
    Normenverzeichnis.
    """

    def __init__(self, spec, dispatcher):
        super(Glossary, self).__init__(spec, dispatcher)
        # schon verwendete Glossareinträge merken:
        self._glossary_id = {}

    def headline_text(self):
        """
        Der Text der Überschrift
        """
        _ = mogrify = self._dispatcher._hub['translate']
        if self._objects == 'glossary':
            return _('Glossary')
        return mogrify('Index of %(objects)s' % self._spec)

    def default_id_prefix(self):
        return 'topic'

    def make_key(self, item, chapter):
        """
        Sammle die Informationen; sie werden auch zur schlußendlichen
        Generierung der Glossareinträge direkt verwendet.

        Es wird ein 6-Tupel zurückgegeben:
        (lower_topic, cnt, topic, description, entry_id, firstuse_id)

        cnt -- der Zähler, wie von RawDirectory.make_key erzeugt;
               fungiert als Indikator, ob ein *neues* Schlagwort
               vorliegt, und stellt sicher, daß gleichlautende
               Schlagwörter in der Reihenfolge des Auftretens
               aufgelistet werden
        topic -- das Schlagwort (der Inhalt des übergeb. Elements)
        description -- der Beschreibungstext
        entry_id -- das id-Attribut des Glossareintrags; Präfix: "topic"
        firstuse_id -- das id-Attribut des Elements der ersten
                       Verwendung des Glossareintrags (normalerweise des
                       hier übergebenen).  Wenn das übergebene Element
                       das erste verwendende ist und noch kein
                       id-Attribut hat, wird es mit dem Präfix "ref"
                       erzeugt.

        <chapter> wird hier ignoriert.
        """
        def _key(lower_topic=None, cnt=None,
                 topic=None, description=None,
                 entry_id=None, firstuse_id=None):
            if lower_topic is None and topic is not None:
                lower_topic = topic.lower()
            return (lower_topic, cnt,    # für Sortierung
                    topic, description,  # ff: für Generierung
                    entry_id, firstuse_id,
                    )
        attributes = item.attrs
        url = attributes.get('href')
        if not url:
            return _key()
        description = attributes.get('title')
        if not description:
            return _key()
        uid = extract_uid(url)
        if not uid:
            return _key()
        entry_id = self._glossary_id.get(uid)
        if entry_id is None:
            # noch nicht vorhanden; Glossareintrag erzeugen:
            topic = self.extract_linktext(item)
            make_id = self._dispatcher._hub[ID_FACTORY]
            entry_id = make_id('topic')
            self._glossary_id[uid] = entry_id
            firstuse_id = self.extract_id(item, 'ref')
            return _key(topic=topic,
                        cnt=RawDirectory.make_key(self, item, chapter),
                        description=description,
                        entry_id=entry_id,
                        firstuse_id=firstuse_id)
        topic = self.extract_linktext(item, None)
        return _key(topic=topic,
                    description=description,
                    entry_id=entry_id)

    def append(self, item, chapter):
        """
        Füge einen Glossareintrag für das übergebene Element hinzu,
        sofern noch nicht vorhanden.

        Wandle jedenfalls den resolveUid-Link in einen lokalen Link (zum
        Glossareintrag) um und entferne das onclick-Attribut.
        """
        (lower_topic, cnt, topic, description,
         entry_id, firstuse_id,
         ) = key_tuple = self.make_key(item, chapter)
        if cnt is not None:
            self._sortable_list.append((key_tuple, item))
        if entry_id is not None:
            # Neuer oder vorhandener Glossareintrag:
            attributes = item.attrs
            if 'onclick' in attributes:
                del attributes['onclick']
            attributes['href'] = '#' + entry_id

    def create_entry(self, soup, key, elem):
        """
        key -- der Sortierschlüssel (enthält alles, was wir brauchen)
        elem -- das Verweisziel (hier nicht benötigt)

        Im Falle eines Glossars wird eine Definitionsliste erzeugt und
        damit *zwei* Elemente pro Eintrag!
        """
        raise NotImplementedError

    def append_entries(self, thedir, soup):
        """
        Lies die sortierte Liste aus und füge die Einträge dem
        Wurzelelement hinzu.

        Im Falle eines Glossars wird eine Definitionsliste erzeugt und
        damit *zwei* Elemente pro Eintrag!
        """
        if not self._sortable_list:
            return
        thelist = soup.new_tag('dl')
        thedir.append(thelist)
        for key_tuple, elem in self._sortable_list:
            (lower_topic, cnt,
             topic, description,
             entry_id, firstuse_id,
             ) = key_tuple
            if not topic and False:
                pp((('key_tuple:', key_tuple),
                    ('elem:', elem.prettify()),
                    ))
            dt = soup.new_tag('dt', id=entry_id)
            dt.append(make_tag(soup, 'a', topic,
                               href='#'+firstuse_id))
            thelist.append(dt)
            if '<' in description:
                dd = BeautifulSoup(description.join(('<dd>',
                                                    '</dd>',
                                                    ))).dd
                thelist.append(dd)
            else:
                dd = make_tag(soup, 'dd', description)
                dd.string = description
            thelist.append(dd)


def disembowel_question(elem, soup):
    """
    Weide das übergebene Frageelement aus: Alle Inhalte, die in der
    Druckausgabe nicht bei der Frage stehen sollen, werden entfernt.

    Rückgabewert ist eine Liste von Elementen, die für den Lösungsteil
    verwendet werden sollen.

    elem - das "auszuweidende" Element
    soup - nur verwendet, um (Container-) Elemente erzeugen zu können
    """
    res = []
    # erst die Antworten (nur die korrekte):
    answer_elements = elem.find_all(class_='question-answer-right')
    answers = []
    for answer in answer_elements:
        dings = clone(answer)
        input = dings.input
        if input:
            input.decompose()
        icon = dings.find(class_='question-answer-icon')
        if icon:
            icon.decompose()
        contents = dings.contents
        if len(contents) == 1 and contents[0].name == 'label':
            dings.label.unwrap()
        answers.append(dings)

    if answers:
        ansdiv = soup.new_tag('div',
                              **{'class': 'question-answers',
                                 })
        for answer in answers:
            ansdiv.append(answer)
        res.append(ansdiv)

    # dann die Erläuterungstexte:
    solution_elements = elem.find_all(class_='question-hint-appendix')
    if not solution_elements:
        solution_elements = elem.find_all(class_='question-hint-any')
    for sol in solution_elements:
        res.append(sol.extract())
    # übrig bleiben die Hinweise für interaktive Bearbeitung;
    # sie werden gelöscht (auch, wenn dann keine mehr übrigbleiben):
    for hint in elem.find_all(True):
        if has_any_class(hint, ['question-hints'],
                         'question-hint-'):
            hint.decompose()
    return res


class SolutionsDirectory(RawDirectory):
    """
    Verarbeitet question-Elemente:
    - Beläßt die Frage an ihrem Ort, und
    - entfernt alle Lösungstexte; dabei werden ...
    - die dafür geeigneten Lösungstexte für den Anhang verwendet.

    Erinnert im Ergebnis an ein Glossar; es gibt aber folgende
    bedeutsame Unterschiede:
    - Es findet keine Sortierung statt.
    - Gleichlautende Lösungen für unterschiedliche Fragen werden
      natürlich nicht zusammengefaßt.
    """

    def create_entry(self, soup, key, elem):
        """
        key -- der Sortierschlüssel (unterschiedlich je nach
               Verzeichnisklasse, und nicht unbedingt verwendet)
        elem -- das Verweisziel

        Da pro Übungsaufgabe zwei Elemente zu erzeugen sind - das
        dt-Element, das den Hyperlink zurück zur Frage enthält, und das
        dd-Element mit der Lösung - werden beide temporär in ein div mit
        der Klasse "unwrap-me" verpackt und nach dem Anhängen wieder
        ausgepackt.
        """
        hub = self._dispatcher._hub
        make_id = hub[ID_FACTORY]

        # IDs von Fragen und Lösungen sollen möglichst dasselbe
        # numerische Suffix haben (question-42 <--> solution-42).
        # *Alle* Fragen erhalten eine ID - auch die, für die wir keine
        # Lösung finden können:
        solution_id = sibling_id(elem, 'question', 'solution', make_id)

        ham = disembowel_question(elem, soup)
        if not ham:
            return None

        # Die Funktion sibling_id hat eine etwa noch fehlende ID
        # ergänzt:
        question_id = elem.attrs['id']
        to_solution = soup.new_tag('a',
                                   **{'class': 'to-solution',
                                      'href': '#'+solution_id,
                                      })
        # Das könnte z. B. ein Glühbirnen-Piktogramm sein:
        _ = hub['translate']
        to_solution.append(soup.new_tag('img',
                                        src='/to-solution.png',
                                        alt=_('Solution')))
        elem.append(to_solution)

        container = soup.new_tag('div',
                                 **{'class': 'unwrap-me'})
        dt = soup.new_tag('dt', id=solution_id)
        dt.append(make_tag(soup, 'a',
                           '%s.' % (key,),
                           **{'class': 'to-question',
                              'href': '#'+question_id,
                              }))
        container.append(dt)

        dd = soup.new_tag('dd')
        for chunk in ham:
            dd.append(chunk)
        container.append(dd)

        return container

    def create_root(self, soup):
        """
        Erzeuge das Wurzelelement und gib das Element zurück, dem die
        Einträge angefügt werden.
        """
        thedir = RawDirectory.create_root(self, soup)
        thelist = soup.new_tag('dl')
        thedir.append(thelist)
        return thelist


class ExerciseDirectory(RawDirectory):
    """
    Übungsaufgaben liegen im W3L-System als Übungslisten vor (ueblist),
    die als "ordered lists" mit der Klasse "questions" importiert werden.
    Jede ol.questions ist technisch ein eigener Verzeichniseintrag, der
    allerdings viele Unterelemente mit jeweils eigenen IDs enthält.
    """

    def create_entry(self, soup, key, elem):
        hub = self._dispatcher._hub
        make_id = hub[ID_FACTORY]
        sink_id = sibling_id(elem, 'exercise', 'solutions', make_id)
        well_id = elem.attrs['id']
        sink_nr = sink_id.split('-')[-1]
        sink_elem = soup.new_tag('div', id=sink_id)

        get_level = self._dispatcher._info['get_level']
        def is_headline(elem):
            try:
                get_level(elem)
            except ValueError:
                return False
            else:
                return True

        # set_trace()
        headline_id = None
        well_hN = find_headline(elem, is_headline)
        if well_hN is not None:
            headline_id = well_hN.attrs.get('id')
            h4 = soup.new_tag('h4')
            textel = well_hN.find(class_='headline-text')
            backlink = None
            try:
                if textel and textel.string.strip():
                    backlink = clone(textel)
            except (TypeError, AttributeError):
                pass
            if backlink is None:
                backlink = clone(well_hN)
            if backlink.attrs.get('id') is not None:
                del backlink.attrs['id']
            if headline_id is not None:
                backlink.name = 'a'
                backlink.attrs['href'] = '#'+headline_id
            else:
                backlink.name = 'span'
            h4.append(backlink)
            sink_elem.append(h4)

        sol = soup.new_tag('ol',  # sol -> "sink ol"
                           **{'class': 'questions'})
        sink_elem.append(sol)
        qid_prefix = '-'.join(('question', sink_nr))
        sid_prefix = '-'.join(('solution', sink_nr))
        for li in elem.contents:
            if li.name is None and not li.string.strip():
                continue
            assert li.name == 'li', \
                    'Listenelement erwartet! (%s)' % (li,)
            sol_id = sibling_id(li, qid_prefix, sid_prefix, make_id)
            ham = disembowel_question(li, soup)
            if ham:
                sol_href = '#' + sol_id
                qst_href = '#' + li.attrs['id']
                sli = soup.new_tag('li', id=sol_id)
                for chunk in ham:
                    sli.append(chunk)
                for txt in hyperlinkable_strings(li):
                    txt.wrap(soup.new_tag('a', href=sol_href))
                for txt in hyperlinkable_strings(sli):
                    txt.wrap(soup.new_tag('a', href=qst_href))
                sol.append(sli)
        # nochmal ein Backlink, diesmal für die gedruckte Darstellung:
        _ = self._dispatcher._hub['translate']

        # Workaround; Hyperlink zu ol-Element klappt nicht:
        if headline_id is not None:
            well_id = headline_id

        sink_elem.append(make_page_link(soup,
                                        _('For exercises see p. '),
                                        well_id))
        LOGGER.info('Link zur Quelle, ID: %s', well_id)
        # ... und im Druck auf die Lösungen verweisen:
        elem.append(make_page_link(soup,
                                   _('For solutions see p. '),
                                   sink_id))
        LOGGER.info('Link zur Senke, ID: %s', sink_id)
        # Die Liste der Lösungen:
        return sink_elem

    def append_entries(self, thedir, soup):
        """
        Sonderfall W3L-Lösungsverzeichnisse:
        Wenn es nur eins gibt (der Regelfall), werden die zusätzlichen
        Überschriften im Anhang nicht benötigt.

        Die Überschrift im Text (und damit auch im Inhaltsverzeichnis)
        läßt sich unterdrücken, indem man das entsprechende Objekt
        genauso benennt wie das Elternobjekt; aufeinanderfolgende
        gleiche Überschriften werden standardmäßig entfernt.
        """
        super(ExerciseDirectory, self).append_entries(thedir, soup)
        h4_list = thedir.find_all('h4')
        if len(h4_list) == 1:
            h4_list[0].extract()


class Index(RawDirectory):
    """
    Index: ein nachgelagert zu erstellendes Verzeichnis, das Elemente
    enthalten kann, die schon in einem der spezielleren Verzeichnisse
    aufgelistet werden.

    Vorerst enthält der Index hartcodiert dieselben Einträge wie ein
    etwaiges Glossar.
    """

    def __init__(self, spec, dispatcher):
        super(Index, self).__init__(spec, dispatcher)
        self._thedict = defaultdict(list)

    def make_key(self, item, chapter):
        """
        simpler Zähler (Reihenfolge des Vorkommens);
        item und chapter werden nicht verwendet.

        Insbesondere für abgeleitete Klassen ist der Sortierschlüssel
        allerdings auch die Möglichkeit, Informationen zu speichern, die
        dann bei der schlußendlichen Generierung der Einträge verwendet
        werden.
        """
        txt = self.extract_linktext(item)
        if txt is None:
            ERROR('Index.make_key: No text from %s', item)
            return
        txt = txt.replace(SOFT_HYPHEN, '')
        return txt.capitalize(), txt

    def create_root(self, soup):
        """
        Erzeuge das Wurzelelement und gib das Element zurück, dem die
        Einträge angefügt werden.
        """
        thedir = RawDirectory.create_root(self, soup)
        thelist = make_tag(soup, 'div', class_='index-content')
        thedir.append(thelist)
        return thelist

    def append_entries(self, thedir, soup):
        """
        Lies die sortierte Liste aus und füge die Einträge dem
        Wurzelelement hinzu.

        Im Falle eines Glossars wird eine Definitionsliste erzeugt und
        damit *zwei* Elemente pro Eintrag!
        """
        thedict = defaultdict(list)
        for keytup, item in self._sortable_list:
            thedict[keytup].append(item)

        sorted_keytups = sorted(thedict.keys())
        self._sorted_list = []
        for keytup in sorted_keytups:
            self._sorted_list.append((keytup, thedict[keytup]))

        if self._spec['sorting'] == 'grouped':
            return self.append_entries_grouped(thedir, soup)

        for keytup, hits in self._sorted_list:
            Cap, text = keytup
            thedir.append(self.topic_elem(text, hits, soup))

    def append_entries_grouped(self, thedir, soup):
        """
        Wie append_entries, aber nach Anfangsbuchstaben gruppiert
        """
        group = None
        prev_prefix = None
        for keytup, hits in self._sorted_list:
            Cap, text = keytup
            curr_prefix = Cap[0]
            if curr_prefix != prev_prefix:
                prev_prefix = curr_prefix
                group = make_tag(soup, 'div', class_='index-group')
                group.append(make_tag(soup, 'div',
                                      curr_prefix,
                                      class_='group-prefix'))
                thedir.append(group)
            group.append(self.topic_elem(text, hits, soup))

    def topic_elem(self, text, hits, soup):
        """
        Erzeuge einen Index-Eintrag
        """
        entry = soup.new_tag('div', **{'class': 'index-topic'})
        entry.append(make_tag(soup, 'span', text))
        ul = soup.new_tag('ul')
        entry.append(ul)
        make_id = None
        for src_elem in hits:
            id = src_elem.attrs.get('id')
            if id is None:
                if make_id is None:
                    make_id = self._dispatcher._hub[ID_FACTORY]
                id = make_id('topic')
                src_elem.attrs['id'] = id
            li = soup.new_tag('li')
            span = soup.new_tag('span')
            li.append(span)
            span.append(make_tag(soup, 'a',
                                 href='#'+id))
            ul.append(li)
        return entry


class NullDirectory(RawDirectory):
    """
    Läßt alles ohne Umschweife in der Versenkung verschwinden.
    """

    def _init_counter(self):
        pass

    def append(self, *args, **kwargs):
        pass

    def elem(self):
        return None

LISTCLASS = {# je nach spec['sorting']:
        'plain':   RawDirectory,
        'sorted':  SortingDirectory,
        'grouped': GroupingDirectory,
        }
# ---------------------------------------------- ] ... Listenklassen ]


# --------------------------------- [ Klasse DirectoryDispatcher ... [
class DirectoryDispatcher(object):
    """
    Organisiert die Verteilung von Objekten auf Verzeichnisse.
    """

    def __init__(self, soup, info, hub):
        """
        soup -- der HTML-Baum, aus dem die Verzeichniseinträge stammen,
                und in den die Verzeichnisse eingefügt werden sollen
        info -- enthält die Einträge 'tocs' (Verzeichnisse) und
                'appendixes' (Anhänge).  Derzeit dürfen diese beiden
                Listen jeweils nur eine Spezifikation enthalten; eine
                Anhangs-Spezifikation kann dabei aber durchaus mehrere
                Listen enthalten (z.B. Bilder, Formeln, Tabellen ...)
        hub -- zum Zugriff auf Browser und Adapter aus dem Kontext;
               insbesondere auf den translate-Adapter
        """
        self._soup = soup
        self._info = info
        self._hub = hub
        self._detectors = []       # (name, detector, verzeichnis)-Tupel
        self._detectors_primary = []
        self._detectors_postponed = []
        self._sortings = set()
        self._chapters_nodes = WriteProtected()
        self._chapters_tuples = WriteProtected()
        self._subappendix_el = None
        self._index = None

        target = WriteProtected()  # was landet wo?

        # siehe .tocspecs.evaluateAppendixDefinition:
        first = True
        for apdx in info['appendixes']:
            if first:
                for spec in apdx['inputlist']:
                    name = spec['objects']
                    if spec['ifempty'] == 'off':
                        liz = NullDirectory(spec, self)
                    elif name in ('glossary',
                                  'literature',
                                  'standards',
                                  ):
                        # Spezialfall Glossar: Sortierung steht fest
                        liz = Glossary(spec, self)
                        self._sortings.add(name)
                    elif name in ('solutions',
                                  ):
                        if contains_questions_list(soup):
                            name = 'exercises'
                            spec['objects'] = name
                            liz = ExerciseDirectory(spec, self)
                        else:
                            liz = SolutionsDirectory(spec, self)
                        self._sortings.add(name)
                    elif name == 'index':
                        # Spezialfall Sachindex: kombinierbar
                        liz = Index(spec, self)
                        self._index = liz
                        self._sortings.add(name)
                    else:
                        sorting = spec['sorting']
                        liz = LISTCLASS[sorting](spec, self)
                        self._sortings.add(sorting)
                    target[name] = liz

                if apdx['headline_text'] is None:
                    self._subappendix_el = 'h2'
                    # TODO: Vorkehrung für Numerierung von
                    #       h4-Überschriften im Anhang
                else:
                    self._subappendix_el = 'h3'
                if 0:\
                print(asciibox(#['%(headline_text)s:' % spec,
                               ['_subappendix_el ist %r('
                                % (self._subappendix_el,),
                                ],
                               ch='#',
                               kwargs=spec))

                # nun die Auswertungsreihenfolge:
                for name in CHECKED_TOPICS:
                    try:
                        tup = (name,
                               DETECTOR[name],
                               target[name],
                               )
                    except KeyError:
                        continue
                    if name in target:
                        self._detectors.append(tup)
                    if name in ('index',
                                ):
                        self._detectors_postponed.append(tup)
                    else:
                        self._detectors_primary.append(tup)
                first = False
            else:
                raise ValueError('Derzeit wird nur *eine* Liste von '
                                 u'Anhängen unterstützt!')

        self._hits = 0
        self._misses = 0
        self._total = 0
        self._indexed = 0

    def __nonzero__(self):
        """
        Der Dispatcher ist "vorhanden", wenn er potentiell reale
        Verzeichnisse erzeugt; für diese gibt es jeweils eine
        sorting-Festlegung
        """
        return bool(self._sortings)

    def dispatch(self, elem, chapter):
        """
        Stecke das übergebene Element in das korrekte Verzeichnis
        """
        self._total += 1
        name = None
        try:
            for name, hit, target in self._detectors_primary:
                if hit(elem):
                    target.append(elem, chapter)
                    self._hits += 1
                    return
            self._misses += 1
        finally:
            # Nachgelagert: Index
            for ign_name, hit, target in self._detectors_postponed:
                if hit(elem):
                    target.append(elem, chapter)
                    self._indexed += 1

    def inject_number(self, number, item):
        """
        Die Generierung von Kapitelnummern per CSS ist leider
        unzuverlässig - jedenfalls aber durch anderen Code realisiert
        als in Unitracc für die Gruppierung von Verzeichniseinträgen
        implementiert.

        Es wird daher die Kapitelnummer serverseitig eingefügt.
        """
        return inject_number(self._soup, number, item)

    def register_chapter(self, number, item):
        """
        Registriere eine Überschrift (für gruppierende Verzeichnisse).
        Füge die Nummer als span.number in die Überschrift ein
        und packe den Text in ein span.label; siehe forks.inject_number

        number -- eine Tupel von Ganzzahlen
        item -- ein HTML-Knoten (BeautifulSoup)
        """
        item = self.inject_number(number, item)
        self._chapters_nodes[number] = item
        return item

    def get_chapter_info(self, number):
        repo = self._chapters_tuples
        if number not in repo:
            item = self._chapters_nodes[number]
            title = item.string.strip()
            level = len(number)
            dic = div_creation_kwargs[level]
            repo[number] = (title, dic)
        return repo[number]

    def elem(self):
        """
        Erzeuge den Anhang und gib ihn zurück.

        Der Anhang wird erzeugt, wenn mindestens eine seiner Listen
        erzeugt wird.
        """
        root = None
        pp(((self._total, 'total'),
            (self._hits, 'hits'),
            (self._misses, 'misses'),
            (self._indexed, 'indexed'),
            ))
        if self._detectors:
            spec = self._info['appendixes'][0]
        pp([(tup[0], tup[2])
            for tup in self._detectors
            ])
        for ign_name, ignored, target in self._detectors:
            sublist = target.elem()
            if sublist is not None:
                if root is None:
                    soup = self._soup
                    make_id = self._hub[ID_FACTORY]
                    id = make_id('appendix', 'appendix')
                    root = soup.new_tag('div', id=id)
                    headline = make_headline_element(soup, spec, 'h2',
                                                     self._hub)
                    # txt = self._hub['translate']('Appendix')
                    # headline = make_tag(soup, 'h2', txt)
                    if headline is not None:
                        root.append(headline)
                    if isinstance(target,
                                  (SolutionsDirectory,
                                   ExerciseDirectory,
                                   )):
                        add_class(root, 'enforce-left-page')

                root.append(sublist)
        return root
# --------------------------------- ] ... Klasse DirectoryDispatcher ]


# ------------------------- [ Hilfsfunktionen: Elemente erzeugen ... [
def make_headline_element(soup, spec, tagspec, hub):
    """
    soup -- die Suppe
    spec -- wie von evaluateTocDefinition oder evaluateAppendixDefinition
            erzeugt
    tagspec -- vorerst der Elementname (meistens h2, h3 ...)
    hub -- für den Zugriff auf den translate-Browser
    """
    if spec['headline_text'] is None:
        return None
    txt = spec['headline_text']
    if spec['headline_translate']:
        txt = hub['translate'](txt)
    tagname, kwargs = parse_selector(tagspec)
    if 0:
        pp(('make_headline_element:',
            ('tagspec:', tagspec),
            ('tagname:', tagname),
            ('kwargs:', kwargs),
            ))
    if tagname is None:
        tagname = 'h2'
    return make_tag(soup, tagname, txt, **kwargs)


def make_page_link(soup, txt, link2id, name='p', **kwargs):
    """
    >>> soup = BeautifulSoup()
    >>> make_page_link(soup, 'Siehe Seite', 'page-42')
    <p class="print-only">Siehe Seite <a class="page-ref" href="#page-42"></a></p>
    """
    fix_class_arg(kwargs, default='print-only')
    elem = soup.new_tag(name, **kwargs)
    elem.append(txt)
    if not txt.endswith(' '):
        elem.append(' ')
    elem.append(soup.new_tag('a', **{'href': '#'+link2id,
                                     'class': 'page-ref',
                                     }))
    return elem


# ---------------------------------- [ ToC-Eintrag erzeugen ... [
# ----------- [ alte Version, ro-(RealObjects)-Klassen ... [
def make_classargs(mask='ro-toc-level-%(level)d'):
    """
    >>> bonk = make_classargs('bonk-%(level)d')
    >>> bonk_proxy = Proxy(bonk)
    >>> dic1 = bonk_proxy[1]
    >>> sorted(dic1.items())
    [('class', ['bonk-1'])]
    """
    def make_dict(level):
        dic = WriteProtected({'class': [mask % locals()]
                              })
        dic.freeze()
        return dic
    return make_dict

# Achtung - dieses dict-Objekt liefert bei gleichen Schlüsselwerten
#           immer *dasselbe* dict zurück; daher ist dieses schreibgeschützt!
div_creation_kwargs = Proxy(make_classargs())
# ----------- ] ... alte Version, ro-(RealObjects)-Klassen ]


# ------------------------------------- [ neue Version ... [
def make_classval(mask='toc-level-%(level)d'):
    """
    >>> bonk = make_classval('bonk-%(level)d')
    >>> bonk_proxy = Proxy(bonk)
    >>> bonk_proxy[1]
    'bonk-1'
    """
    def make_string(level):
        return mask % locals()
    return make_string

tocdiv_class = Proxy(make_classval('toc-level-%(level)d'))

def make_toc_entry(elem, level):
    """
    >x> soup = BeautifulSoup('')
    >x> text = 'Headline content'
    >x> theid = 'abc123'
    >x> level = 1
    >x> make_toc_entry(soup, text, theid, level)
    <div class="ro-toc-level-1"><a href="#abc123">Headline content</a></div>

    Neues Verhalten:
    - item wird anstelle text übergeben;
    - theid entfällt (dem Element zu entnehmen)
    - die Nummer ist im span.number enthalten und muß sich in einem
      entsprechenden Element wiederfinden
    - der Text ist im span.text enthalten (und in etwaigen Kindern)
    >>> soup = BeautifulSoup('<h2 id="42">Die Antwort</h2>')
    >>> h2 = soup.h2
    >>> wrapped = inject_number(soup, (4, 2), h2)
    >>> wrapped
    <h2 id="42"><span class="chapter-number">4.2</span> <span class="headline-text">Die Antwort</span></h2>

    Dieses Element "wrapped" wird nun an make_toc_entry übergeben - und
    darf dabei nicht aufgezehrt werden:

    >>> make_toc_entry(wrapped, 1)
    <div class="toc-level-1"><span class="chapter-number">4.2</span> <a class="headline-text" href="#42">Die Antwort</a></div>
    >>> wrapped
    <h2 id="42"><span class="chapter-number">4.2</span> <span class="headline-text">Die Antwort</span></h2>

    Die Überschrift darf Kindelemente haben, z. B.:
    >>> soup = BeautifulSoup('<h3 id="co2">CO<sub>2</sub></h3>')
    >>> h3 = soup.h3
    >>> wrapped = inject_number(soup, (1, 2), h3)
    >>> wrapped
    <h3 id="co2"><span class="chapter-number">1.2</span> <span class="headline-text">CO<sub>2</sub></span></h3>
    >>> make_toc_entry(wrapped, 2)
    <div class="toc-level-2"><span class="chapter-number">1.2</span> <a class="headline-text" href="#co2">CO<sub>2</sub></a></div>
    >>> wrapped
    <h3 id="co2"><span class="chapter-number">1.2</span> <span class="headline-text">CO<sub>2</sub></span></h3>

    Es gibt auch Überschriften ohne Nummer:
    >>> soup = BeautifulSoup('<h2 id="appendix">Anhang</h2>')
    >>> h2 = soup.h2
    >>> wrapped = inject_number(soup, (4,), h2, appendix_dots)
    >>> wrapped
    <h2 id="appendix"><span class="headline-text">Anhang</span></h2>
    >>> make_toc_entry(wrapped, 1)
    <div class="toc-level-1"><a class="headline-text" href="#appendix">Anhang</a></div>

    Wenn Überschriften mit einem Doppelpunkt enden, wird dieser im
    Verzeichniseintrag entfernt:
    >>> soup = BeautifulSoup('<h4 id="appendix">Fragen zum Thema:</h4>')
    >>> h4 = soup.h4
    >>> wrapped = inject_number(soup, (1, 2, 3), h4, appendix_dots)
    >>> wrapped
    <h4 id="appendix"><span class="chapter-number">B.3</span> <span class="headline-text">Fragen zum Thema:</span></h4>
    >>> make_toc_entry(wrapped, 3)
    <div class="toc-level-3"><span class="chapter-number">B.3</span> <a class="headline-text" href="#appendix">Fragen zum Thema</a></div>
    """
    entry = clone(elem)
    theid = entry.attrs.pop('id')
    add_class(entry, tocdiv_class[level])
    entry.name = 'div'
    children = list(entry.children)
    assert len(children) <= 3, \
            ('3 Kinder erwartet (span.chapter-number, " " und '
             'span.headline-text); '
             '%(children)s'
             ) % locals()
    thelink = children[-1]
    thelink.name = 'a'
    thelink.attrs['href'] = '#'+theid
    # etwaigen Doppelpunkt am Ende entfernen;
    # provisorische Lösung:
    linktext = thelink.string
    if linktext:
        linktext = linktext.rstrip()
        if linktext.endswith(':'):
            thelink.string = linktext[:-1]
    return entry

    # Generische Lösung; funktioniert leider noch nicht:
    stack = list(entry.strings)
    while stack:
        child = stack.pop()
        s = child.rstrip()
        if s:
            if s.endswith(':'):
                child.string = s
            break
    return entry
# ------------------------------------- ] ... neue Version ]
# ---------------------------------- ] ... ToC-Eintrag erzeugen ]

# ------------------------- ] ... Hilfsfunktionen: Elemente erzeugen ]


if __name__ == '__main__':
    # Standard library:
    import doctest
    doctest.testmod()
