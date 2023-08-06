# -*- coding: utf-8 -*- Umlaute: ÄÖÜäöüß
"""
Adapter-Package breadcrumbs - Generierung von Brotkrümel-Navigationshilfen
"""

# Python compatibility:
from __future__ import absolute_import

# visaplan:
from visaplan.plone.base import Base, Interface
from visaplan.plone.infohubs import make_hubs

# Local imports:
from visaplan.plone.breadcrumbs._vars import SHORTCUT_TEMPLATES
from visaplan.plone.breadcrumbs.base import (
    NoCrumbsException,
    RootedBrowserCrumb,
    RootedDefaultCrumb,
    SkipCrumb,
    register,
    registered,
    )
from visaplan.plone.breadcrumbs.tree import base_crumbs, register_crumbs
from visaplan.plone.breadcrumbs.utils import crumbdict

# Logging / Debugging:
from pdb import set_trace
from visaplan.plone.tools.log import getLogSupport
from visaplan.tools.debug import pp

logger, debug_active, DEBUG = getLogSupport(defaultFromDevMode=0)

# -------------------------------------------------- [ Interface ... [
class IBreadcrumbs(Interface):
    pass
# -------------------------------------------------- ] ... Interface ]

# ---------------------------------------------------- [ Adapter ... [
class Adapter(Base):

    def __init__(self, arg):
        self.getbrain = None
        Base.__init__(self, arg)

    def __call__(self, gid=None):
        """
        gib eine Sequenz von Dictionarys zurück.

        Argumente:
            gid -- Gruppen-ID (für Gruppenschreibtisch; optional).
                   Wenn None, wird im Request gesucht;
                   unterdrücken mit jedem anderen False-Wert

        Schlüssel:
            href - die URL (ohne Portal-Hostname)
            title - der sichtbare Text
            o - das Objekt (wenn vorhanden; sonst None)
        """
        hub, info = make_hubs(self.context, 0)
        if gid is not None:
            if 1:
                if debug_active and 0:
                    pp((['gid angegeben (veraltet):', gid],
                        ['context:', context],
                        'angegebene <gid> wird ignoriert',
                        ))
            elif gid:
                info['gid'] = gid
            else:
                info['gid'] = None

        crumbs = []
        try:
            base_crumbs(crumbs, hub, info)
            templateid = info['template_id']
            if debug_active >= 2:
                pp((('context:', self.context), ('info:', info), ('crumbs:', crumbs), ('debug_active:', debug_active)))
                set_trace()

            try:
                registered(templateid)(crumbs, hub, info)
            except KeyError as e:
                if debug_active:
                    logger.warning('No crumb adapter for template %(template_id)r',
                                   info)
                    if templateid in ('get',
                                      ):
                        logger.info('Template id %(templateid)r is useless.'
                                    'info: \n%(info)s',
                                    locals())
                if templateid is not None:
                    if (templateid.startswith('manage')
                        or templateid.endswith('management')
                        or templateid.startswith('configure')
                        ):
                        crumbler = RootedDefaultCrumb(templateid,
                                                      [registered('management_view')])
                        logger.info('Created generic breadcrumb function'
                                    ' %(crumbler)s',
                                    locals())
                        register(crumbler)
                        crumbler(crumbs, hub, info)
                    elif (templateid.endswith('-controlpanel')
                          or templateid.endswith('-settings')
                          ):
                        # Dies ergibt manchmal sogar die korrekte Message-ID,
                        # z. B. '@@navigation-controlpanel' -> 'Navigation settings';
                        # zumindest aber kommt etwas lesbares heraus,
                        # z. B. '@@discussion-settings' -> 'Discussion settings'
                        crumbler = RootedBrowserCrumb(templateid,
                                                      '_'.join(templateid.split('-')[:-1]
                                                               ).capitalize()+' settings',
                                                      '',
                                                      [registered('plone_control_panel')])
                        register(crumbler)
                        logger.info('Created generic breadcrumb function'
                                    ' %(crumbler)s',
                                    locals())
                        crumbler(crumbs, hub, info)
                    elif templateid.endswith('folder_view'):
                        crumbler = SkipCrumb(templateid, [])
                        register(crumbler)
                        logger.info('No breadcrumbs by default for template '
                                    '%(templateid)s (%(crumbler)s)',
                                    locals())
                    elif templateid in ('folder_contents',
                                        ):
                        # für diese Templates brauchen wir vielleicht mal spezielle Krümel;
                        # nach Systemstart einmal protokollieren:
                        crumbler = SkipCrumb(templateid, [])
                        register(crumbler)
                        logger.info('No breadcrumbs yet for template '
                                    '%(templateid)s (%(crumbler)s)',
                                    locals())

                    elif templateid is None:
                        logger.error('No breadcrumb found! Context is %(context)r', info)
                    else:
                        logger.error('Unhandled template id %(templateid)r', locals())

        except NoCrumbsException as e:
            DEBUG('%r, aborted: %s', info['context'], e)
            del crumbs[:]
        except AttributeError as e:
            logger.exception(e)
            if templateid is None:
                logger.error('Konnte kein Template ermitteln fuer %s!', self.context)
        except Exception as e:
            logger.exception(e)
            logger.error('Fehler bei Breadcrumbs fuer %s!', self.context)
        finally:
            return crumbs
# ---------------------------------------------------- ] ... Adapter ]
# vim: ts=8 sts=4 sw=4 si et hls
