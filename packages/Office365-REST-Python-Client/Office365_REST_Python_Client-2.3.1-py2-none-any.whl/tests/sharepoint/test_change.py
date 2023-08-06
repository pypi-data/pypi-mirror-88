from office365.sharepoint.changes.change_log_item_query import ChangeLogItemQuery
from tests.sharepoint.sharepoint_case import SPTestCase

from office365.sharepoint.changes.change_collection import ChangeCollection
from office365.sharepoint.changes.change_query import ChangeQuery


class TestChange(SPTestCase):

    def test_1_get_web_changes(self):
        changes = self.client.site.root_web.get_changes(query=ChangeQuery(web=True)).execute_query()
        self.assertIsInstance(changes, ChangeCollection)

    def test_2_get_site_changes(self):
        target_list = self.client.site.root_web.default_document_library()
        changes = target_list.get_changes(query=ChangeQuery(site=True)).execute_query()
        self.assertIsInstance(changes, ChangeCollection)

    #def test_3_get_list_item_changes_since_token(self):
    #    target_list = self.client.site.rootWeb.default_document_library()
    #    query = ChangeLogItemQuery(row_limit="100")
    #    result = target_list.get_list_item_changes_since_token(query)
    #    self.client.execute_query()
    #    self.assertIsNotNone(result.value)
