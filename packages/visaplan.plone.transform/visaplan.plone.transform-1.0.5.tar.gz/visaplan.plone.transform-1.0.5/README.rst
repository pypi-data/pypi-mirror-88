.. This README is meant for consumption by humans and pypi. Pypi can render rst files so please do not use Sphinx features.
   If you want to learn more about writing documentation, please check out: http://docs.plone.org/about/documentation_styleguide.html
   This text does not appear on pypi or github. It is a comment.

.. image::
   https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336
       :target: https://pycqa.github.io/isort/

========================
visaplan.plone.transform
========================

HTML transformations for Plone sites.

The purpose of this package is *not* to provide new functionality (for now)
but to factor out existing functionality from an existing monolitic Zope product.
Thus, it is more likely to lose functionality during further development
(as parts of it will be forked out into their own packages,
or some functionality may even become obsolete because there are better
alternatives in standard Plone components).


Features
--------

- Several transformations for HTML pages, including generation of TOCs etc.


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

Install visaplan.plone.transform by adding it to your buildout::

    [buildout]

    ...

    eggs =
        visaplan.plone.transform


and then running ``bin/buildout``


Contribute
----------

- Issue Tracker: https://github.com/visaplan/visaplan.plone.transform/issues
- Source Code: https://github.com/visaplan/visaplan.plone.transform


Support
-------

If you are having issues, please let us know;
please use the `issue tracker`_ mentioned above.


License
-------

The project is licensed under the GPLv2.

.. _`issue tracker`: https://github.com/visaplan/PACKAGE/issues

.. vim: tw=79 cc=+1 sw=4 sts=4 si et
