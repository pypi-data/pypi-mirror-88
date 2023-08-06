# -*- coding: utf-8 -*- vim: ts=8 sts=4 sw=4 si et tw=72
"""\
sniff.py - HTML-Knoten erkennen
"""

# Python compatibility:
from __future__ import absolute_import

# Standard library:
from re import IGNORECASE
from re import compile as re_compile
from re import match

# visaplan:
from visaplan.kitchen.spoons import (
    has_all_classes,
    has_any_class,
    has_class,
    is_block_element,
    is_empty,
    )
from visaplan.tools.classes import Proxy

__all__ = [# Testfunktionen:
           'is_cooked_image',
           'is_cooked_formula',
           'is_cooked_animation',
           'is_cooked_video',
           'is_cooked_audio',
           'is_cooked_media',
           'is_cooked_table',
           'is_cooked_standard',
           'is_cooked_literature',
           'is_cooked_glossary',
           'is_question',
           # Übungslisten aus W3L-Importen:
           'is_questions_list',
           'contains_questions_list',
           # Marginalien aufräumen:
           'is_marginal',
           'is_marginal_div',
           'has_transformed_image',
           # sonstige Verdächtige:
           'often_empty',
           # konvertiert Marginalien:
           'is_block',
           ]

# ------------------------------------------- [ Objekte erkennen ... [
"""
Die folgenden Funktionen akzeptieren als einziges Argument ein
HTML-Element wie von BeautifulSoup erzeugt.
"""

def created_by_transform_images(elem):
    return has_all_classes(elem, ('media',
                                  intern('transformed-image'),
                                  ))

def created_by_transform_files(elem):
    return has_all_classes(elem, ('media',
                                  intern('transformed-file'),
                                  ))

def is_cooked_media(elem):
    return has_class(elem, 'media')


# ------------------------------------ [ derzeit nicht verwendet ... [
def make_has_no_such_parent(func):
    """

    """
    def has_no_such_parent(elem):
        """
        Untersucht nur das unmittelbare Elternelement.

        Es geht immer um Knoten im Baum; diese haben stets zumindest ein
        Elternelement (html, body); html- und body-Elemente werden von
        dieser Funktion nicht untersucht
        """
        par = elem.parent
        if par is None:
            # kein solches Elternelement -- aber auch kein anderes
            return False
        return not func(par)
    return has_no_such_parent

def make_has_no_such_ancestor(func):
    def has_no_such_ancestor(elem):
        for par in elem.parents:
            if par is None:
                return True
            if func(par):
                return False
        return True
    return has_no_such_ancestor
# ------------------------------------ ] ... derzeit nicht verwendet ]

RE_REFERENCES_UID = re_compile('\\b'
                               'resolveuid'
                               '/'
                               '[0-9a-f]{32}'
                               '\\b',
                               IGNORECASE)
"""
Test des regulären Ausdrucks:

>>> uid = '0123456789abcdef0123456789abcdef'
>>> val = '/resolveUid/%s/honk' % uid
>>> match(RE_REFERENCES_UID, val) is not None
True
>>> uid += '0'
>>> val = '/resolveUid/%s/honk' % uid
>>> match(RE_REFERENCES_UID, val) is not None
False
"""
def is_image_with_uid(elem):
    if elem.name != 'img':
        return False
    try:
        val = elem.attrs['src']
    except (KeyError, AttributeError):
        return False
    else:
        match(RE_REFERENCES_UID, val) is not None


def is_free_image_with_uid(elem):
    if not is_image_with_uid(elem):
        return False
    pa = elem.parent
    if pa is not None and is_cooked_media(pa):
        return False
    return True


def is_cooked_image(elem):
    """
    Erkennt mehrere Varianten
    """
    for f in (created_by_transform_images,
              # oder img, aber ohne div.media:
              is_free_image_with_uid,
              ):
        if f(elem):
            return True
    return False


def is_cooked_formula(elem):
    if not is_cooked_media(elem):
        return False
    for child in elem.children:
        if child.name == 'img':
            # wenn ein Bild, dann das der Formel:
            return has_class(child, 'unitracc-formula')
        elif child.name == 'div':
            if has_class(child, 'unitracc-formula'):
                return True
    return False


def is_cooked_animation(elem):
    if not is_cooked_media(elem):
        return False
    for child in elem.children:
        if child.name == 'object':
            return True
    return False


def is_cooked_video(elem):
    if not is_cooked_media(elem):
        return False
    for child in elem.children:
        if child.name == 'video':
            return True
    return False


def is_cooked_audio(elem):
    if not is_cooked_media(elem):
        return False
    for child in elem.children:
        if child.name == 'audio':
            return True
    return False


def is_cooked_table(elem):
    return has_class(elem, 'area-table')


def is_cooked_literature(elem):
    return has_class(elem, 'unitracc-literature')


def is_cooked_standard(elem):
    return has_class(elem, 'unitracc-standard')


def is_cooked_glossary(elem):
    return has_any_class(elem, (# in importierten W3L-Kursen:
                                'glossar',
                                # postuliert:
                                'unitracc-glossary',
                                ))
# ------------------------------------------- ] ... Objekte erkennen ]

def is_marginal(elem):
    """
    Handelt es sich um Inhalt für die Marginalspalte?
    """
    return has_any_class(elem, ['marginalia',
                                'marginal',
                                ])


def is_marginal_div(elem):
    """
    Marginalien werden in span-Elemente konvertiert, um sie in Absätzen
    plazieren zu können; diese Funktion identifiziert solche, bei denen
    das (noch) nicht geschehen ist.
    """
    return elem.name == 'div' and is_marginal(elem)


def often_empty(elem):
    """
    Erkenne einige Elemente, die gern mal leer sind bzw.
    nur Leerraum und allenfalls ein br-Element enthalten.

    Achtung: Diese Funktion darf nur auf solche Elemente anschlagen,
    für die --> is_empty sinnvolle Ergebnisse liefert!
    """
    n = elem.name
    if n == 'div' and has_any_class(elem, ('attribute-text',
                                           'attribute-title',
                                           )):
        return True
    return n == 'p' and not elem.attrs


def is_block(elem):
    """
    Für Bereinigung von Absätzen mit split_paragraphs
    """
    if elem.name == 'div' and is_marginal(elem):
        elem.name = 'span'
        return False
    return is_block_element(elem)


def is_question(elem):
    return has_class(elem, 'question')


def is_questions_list(elem):
    """
    ueblist-Elemente aus w3l-Importen -> ol.questions:

    Konsistent halten mit -> contains_questions_list!
    """
    return elem.name == 'ol' and has_class(elem, 'questions')


def contains_questions_list(soup):
    """
    Konsistent halten mit -> is_questions_list!
    """
    return soup.find('ol', class_='questions') is not None


def has_transformed_image(elem):
    """
    Zur Verwendung in Marginalien:
    Solche Elemente enthalten üblicherweise ein a[name] und, um das
    enthaltene Bild, ein a[href][onclick].
    """
    if elem.name != 'div':
        return False
    return has_class(elem, 'transformed-image')
