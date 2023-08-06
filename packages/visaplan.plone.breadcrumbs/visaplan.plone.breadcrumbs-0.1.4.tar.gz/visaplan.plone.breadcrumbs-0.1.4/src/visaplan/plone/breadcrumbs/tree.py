# -*- coding: utf-8 -*- vim: ts=8 sts=4 sw=4 si et tw=79
"""\
tree-Modul für unitracc->breadcrumbs:

und die Kaskade der Breadcrumb-Funktionen
"""
# TODO: unnötige Breadcrumb-Klassen eliminieren
#       (möglichst auf Grundtypen zurückführen)

# Python compatibility:
from __future__ import absolute_import

from six.moves import map
from six.moves.urllib.parse import urlencode

__author__ = "Tobias Herp <tobias.herp@visaplan.com>"
VERSION = (0,
           4,  # Krümelklassen nun in .base
           )
__version__ = '.'.join(map(str, VERSION))

# Setup tools:
import pkg_resources

# Standard library:
from collections import defaultdict

# Zope:
import zope.component.hooks

try:
    pkg_resources.get_distribution('visaplan.plone.browsers')
except pkg_resources.DistributionNotFound:
    HAS_VISAPLANPLONEBROWSERS = False
else:
    HAS_VISAPLANPLONEBROWSERS = True
    # visaplan:
    from visaplan.plone.browsers.management.crumbs import OK

try:
    pkg_resources.get_distribution('visaplan.plone.groups')
except pkg_resources.DistributionNotFound:
    HAS_VISAPLANPLONEGROUPS = False
else:
    HAS_VISAPLANPLONEGROUPS = True
    from visaplan.plone.groups.groupdesktop.crumbs import OK

# visaplan:
from visaplan.tools.minifuncs import translate_dummy as _

# Local imports:
from visaplan.plone.breadcrumbs._vars import SHORTCUT_TEMPLATES
from visaplan.plone.breadcrumbs.base import (
    BaseEditCrumb,
    BaseParentsCrumbs,
    ContextCrumb,
    DesktopBrowserCrumb,
    GenericContainerCrumb,
    GenericViewCrumb,
    NoCrumbs,
    NoCrumbsException,
    RootedBrowserCrumb,
    SkipCrumb,
    register,
    registered,
    tellabout_call,
    )

# Logging / Debugging:
from pdb import set_trace
from visaplan.plone.tools.log import getLogSupport
from visaplan.tools.debug import pp

# --------------- [ Registrierung wichtiger Krümel sicherstellen ... [
# (Nicht mehr nötig in visaplan.plone.breadcrumbs 1+)

# --------------- ] ... Registrierung wichtiger Krümel sicherstellen ]


logger, debug_active, DEBUG = getLogSupport(defaultFromDevMode=0)

__all__ = ('register_crumbs',
           # Shortlist wichtiger Breadcrumb-Funktionen:
           'base_crumbs',
           )


# ------------------------------------------------------ [ Daten ... [
base_crumbs = None  # --> register_crumbs()
# ------------------------------------------------------ ] ... Daten ]


# -------------------- [ Brotkrümel-Registry: Crumb-Klassen ... [
# -------------------- ] ... Brotkrümel-Registry: Crumb-Klassen ]


# -------------------------------------------- [ Registry füllen ... [

# ------------------------------- [ Krümel für Gruppenforen ... [
# ... siehe (gf) ../../browser/groupboard/crumbs.py
# ------------------------------- ] ... Krümel für Gruppenforen ]
                # --- Bereich Verwaltung/Mgmt ---

# --------------------------------- [ Krümel für Verwaltung ... [
# ... siehe (gf) ../../browser/management/crumbs.py
# --------------------------------- ] ... Krümel für Verwaltung ]

# <a href="/portal_lock_manager/pane_manage_locks" Lock Manager
# ----------------------------- [ Krümel für TAN-Verwaltung ... [
# ... siehe (gf) ../../browser/tan/crumbs.py
# ----------------------------- ] ... Krümel für TAN-Verwaltung ]

# ------------------------------ [ Krümel für Exportprofile ... [
# ... siehe (gf) ../../browser/export/crumbs.py
# ------------------------------ ] ... Krümel für Exportprofile ]

# ----------------------- [ Krümel für Easyvoc-Wörterbücher ... [
# ... siehe vorerst (gf) ../../browser/management/crumbs.py;
# Browser easyvoc entstammt tomcom.easyvoc
# ----------------------- ] ... Krümel für Easyvoc-Wörterbücher ]

# ----------------- [ Krümel für Plone-Konfigurationsseiten ... [
# ----------------- ] ... Krümel für Plone-Konfigurationsseiten ]

# --------------------------------- [ Templates ohne Krümel ... [
# --------------------------------- ] ... Templates ohne Krümel ]
# -------------------------------------------- ] ... Registry füllen ]

NOCRUMBS = set([
    'fg_base_view_p3', # Kontaktseite: Akquise reicht
    'index_html',      # sinnfrei, oder?
    'document_view',   # direkter Aufruf einer Seite
    'default_page_view', # Standardseite eines Ordners
    'document_and_ads_view',  # Red. Inhalt und Werbung
    'get',  # produktiv beobachtet am 26.5.2017
    # aus Logdatei:
    'book_agenda_view',
    'fg_thankspage_view_p3',
    'localsearch_ajax_view',
    'localsearch_bookcarousels_view',
    'localsearch_mediacarousels_view',
    'logged_out',
    'set',
    'translate_item',
    # Ansichtstemplate:
    'unitraccauthor_view',
    # (other unitracc..._view templates: see Productsu.unitracc.oldcrumbs)
])

# -------------------------------------------- [ Initialisierung ... [
def register_crumbs():
    global base_crumbs
    desktop_crumbs = registered('group-desktop')
    base_crumbs = BaseParentsCrumbs('')

    generic_container_crumb = \
            register(GenericContainerCrumb(
                '--generic container--', [registered('group-desktop')]))

    generic_view_crumb = register(SkipCrumb('base_view'))

    for tid in ('base_edit',
                'atct_edit',
                ):
        register(BaseEditCrumb(tid, [generic_view_crumb]))
    register(ContextCrumb('code-audit', 'Code audit', [generic_view_crumb]))
    for tid in NOCRUMBS:
        register(SkipCrumb(tid))

    for template_id in SHORTCUT_TEMPLATES:
        register(NoCrumbs(template_id))
    for tid, label in [
            ('editProfile',
             _('Benutzerkonto'),
             ),
            ]:
        register(DesktopBrowserCrumb(tid, label,
                                     'myaccount',
                                     [registered('group-desktop')]))

    for tid in ('manage-portlets',
                'manage-viewlets',
                ):
        register(GenericViewCrumb(tid))

    # --------------------------- [ collective.logbook ... [
    logbook_root_crumb = register(
        RootedBrowserCrumb('logbook',
                           'Error log',
                           None,
                           [registered('management_view')]))
    for tid, label in (('logbook-controlpanel', 'Configuration'),
                ('error-test', None),
                ('random-error-test', 'Random error'),
                ):
        register(RootedBrowserCrumb(tid, label, None,
                                    [logbook_root_crumb]))
    # --------------------------- ] ... collective.logbook ]

register_crumbs()
# -------------------------------------------- ] ... Initialisierung ]

# ---------------------------------- [ Entwicklungsunterstützung ... [
class Node(object):
    def __init__(self, name, o):
        self.name = name
        self.o = o
        self.children = []

def make_forest(namespace, attribute='getParent'):
    """
    Erstelle einen Wald mit Bäumen.
    Bäume sind alle Elemente, die kein Elternelement haben.
    """
    children_of = defaultdict(list)
    """
    nodes_list = []
    nodes_dict = {}
    for name, o in namespace.items():
        node = Node(name, o)
        nodes_list.append(node)
        nodes_dict[name] = node
    remaining = set(nodes_list)
    while remaining:
        for node in remaining:
            pa = node.o.getParent()
            if pa is None:

                children_of[node]
    """
    twigs = set(namespace.values())
    # set_trace()
    done = set()
    imax = 20
    cnt = 0
    while twigs:
        for twig in twigs:
            pa = getattr(twig, attribute)()
            if pa is None:
                children_of[twig] = []
                done.add(twig)
            elif pa in children_of:
                children_of[pa].append(twig)
                done.add(twig)
        if done:
            pp(len(done), 'Aenderungen ...', done)
            twigs.difference_update(done)
            done.clear()
            pp('noch %d uebrig' % len(twigs))
        cnt += 1
        if cnt >= imax:
            pp('%d nicht verarbeitet:' % len(twigs),
               twigs)
            break
    return dict(children_of)


if debug_active:
    # Local imports:
    from visaplan.plone.breadcrumbs.base import REGISTRY
    if 0 and 'make forest':
        forest = make_forest(REGISTRY)
        pp( 'der Wald ...', forest, '... der Wald')
    else:
        pp(REGISTRY,
           '(%d registrierte Breadcrumb-Funktionen' % len(REGISTRY))
# ---------------------------------- ] ... Entwicklungsunterstützung ]
