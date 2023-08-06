# -*- coding: utf-8 -*-
from cpskin.minisite import logger
from cpskin.minisite.event import MinisiteMarkedEvent
from cpskin.minisite.interfaces import IMinisiteRoot
from cpskin.minisite.minisite import MinisiteConfig
from plone import api
from transaction import commit
from zope.component import provideUtility
from zope.component.hooks import setSite
from zope.event import notify
from zope.interface import alsoProvides
from zope.interface import noLongerProvides

import ConfigParser
import os
import os.path
import Zope2


def registerMinisites(event):
    CLIENT_HOME = os.environ["CLIENT_HOME"]
    minisites_directory = os.path.join(CLIENT_HOME, "minisites")
    if os.path.exists(minisites_directory):
        registerMinisitesFromDirectory(minisites_directory)


def registerMinisitesFromDirectory(directory):
    files = os.listdir(directory)
    minisite_paths = []
    for filename in files:
        filename = os.path.join(directory, filename)
        if os.path.isfile(filename):
            minisite_paths.append(registerMinisitesFromFile(filename))
    markMinisites(minisite_paths)


def registerMinisitesFromFile(filename):
    config = ConfigParser.RawConfigParser()
    try:
        config.read(filename)
    except ConfigParser.MissingSectionHeaderError:
        return
    logger.debug("Register minisites from file {0}".format(filename))
    for section in config.sections():
        try:
            portal_url = config.get(section, "portal_url")
            minisite_url = config.get(section, "minisite_url")
            minisite = MinisiteConfig(
                main_portal_url=portal_url,
                minisite_url=minisite_url,
                search_path=section,
                filename=filename,
            )
            registerMinisite(minisite)
            return section
        except KeyError:
            continue


def markMinisites(minisite_paths):
    app = Zope2.app()
    if not minisite_paths:
        return
    # we suppose plone is in first level of zope
    portal_path = filter(None, minisite_paths[0].split("/"))[0]
    plonesite = app.get(portal_path)
    if not plonesite:
        return
    setSite(plonesite)
    # plone.api do not work here
    catalog = plonesite.portal_catalog
    brains = catalog({"object_provides": IMinisiteRoot.__identifier__})
    for brain in brains:
        obj = brain.getObject()
        noLongerProvides(obj, IMinisiteRoot)
        logger.debug("{0} unmark as minisite".format(obj.absolute_url()))

    for minisite_path in minisite_paths:
        try:
            minisite_root = api.content.get(minisite_path)
            docker_compose_hostname = os.environ.get("HOSTNAME") or ""
        except:  # noqa
            # if folder path is not publish
            minisite_root = None
        if (
            minisite_root
            and minisite_root.portal_type != "Link"
            and "instance1" in docker_compose_hostname
        ):
            alsoProvides(minisite_root, IMinisiteRoot)
            notify(MinisiteMarkedEvent(minisite_root))
            logger.debug("{0} folder mark as minisite".format(minisite_path))
            commit()


def registerMinisite(config):
    logger.debug(
        "Register minisite at {0} for {1}".format(
            config.main_portal_url, config.minisite_url
        )
    )
    provideUtility(config, name=config.search_path)


def registerMinisitesSetupHandler(context):

    # Ordinarily, GenericSetup handlers check for the existence of XML files.
    # Here, we are not parsing an XML file, but we use this text file as a
    # flag to check that we actually meant for this import step to be run.
    # The file is found in profiles/default.
    if context.readDataFile("register_cpskin_minisites.txt") is None:
        return
    from cpskin.minisite import tests

    filename = os.path.join(os.path.dirname(tests.__file__), "minisites_config.txt")

    registerMinisitesFromFile(filename)
