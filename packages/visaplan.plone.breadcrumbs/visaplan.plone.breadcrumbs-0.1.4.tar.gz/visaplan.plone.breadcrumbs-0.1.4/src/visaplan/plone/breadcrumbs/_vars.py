# -*- coding: utf-8 -*- vim: ts=8 sts=4 sw=4 si et tw=79
"""\
data module visaplan.plone.breadcrumbs._vars
"""

# Python compatibility:
from __future__ import absolute_import

from six.moves import map

__author__ = "Tobias Herp <tobias.herp@visaplan.com>"
VERSION = (0,
           2,  # Daten für Breadcrumb-Registry
           1,  # Importe geordnet
           )
__version__ = '.'.join(map(str, VERSION))

# Logging / Debugging:
from visaplan.plone.tools.log import getLogSupport

logger, debug_active, DEBUG = getLogSupport(defaultFromDevMode=0)

# die folgenden Templates brechen die Breadcrumb-Generierung ab:
SHORTCUT_TEMPLATES = (
        'refresh_lock',
        'require_login',  # sonst mehrfache Startseitenkrümel
        'mainpage_view',  # wenig prakt. Nährwert; Platzverschwendung
        )
# die folgenden Templates unterdrücken die Erzeugung eines
# Schreibtischkrümels durch die BaseParentsCrumbs-Klasse:
NODESKTOP_TEMPLATES = (
        'folder_contents',
        'folder_listing',
        )
# die folgenden Templates erzeugen Krümel auch für von der Navigation
# ausgeschlossene Ordner (bzw. Objekte):
LISTING_TEMPLATES = (
        'folder_contents',
        'folder_listing',
        )
