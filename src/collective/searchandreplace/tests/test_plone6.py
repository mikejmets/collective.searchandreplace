"""Tests for the Plone 6 changes in 9.0.0: the preview table's Path column,
upgrade step 2003 (icons) and the control panel registration."""

from collective.searchandreplace.searchreplaceutility import make_catalog_query_args
from collective.searchandreplace.testing import SEARCH_REPLACE_INTEGRATION_LAYER
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from zope.interface import alsoProvides

import unittest

PROFILE = "collective.searchandreplace:default"


def path(obj):
    # Compare by path: each lookup returns a new acquisition wrapper.
    return "/".join(obj.getPhysicalPath())


CONFIGLET_ID = "collective.searchandreplace.searchreplacesettings"


class TestPathColumn(unittest.TestCase):
    """Which paths the preview table shows, and relative to what.

    A folder's default page searches the whole folder when "Search Subfolders" is
    on (make_catalog_query_args), so the table must then show paths relative to
    that folder.
    """

    layer = SEARCH_REPLACE_INTEGRATION_LAYER

    def setUp(self):
        self.portal = self.layer["portal"]
        self.request = self.layer["request"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])

    def table(self, context, subfolders):
        if subfolders:
            self.request.form["form.widgets.searchSubfolders"] = ["selected"]
        else:
            self.request.form.pop("form.widgets.searchSubfolders", None)
        # Imported here, not at module level: importing searchreplacetable
        # registers its content provider, which must happen inside the test
        # layer's component registry (as when ZCML loads it).
        from collective.searchandreplace.browser.searchreplacetable import (
            SearchReplaceTable,
        )

        # The table only reads the request here; the form view is not needed.
        return SearchReplaceTable(context, self.request, None)

    def search_path(self, context, subfolders):
        args = make_catalog_query_args(
            context=context,
            findWhat="Find",
            searchSubFolders=subfolders,
            onlySearchableText=False,
        )
        return args["path"]["query"]

    def assert_root_matches_search(self, context, subfolders):
        root = self.table(context, subfolders).search_root()
        self.assertEqual(path(root), self.search_path(context, subfolders))

    def test_default_page_with_subfolders_shows_site_paths(self):
        self.portal.invokeFactory("Document", "index_html")
        self.portal.invokeFactory("Folder", "essays")
        table = self.table(self.portal.index_html, subfolders=True)
        self.assertEqual(path(table.search_root()), path(self.portal))
        self.assertTrue(table.shows_paths())
        self.assertEqual(table.getRelativePath("/plone/essays/page"), "./essays/page")
        self.assert_root_matches_search(self.portal.index_html, True)

    def test_default_page_without_subfolders_hides_paths(self):
        self.portal.invokeFactory("Document", "index_html")
        table = self.table(self.portal.index_html, subfolders=False)
        self.assertEqual(path(table.search_root()), path(self.portal.index_html))
        self.assertFalse(table.shows_paths())
        self.assert_root_matches_search(self.portal.index_html, False)

    def test_folder_shows_paths(self):
        self.portal.invokeFactory("Folder", "essays")
        for subfolders in (True, False):
            table = self.table(self.portal.essays, subfolders)
            self.assertEqual(path(table.search_root()), path(self.portal.essays))
            self.assertTrue(table.shows_paths())
            self.assertEqual(table.getRelativePath("/plone/essays/page"), "./page")
            self.assertEqual(table.getRelativePath("/plone/essays"), "./")
            self.assert_root_matches_search(self.portal.essays, subfolders)

    def test_ordinary_page_hides_paths(self):
        self.portal.invokeFactory("Document", "doc1")
        for subfolders in (True, False):
            table = self.table(self.portal.doc1, subfolders)
            self.assertEqual(path(table.search_root()), path(self.portal.doc1))
            self.assertFalse(table.shows_paths())
            self.assert_root_matches_search(self.portal.doc1, subfolders)

    def test_folder_as_default_page_searches_itself(self):
        self.portal.invokeFactory("Folder", "index_html")
        table = self.table(self.portal.index_html, subfolders=True)
        self.assertEqual(path(table.search_root()), path(self.portal.index_html))
        self.assertTrue(table.shows_paths())
        self.assert_root_matches_search(self.portal.index_html, True)


class TestIcons(unittest.TestCase):
    """Plone 6 icons for the toolbar action and the control panel."""

    layer = SEARCH_REPLACE_INTEGRATION_LAYER

    def setUp(self):
        self.portal = self.layer["portal"]
        self.setup = self.portal.portal_setup
        setRoles(self.portal, TEST_USER_ID, ["Manager"])

    def action(self):
        return self.portal.portal_actions.object.search_and_replace

    def configlet(self):
        for configlet in self.portal.portal_controlpanel.listActions():
            if configlet.getId() == CONFIGLET_ID:
                return configlet
        self.fail("configlet not found")

    def test_install_has_icons_and_latest_version(self):
        self.assertEqual(self.setup.getLastVersionForProfile(PROFILE), ("2003",))
        self.assertEqual(self.action().icon_expr, "string:search")
        self.assertEqual(self.configlet().getIconExpression(), "string:search")

    def test_upgrade_2002_to_2003_sets_icons(self):
        # A site on 2002 has the Plone 4/5 icon settings.
        self.action()._setPropValue("icon_expr", "")
        self.configlet().setIconExpression("string:$portal_url/search_icon.png")
        self.setup.setLastVersionForProfile(PROFILE, "2002")

        self.setup.upgradeProfile(PROFILE)

        self.assertEqual(self.setup.getLastVersionForProfile(PROFILE), ("2003",))
        self.assertEqual(self.action().icon_expr, "string:search")
        self.assertEqual(self.configlet().getIconExpression(), "string:search")


class TestControlPanel(unittest.TestCase):
    """The control panel is registered for plone.base's IPloneSiteRoot."""

    layer = SEARCH_REPLACE_INTEGRATION_LAYER

    def setUp(self):
        self.portal = self.layer["portal"]
        self.request = self.layer["request"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])

    def test_control_panel_renders(self):
        from plone.app.z3cform.interfaces import IPloneFormLayer

        alsoProvides(self.request, IPloneFormLayer)
        view = self.portal.restrictedTraverse("@@searchreplace-controlpanel")
        html = view()
        self.assertIn("Search and Replace settings", html)
        self.assertIn("maximum_text_characters", html)
