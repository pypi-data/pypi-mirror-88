.. This README is meant for consumption by humans and pypi. Pypi can render rst files so please do not use Sphinx features.
   If you want to learn more about writing documentation, please check out: http://docs.plone.org/about/documentation_styleguide.html
   This text does not appear on pypi or github. It is a comment.

=======================
visaplan.plone.adapters
=======================

Provides a brown bag of adapters for Plone sites

The purpose of this package is *not* to provide new functionality
but to factor out existing functionality from an existing monolitic Zope product.
Thus, it is more likely to lose functionality during further development
(as parts of it will be forked out into their own packages,
or some functionality may even become obsolete because there are better
alternatives in standard Plone components).


Features
--------


- ``flvinfo`` adapter:

  flash file metadata extraction

- ``getmenulevel`` adapter:

  Catalog query to create a submenu level

- ``grouplog`` adapter:

  Maintains a special logfile for group membership changes

- ``pc2`` adapter:

  The ``portal_catalog`` as a ``decorated_tool``
  (which logs its calls; for development)

- ``pformat`` adapter:

  Makes the ``pprint.pformat`` function available for page template code
  (for development)

- ``puc`` adapter:

  The ``portal_user_catalog`` (if you have one)

- ``rawbyname`` adapter:

  Return the raw contents of the given field

- ``swfinfo`` adapter:

  Parses the header information of a Shockwave Flash (swf) file

- ``uidorint`` adapter:

  Does the given ``value`` or (request) ``varname`` contain a number or a UID?

- ``updateactualurl`` adapter:

  Sets the request variable ``ACTUAL_URL`` to the given value

- ``userlog`` adapter:

  Maintains a special logfile for user account changes, e.g. registrations and
  activations.

  There is a utility script ``parseuserlog`` to extract information from this
  file and write it to a ``CSV`` file.


Examples
--------

This add-on can be seen in action at the following sites:

- https://www.unitracc.de
- https://www.unitracc.com


Installation
------------

Install visaplan.plone.adapters by adding it to your buildout::

    [buildout]

    ...

    eggs =
        visaplan.plone.adapters


and then running ``bin/buildout``


Contribute
----------

- Issue Tracker: https://github.com/visaplan/visaplan.plone.adapters/issues
- Source Code: https://github.com/visaplan/visaplan.plone.adapters


Support
-------

If you are having issues, please let us know;
please use the `issue tracker`_ mentioned above.


License
-------

The project is licensed under the GPLv2.

.. _`issue tracker`: https://github.com/visaplan/PACKAGE/issues

.. vim: tw=79 cc=+1 sw=4 sts=4 si et
