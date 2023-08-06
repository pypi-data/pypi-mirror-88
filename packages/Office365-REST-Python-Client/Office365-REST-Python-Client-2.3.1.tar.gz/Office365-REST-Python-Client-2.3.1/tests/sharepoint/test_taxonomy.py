from office365.sharepoint.fields.field import Field
from office365.sharepoint.taxonomy.taxonomy_field import TaxonomyField
from office365.sharepoint.taxonomy.taxonomy_service import TaxonomyService
from office365.sharepoint.taxonomy.term import Term
from office365.sharepoint.taxonomy.term_set import TermSet
from office365.sharepoint.taxonomy.term_store import TermStore
from office365.sharepoint.taxonomy.term_group import TermGroup
from tests.sharepoint.sharepoint_case import SPTestCase


class TestSPTaxonomy(SPTestCase):
    target_field = None  # type: Field
    tax_svc = None  # type: TaxonomyService
    target_term_group = None  # type: TermGroup
    target_term_set = None  # type: TermSet

    @classmethod
    def setUpClass(cls):
        super(TestSPTaxonomy, cls).setUpClass()
        cls.tax_svc = TaxonomyService(cls.client)

    @classmethod
    def tearDownClass(cls):
        pass

    def test1_get_term_store(self):
        term_store = self.tax_svc.term_store.get().execute_query()
        self.assertIsInstance(term_store, TermStore)
        self.assertIsNotNone(term_store.name)

    def test2_get_term_groups(self):
        term_groups = self.tax_svc.term_store.term_groups.filter("name eq 'Geography'").get().execute_query()
        self.assertGreater(len(term_groups), 0)
        self.assertIsInstance(term_groups[0], TermGroup)
        self.__class__.target_term_group = term_groups[0]

    def test3_get_term_sets(self):
        term_sets = self.__class__.target_term_group.term_sets.get().execute_query()
        self.assertGreater(len(term_sets), 0)
        self.assertIsInstance(term_sets[0], TermSet)
        self.__class__.target_term_set = term_sets[0]

    def test4_get_terms(self):
        terms = self.__class__.target_term_set.terms.get().execute_query()
        self.assertGreater(len(terms), 0)
        self.assertIsInstance(terms[0], Term)

    # def test5_search_term(self):
    #    result = self.tax_svc.term_store.search_term("Finland", self.__class__.target_term_set.properties.get('id'))
    #    self.tax_svc.execute_query()
    #    self.assertIsNotNone(result)

    def test6_create_list_tax_field(self):
        ssp_id = "f02be691-d551-462f-aaae-e1c89168cd0b"
        term_set_id = "b49f64b3-4722-4336-9a5c-56c326b344d4"
        text_field_id = "cd790052-00e3-4317-a090-365cd85795b6"
        # list_id = "b9b8e2ef-6f9a-400b-a218-6a4899ea0121"
        # web_id = "cd5c86f3-261c-4d3a-8a91-34d6392cdfb9"
        tax_field = self.client.web.default_document_library().fields \
            .create_taxonomy_field(name="Category",
                                   ssp_id=ssp_id,
                                   term_set_id=term_set_id,
                                   text_field_id=text_field_id).execute_query()
        self.assertIsNotNone(tax_field.resource_path)
        self.__class__.target_field = tax_field

    def test7_get_tax_field(self):
        existing_field = self.__class__.target_field.get().execute_query()
        self.assertTrue(existing_field.properties.get('TypeAsString'), 'TaxonomyFieldType')
        self.assertIsInstance(existing_field, TaxonomyField)
        self.assertIsNotNone(existing_field.properties.get('TextField'))
        self.assertIsNotNone(existing_field.properties.get('LookupList'))
        self.assertIsNotNone(existing_field.properties.get('LookupWebId'))

        text_field_id = existing_field.properties.get('TextField')
        text_field = self.client.web.default_document_library().fields.get_by_id(text_field_id)
        self.client.load(text_field)
        self.client.execute_batch()
        self.assertIsNotNone(text_field.internal_name)

    def test8_delete_tax_field(self):
        self.__class__.target_field.delete_object().execute_query()

        # text_field_id = self.__class__.target_field.properties.get('TextField')
        # text_field = self.client.web.default_document_library().fields.get_by_id(text_field_id)
        # self.assertIsNotNone(text_field.resource_path)
