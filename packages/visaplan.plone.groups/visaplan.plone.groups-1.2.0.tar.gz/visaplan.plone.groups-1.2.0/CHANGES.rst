Changelog
=========


1.2.0 (2020-12-16)
------------------

Breaking changes:

- `crumbs` modules renamed to `oldcrumbs`

  (With zope.deprecation_ installed, imports will continue to work;
  a DeprecationWarning will be logged.)

Requirements removed:

- visaplan.plone.breadcrumbs_ (still supported; hard requirement removed)
- visaplan.plone.sqlwrapper_
  (An SQLWrapper class with that very functionality is alternatively implemented
  by the visaplan.zope.reldb_.legacy module)

Bugfixes:

- Don't include the (now) non-required packages in the configure.zcml anymore:

  - visaplan.plone.breadcrumbs_
  - visaplan.kitchen_

[tobiasherp]


1.1.6 (2020-08-20)
------------------

Miscellaneous:

- Python 3 compatibility, using six_

[tobiasherp]


1.1.5 (2020-08-03)
------------------

Bugfixes:

- Switch to group desktop via group selection didn't work.
- Access codes page now linked absolutely, and thus works now even if
  the desktop was loaded via AJAX.

[tobiasherp]


1.1.4 (2020-06-12)
------------------

New Features:

- On the desktop, list unbooked but accessable courses (e.g. demo courses, "for authenticated" / "for all")
  after the booked courses (and without statistics, of course).
  This is so far considered too tiny to rectify a "minor" version change.

Miscellaneous:

- Switched off the disfunctional personal calendar
  (more precisely: removed the section from the desktop)
  which crashed when clicked (#50)

[tobiasherp]


1.1.3 (2020-04-08)
------------------

Miscellaneous:

- Don't use the course titles for a link to the course anymore;
  we have "Start course" and "Continue course" for this purpose

[tobiasherp]


1.1.2 (2020-03-27)
------------------

Bugfix:

- ``group-desktop.pt`` now loads correctly via AJAX
  (including the DataTable; a minor layout problem remains)
- To `start` course via desktop link (rather than continueing),
  specify ``uid=1`` explicitly;
  this is currently necessary to make the AJAX load work.

[tobiasherp]


1.1.0.1 (2020-03-24)
--------------------

Miscellaneous:

- New SQL script ``src/visaplan/plone/groups/groupsharing/sql/update-0003.sql``:
  modifies the SQL view ``course_statistics_overview`` to always report
  ``course_view`` as the (last used) ``page_view_type``
  (to load that page via AJAX; #393)

[tobiasherp]


1.1.0 (2020-03-06)
------------------

New features:

- Views for AJAX navigation (registered if visaplan.plone.ajaxnavigation_ is installed)
- ``group-desktop`` views
  (for full-page and - not yet used with visaplan.plone.ajaxnavigation_ v1.0 -
  for AJAX loading;
  {my,our}-{images,...} views currently linked with data-fullpage-only attributes)

[tobiasherp]


1.0.2 (2019-05-13)
------------------

Bugfixes:

- Fixed incomplete conversion of Tomcom adapters usage to ``getToolByName``

[tobiasherp]


1.0.1 (2019-05-09)
------------------

Note: Due to a regression, please proceed to version 1.0.2!

- New functions ``utils.generate_{structure,course}_group_ids``,
  ``generate_structure_group_tuples``

- Support for option ``resolve_role`` for the following functions:

  - ``split_group_id``
  - ``generate_structure_group_tuples``

  With ``resolve_role=True``, these functions tell a role a role, and a
  suffix a suffix; e.g., the ``Author`` group of structures is not given the
  ``Author`` but the ``Editor`` local role.

  For now, the default value for ``resolve_role`` is *False*;
  this may change in future versions.


[tobiasherp]


1.0 (2018-09-19)
----------------

- Initial release.
  [tobiasherp]


.. _six: https://pypi.org/project/six
.. _visaplan.kitchen: https://pypi.org/project/visaplan.kitchen
.. _visaplan.pgquery: https://pypi.org/project/visaplan.pgquery
.. _visaplan.plone.ajaxnavigation: https://pypi.org/project/visaplan.plone.ajaxnavigation
.. _visaplan.plone.breadcrumbs: https://pypi.org/project/visaplan.plone.breadcrumbs
.. _visaplan.plone.sqlwrapper: https://pypi.org/project/visaplan.plone.sqlwrapper
.. _visaplan.zope.reldb: https://pypi.org/project/visaplan.zope.reldb
.. _zope.deprecation: https://pypi.org/project/zope.deprecation
