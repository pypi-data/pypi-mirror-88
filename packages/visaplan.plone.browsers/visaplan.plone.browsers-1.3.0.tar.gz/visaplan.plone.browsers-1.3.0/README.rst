.. This README is meant for consumption by humans and pypi. Pypi can render rst files so please do not use Sphinx features.
   If you want to learn more about writing documentation, please check out: http://docs.plone.org/about/documentation_styleguide.html
   This text does not appear on pypi or github. It is a comment.

=======================
visaplan.plone.browsers
=======================

A brown bag of "browsers" for Plone sites.

The purpose of this package (for now) is *not* to provide new functionality
but to factor out existing functionality from an existing monolitic Zope product.
Thus, it is more likely to loose functionality during further development
(as parts of it will be - or have already been - forked out into their own packages,
or some functionality may even become obsolete because there are better
alternatives in standard Plone components).

It is currently not expected to be useful to a broader audience;
many "browsers" implemented here are very specific to our sites like they exist
now.


Examples
--------

This add-on can be seen in action at the following sites:

- https://www.unitracc.de
- https://www.unitracc.com


Installation
------------

Install visaplan.plone.browsers by adding it to your buildout::

    [buildout]

    ...

    eggs =
        visaplan.plone.browsers


and then running ``bin/buildout``


Contribute
----------

- Issue Tracker: https://github.com/visaplan/visaplan.plone.browsers/issues
- Source Code: https://github.com/visaplan/visaplan.plone.browsers


Support
-------

If you are having issues, please let us know;
please use the `issue tracker`_ mentioned above.


License
-------

The project is licensed under the GPLv2.

The submodule `.unitraccmail.mail` is a copy of the mail module by Christian
Heimes, which is protected by the Zope Public License, Version 2.1 (ZPL).

.. _`issue tracker`: https://github.com/visaplan/visaplan.plone.browsers/issues

.. vim: tw=79 cc=+1 sw=4 sts=4 si et
