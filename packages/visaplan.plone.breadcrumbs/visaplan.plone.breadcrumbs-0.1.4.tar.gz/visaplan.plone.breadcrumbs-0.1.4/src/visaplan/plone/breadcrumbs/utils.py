# -*- coding: utf-8 -*- vim: ts=8 sts=4 sw=4 si et tw=79
"""\
utils-Modul für unitracc->breadcrumbs
"""

# Python compatibility:
from __future__ import absolute_import

from six.moves import map

__author__ = "Tobias Herp <tobias.herp@visaplan.com>"
VERSION = (0,
           4,  # delete_last_nonfolderish_basecrumb
           )
__version__ = '.'.join(map(str, VERSION))

# ------------------------------------------------------ [ Daten ... [
LAST_NONFOLDERISH_BASECRUMB_KEY = 'last_nonfolderish_basecrumb_idx'

__all__ = (
    'crumbdict',
    'title_or_caged_id',
    'delete_last_nonfolderish_basecrumb',
    'LAST_NONFOLDERISH_BASECRUMB_KEY',
    )
# ------------------------------------------------------ ] ... Daten ]


# ------------------------------------------------- [ Funktionen ... [
def crumbdict(title, href, cls=''):
    return {'title': title,
            'href': href,
            # 'class': cls,
            }


def title_or_caged_id(o):
    """
    Zur Vermeidung unsichtbarer Brotkrümel
    """
    try:
        txt = o.Title().strip()
    except (AttributeError,):
        txt = None
    if txt:
        return txt
    return o.id.join(('[', ']'))


def title_or_caged_id__tup(o):
    """
    Zur Vermeidung unsichtbarer Brotkrümel:
    wie title_or_caged_id, gibt aber ein Tupel zurück
    """
    # TODO: dokumentieren; wozu braucht man das?!
    try:
        txt = o.Title().strip()
    except (AttributeError,):
        txt = None
    if txt:
        la = o.Language()
        return txt, not la
    else:
        return o.id.join(('[', ']')), False


def delete_last_nonfolderish_basecrumb(info, crumbs):
    """
    Lösche den letzten von BaseParentsCrumbs erzeugten Krümel,
    sofern dieser kein ordnerartiges Objekt bezeichnet
    """
    try:
        delidx = info[LAST_NONFOLDERISH_BASECRUMB_KEY]
    except KeyError:
        pass
    else:
        if delidx is not None:
            del crumbs[delidx]
            # weitere Löschung verhindern:
            info[LAST_NONFOLDERISH_BASECRUMB_KEY] = None
# ------------------------------------------------- ] ... Funktionen ]

if __name__ == '__main__':
    # Standard library:
    import doctest
    doctest.testmod()
