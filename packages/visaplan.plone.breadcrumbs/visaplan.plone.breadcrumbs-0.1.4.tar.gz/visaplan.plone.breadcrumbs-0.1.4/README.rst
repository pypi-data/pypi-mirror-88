.. This README is meant for consumption by humans and pypi. Pypi can render rst files so please do not use Sphinx features.
   If you want to learn more about writing documentation, please check out: http://docs.plone.org/about/documentation_styleguide.html
   This text does not appear on pypi or github. It is a comment.

==========================
visaplan.plone.breadcrumbs
==========================

This package provides breadcrumbs classes for object trees in Zope/Plone
instances; e.g., it is possible to have the ``uid`` request variable used for
the breadcrumb if a certain template is used.

For each view template name, it allows the registration of an executable
breadcrumbs instance, which may create zero or more breadcrumbs and then give
over processing to a parent breadcrumb. Such breadcrumbs instances usually use
the current value of a certain request variable, or they may suppress the
creation of any breadcrumbs at all.

**NOTE:**

The purpose of this package is *not* to provide new functionality
but to factor out existing functionality from an existing monolitic Zope product.
Thus, it is more likely to lose functionality during further development
(as parts of it will be forked out into their own packages,
or some functionality may even become obsolete because there are better
alternatives in standard Plone components).


Features
--------

- Breadcrumbs classes for several use cases
- A simple registry for breadcrumbs and the templates they are triggered by

Due to it's history, this package still has a few dependencies which are not
really important for the core functionality but rather are related to
particular breadcrumbs classes of our old monolithic product and it's eggified
successors. For this reason, and because of some weaknesses of the current
breadcrumbs registry, the current versions are called *0.x*.

Before you fork you own mycompany.plone.breadcrumbs package, here is what we
plan for the 1.x versions:

- The ``register`` function will take ...

  - the *name* of a breadcrumbs class,
  - the (single) parent (or ``None``, for the standard breadcrumbs from the
    objects tree), and
  - optional keyword arguments.

  Currently, it takes an instance of a breadcrumbs class, and the further
  information thrown at the breadcrumbs class when constructing the instance.
  The main drawback is that the parent breadcrumb needs to already exist when a
  new breadcrumb is to be registered, which leads to very annoying module
  dependenies.

  Thus, versions 1.x will take all the necessary information during
  registration, and will create a breadcrumb instance when it is first used,
  including the ``parent`` (and "grandparents", if any).

- The ``parents`` list will be replaced by a single ``parent``;
  each breadcrumb has exactly one parent to which it hands over it's results
  after processing (or ``None``, which will cause the usual standard
  breadcrumbs to be created from the objects tree).

- The ``tweak`` method will likely be renamed to something more reasonable;
  unless someone comes up with something better, this will be ``process``.
  It's signature might change, too.


Examples
--------

This add-on can be seen in action at the following sites:

- https://www.unitracc.de
- https://www.unitracc.com


Documentation
-------------

Sorry, we don't have real user documentation yet.


Installation
------------

Install visaplan.plone.breadcrumbs by adding it to your buildout::

    [buildout]

    ...

    eggs =
        visaplan.plone.breadcrumbs


and then running ``bin/buildout``


Contribute
----------

- Issue Tracker: https://github.com/visaplan/visaplan.plone.breadcrumbs/issues
- Source Code: https://github.com/visaplan/visaplan.plone.breadcrumbs


Support
-------

If you are having issues, please let us know;
please use the `issue tracker`_ mentioned above.


License
-------

The project is licensed under the GPLv2.

.. _`issue tracker`: https://github.com/visaplan/PACKAGE/issues

.. vim: tw=79 cc=+1 sw=4 sts=4 si et
