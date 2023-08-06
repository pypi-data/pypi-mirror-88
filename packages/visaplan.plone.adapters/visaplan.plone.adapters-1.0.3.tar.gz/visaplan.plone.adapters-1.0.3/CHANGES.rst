Changelog
=========


1.0.3 (2020-12-16)
------------------

Improvements:

- Dependencies on proprietary adapters removed

New Features:

- Installable script `parseuserlog`

[tobiasherp]


1.0.2 (2020-08-12)
------------------

New Features:

- Python 3 support, using six_ (python-modernize)

Improvements:

- `userlog` and `grouplog` adapters group HTTP-related information together:

  - `ip`, usually meaning the IP address of the client;
  - `hostname`, usually meaning the hostname of the server
    (since there may be more than one)

[tobiasherp]


1.0.1 (2019-01-29)
------------------

- Tools updates

- Bugfix: No generation of ``configure.zcml`` files tried anymore
  in production setups
  (using ``visaplan.plone.tools.zcmlgen.SubpackageGenerator``)

[tobiasherp]


1.0 (2018-09-19)
----------------

Initial release.

[tobiasherp]

.. _six: https://pypi.org/project/six
