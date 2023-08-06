.. contents::

UI for sections of site configured with their own domain.

Overview
========
Those sections are named mini sites.

When a mini site is traversed, the request is marked with

``IInMinisite`` if the domain used is the mini site domain,

or

``IInPortal`` if the domain used is the portal domain.

The request is also decorated with a ``cpskin_minisite`` attribute
which holds an instance of ``cpskin.minisite.minisite.Minisite`` class.

The instance has the following attributes :

``main_portal_url``
  The url under which the portal is served.

``minisite_url``
  The url under which the section is served as a minisite.

``minisite_urls``
  The urls under which the section is served as a minisite. Use minisite_url OR minisite_urls (urls are separeted with coma)

``search_path``
  The location of the section, expressed as a path from the Zope root.

``is_in_minisite_mode``
  Is the current request served as minisite ?

``is_in_portal_mode``
  Is the current request served as portal ?


Configuration
=============

The mini sites are configured by placing files in directory named ``minisites`` inside the ``CLIENT_HOME`` directory.

The ``CLIENT_HOME`` directory is found inside the ``var`` directory in a
standard instance built with buildout recipe ``plone.recipe.zope2instance``.

Typically, the files must be saved in ``buildout_dir/var/instance/minisites``.

The configuration file is a INI-file format file. Each section is configured as
below::

    [/plone/folder/minisite]
    minisite_url = http://minisite/url
    portal_url = http://localhost


Where the section name is the minisite path from the Zope root.
The ``minisite_url`` holds the url with the specific domain under which the minisite
must be served.
The ``portal_url`` holds the url with the specific domain under which the
portal is served.
