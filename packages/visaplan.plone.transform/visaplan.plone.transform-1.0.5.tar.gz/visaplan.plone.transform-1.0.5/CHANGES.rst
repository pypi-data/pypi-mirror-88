Changelog
=========


1.1 (unreleased)
----------------

- Support for `FolderishAnimation` (visaplan.plone.animations_)

[tobiasherp]


1.0.5 (2020-12-16)
------------------

Improvements:

- In ``configure.zcml``, don't  import "zcml-empty" packages anymore
- Support both Products.unitracc < 3.5 (with ``@@versioninformation`` browser)
  and >= 3.5 (where that browser was moved to the policy package)

[tobiasherp]


1.0.4 (2020-06-12)
------------------

Bugfixes:

- ``.utils.extract_2uids`` now recognizes ``@@resolveuid`` links as well

[tobiasherp]


1.0.3 (2019-12-18)
------------------

Improvements:

- Don't crash for image references with invalid UID parts (URL segment after ``resolveuid/``);
  styling requires visaplan.UnitraccResource v1.1.2+.

[tobiasherp]


1.0.2 (2019-02-14)
------------------

- Per-object delay during export of (possibly big) structures to allow for
  requests in other threads (to improve responsiveness)

[tobiasherp]


1.0.1 (2018-08-18)
------------------

- Bugfix for v1.0
  [tobiasherp]


1.0 (2018-08-18)
----------------

- Initial release.
  [tobiasherp]


.. _visaplan.plone.animations: https://pypi.org/project/visaplan.plone.animations
