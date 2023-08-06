Changelog
=========

1.1.8 (2020-12-09)
------------------

- WEB-3377: Fix traversing redirection where there are views / attributes in URL
  [laulaz]


1.1.7 (2020-09-25)
------------------

- WEB-3436: Also transform img src for content coming from portal
  [laulaz]

- Begin to fix tests, but I have to comment all of tests. I think there is an issue during initialisation of minisite.
  [bsuttor]


1.1.6 (2020-08-24)
------------------

- Fix bug when rss_feed_view is apply in minisite context.
  [boulch]


1.1.5 (2020-07-02)
------------------

- Fix problem with external url transformation : WEB-3375
  [laulaz]

- Add more improvements for i18n support
  [macagua]

- Avoid error when there is no HOSTNAME env variable
  [laulaz]


1.1.4 (2019-07-09)
------------------

- Tag minisite folders only on instance1 to avoid conflict error.
  [bsuttor]


1.1.3 (2019-04-24)
------------------

- Open links to portal in new window : WEB-3013
  [laulaz]


1.1.2 (2019-04-10)
------------------

- Add id to fix Diazo rules in several themes : WEB-2976
  [laulaz]


1.1.1 (2019-04-08)
------------------

- Breathcrumb in minisite mode has no more link to portal.
  [bsuttor]


1.1.0 (2019-03-20)
------------------

- Fix / improve herited content href transformation and redirection (WEBNAM-209)
  - herited content will be found event in the parents of a content with same id
  - language is now properly handled
  - href transformation works now also on specific areas outside of content-core
  and viewlet-below-content-body : just use parsable-content class
  - optimizations have been made
  [laulaz]


1.0.9 (2019-03-01)
------------------

- Remove collective.redirectacquired as it is no longer needed
  [laulaz]


1.0.8 (2019-02-11)
------------------

- Add new viewlet menu for dropdown : WEBOTT-9
  The viewlet is hidden for now
  [laulaz]

- Code cleanup
  [laulaz]

- Add event notification when marking a minisite
  [laulaz]


1.0.7 (2019-01-08)
------------------

- Do not try to change Unauthorized url.
  [bsuttor]


1.0.6 (2018-12-03)
------------------

- Remove /index_html from redirect urls.
  [bsuttor]

- Transform check if href is find.
  [bsuttor]


1.0.5 (2018-11-30)
------------------

- Check UnicodeEncodeError on transform url.
  [bsuttor]


1.0.4 (2018-11-30)
------------------

- Improve transform.
  [bsuttor]


1.0.3 (2018-11-29)
------------------

- Sometimes a tag has no href.
  [bsuttor]


1.0.2 (2018-11-29)
------------------

- Also check if minisite path is published on starting.
  [bsuttor]


1.0.1 (2018-11-28)
------------------

- Improve way to mark minisite on startup.
  [bsuttor]


1.0.0 (2018-11-28)
------------------

- Add transform to change a href link on content-core and viewlet-below-content-body div.
  [bsuttor]

- Redirect requests that use acquisition to access portal content from
  minisites.
  [laulaz]

- Remove IMinisiteRoot marker interface on uninstall.
  [bsuttor]

- sitemap.xml.gz view is now callable from minisites.
  [bsuttor]


0.5.5 (2018-06-06)
------------------

- Use collective.redirectacquired to block acquisition : #21570
  [laulaz]

- Improve minisites_panel view.
  [bsuttor]


0.5.4 (2018-05-16)
------------------

- Fix publishTraverse to work with plone.restapi.
  [bsuttor]


0.5.3 (2018-05-15)
------------------

- Minisite publishTraverse inherit of REST plublishTraverse to work with plone.restapi.
  [bsuttor]


0.5.2 (2018-04-19)
------------------

- Allow registration on minisite
  [mpeeters]


0.5.1 (2016-10-17)
------------------

- Ensure minisite actions are sorted correctly (position in parent folder)
  [laulaz]


0.5.0 (2016-08-17)
------------------

- Add local actions (in minisites) to minisite viewlet : content tagged with
  minisite-action hidden keyword appears there
  [laulaz]


0.4.0 (2016-08-09)
------------------

- Move CPSkin actions to a new dedicated menu
  [laulaz]

- Fix / improve tests interfering with footer sitemap content
  [laulaz]


0.3.4 (2015-12-01)
------------------

- Traverse also into plone.app.contenttypes folders.
  [bsuttor]


0.3.3 (2015-09-28)
------------------

- Add css class for home object.
  [bsuttor]


0.3.2 (2015-09-28)
------------------

- Add utils for getting minisite object.
  [bsuttor]


0.3.1 (2015-09-28)
------------------

- Minisite viewlet is also visible on portal.
  [bsuttor]


0.3.0 (2015-09-25)
------------------

- Add a viewlet with an horizontal menu for minisite.
  [bsuttor, cboulanger]


0.2.1 (2015-02-20)
------------------

- Add minisite_urls attribute.


0.2 (2014-08-21)
----------------

- Add minisite portlet on top of right column (affinitic #5859)


0.1 (2014-07-02)
----------------

- Initial release
