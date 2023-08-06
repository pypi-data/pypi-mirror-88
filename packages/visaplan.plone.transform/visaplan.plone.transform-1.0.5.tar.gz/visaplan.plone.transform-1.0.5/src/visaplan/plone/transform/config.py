# -*- coding: utf-8 -*- äöü vim: ts=8 sts=4 sw=4 si et tw=79
"""\
config-Modul für transform-Browser

Enthält auch ein paar "Utilities" für Profiling, die aber nicht
(oder zumindest nicht auf einfache Weise) per Doctest testbar sind.
"""
# Python compatibility:
from __future__ import absolute_import, print_function

# Setup tools:
import pkg_resources

# Standard library:
from time import clock, strftime, time

try:
    pkg_resources.get_distribution('visaplan.UnitraccPolicy')
except pkg_resources.DistributionNotFound:
    HAS_POLICYPACKAGE = False
    # visaplan:
    from Products.unitracc.browser.versioninformation.browser import (
        static_info,
        )
else:
    # visaplan:
    from visaplan.UnitraccPolicy.versioninformation.browser import static_info
    HAS_POLICYPACKAGE = True

# visaplan:
from visaplan.tools.minifuncs import makeBool

__all__ = ['CONFIG',  # die eingelesene Konfiguration
           'DEBUG_ACTIVE',
           # 'DEBUG',   obsolet?
           'WATCH_ME',
           ]

TIMESTAMP_FORMAT = '%Y-%m-%d %H:%M:%S'
REV = int(static_info['Revision'])
BRANCH = static_info['svn_branch']
DEFAULTS = {'profile_active': '0',  # obsolet
            'debug_active': '0',
            'watch_me': '0',
            'method': 'soup',  # obsolet; regex gibt es nicht mehr
            'max_iterations': '2',
            }

try:
    # visaplan:
    from visaplan.plone.tools.cfg import get_raw_config
    CONFIG = get_raw_config('transform',
                            DEFAULTS)
except:
    # Standard library:
    from os.path import sep

    # visaplan:
    from visaplan.plone.tools.mock_cfg import get_raw_config

    # Logging / Debugging:
    from visaplan.tools.debug import asciibox
    _fnlist = __file__.split(sep)
    _start = _fnlist.index('Products')
    _fn = sep.join(_fnlist[_start:])
    print(asciibox(['   ***   '.join(['TEST']*5),
                    _fn+':',
                    'verwende keine reale Konfiguration!',
                    ]))
    CONFIG = get_raw_config('transform',
                            DEFAULTS)

DEBUG_ACTIVE = makeBool(CONFIG['debug_active'])
WATCH_ME = makeBool(CONFIG['watch_me'])
# etwaige numerische Werte sind unverdaulich für die Tabelle:
DEBUG = bool(DEBUG_ACTIVE)

METHOD = CONFIG.get('method', 'soup')
assert METHOD in ('regex',
                  'soup',
                  )
if METHOD not in ('regex', 'soup'):
    raise ValueError('Unbekannte Methode %(METHOD)s!' % locals())

MAX_ITERATIONS = int(CONFIG['max_iterations'])
if not 0 < MAX_ITERATIONS <= 5:
    raise ValueError('transform.max_iterations: '
        'Ganzzahl aus (0, 5] erwartet! (%r)'
        % (MAX_ITERATIONS,))
