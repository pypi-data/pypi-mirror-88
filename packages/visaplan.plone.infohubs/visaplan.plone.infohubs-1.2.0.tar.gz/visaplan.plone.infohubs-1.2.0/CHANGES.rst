Changelog
=========


1.2.0 (2020-12-16)
------------------

New Features:

- ``@@infohubs-demo`` view to allow interactive tests;
  info keys and their values are listed in resolution order.

  With visaplan.tools_ >= v1.3.1, the ``keys`` input field will take
  multiple keys to demonstrate.

- info key `my_translation`: a proxy to get the appropriate language version
  for an object given by `path` or `uid`

Improvements:

- If visaplan.zope.reldb_ is installed, the ``hub['sqlwrapper']``
  will use its wrapper for an SQLAlchemy_ -based database connection

Hard dependencies removed:

+------------------------------+----------------------------------------+
| Package                      | Depending features                     |
+==============================+========================================+
| visaplan.plone.groups_       | - ``info['group_title']``              |
|                              | - ``info['gid']`` (group id)           |
|                              | - ``info['managed_group_title']``      |
|                              | - ``info['is_member_of'](`group`)``    |
+------------------------------+----------------------------------------+
| visaplan.plone.tools_        | - ``info['session']``                  |
|                              | - ``info['gid']`` (group id)           |
+------------------------------+----------------------------------------+
| visaplan.plone.pdfexport     | - ``info['PDFCreator']``               |
+------------------------------+----------------------------------------+
| visaplan.zope.reldb_ *or*    | - ``hub['sqlwrapper']``                |
| visaplan.plone.sqlwrapper_   |                                        |
+------------------------------+----------------------------------------+
| visaplan.plone.unitracctool  | - ``info['desktop_brain']``            |
|                              | - ``info['desktop_url']``              |
|                              | - ``info['bracket_default']``          |
+------------------------------+----------------------------------------+

Requirements:

- If visaplan.zope.reldb_ is not installed
  but visaplan.plone.sqlwrapper_ *is*, the latter must be >= v1.0.3.
  
  If visaplan.zope.reldb_ *is* installed, we don't care whether or not
  visaplan.plone.sqlwrapper_ is installed as well, and which version.

[tobiasherp]


1.1.0 (2020-07-15)
------------------

New Features:

- info key `my_translation`: a proxy to get the appropriate language version
  for an object given by `path` or `uid`

[tobiasherp]


1.0.2 (2019-05-09)
------------------

- convenience function ``context_tuple``,
  e.g. for methods with optional ``hub`` and ``info`` arguments

- Explicitly raise TypeErrors instead of using assertions
  (``context_and_form_tuple``, ``context_tuple``)

- New info keys ``counter`` and ``counters``

[tobiasherp]


1.0.1 (2019-01-31)
------------------

- ``info['my_uid']`` uses ``plone.uuid.interfaces.IUUID`` directly
  [tobiasherp]


1.0 (2018-09-17)
-----------------

- Initial release.
  [tobiasherp]

.. _SQLAlchemy: https://pypi.org/project/SQLAlchemy
.. _visaplan.plone.groups: https://pypi.org/project/visaplan.plone.groups
.. _visaplan.plone.sqlwrapper: https://pypi.org/project/visaplan.plone.sqlwrapper
.. _visaplan.plone.tools: https://pypi.org/project/visaplan.plone.tools
.. _visaplan.tools: https://pypi.org/project/visaplan.tools
.. _visaplan.zope.reldb: https://pypi.org/project/visaplan.zope.reldb
