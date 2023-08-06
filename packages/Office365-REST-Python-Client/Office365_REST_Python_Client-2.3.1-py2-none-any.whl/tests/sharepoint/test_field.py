import uuid

from tests.sharepoint.sharepoint_case import SPTestCase

from office365.sharepoint.fields.field import Field
from office365.sharepoint.fields.field_creation_information import FieldCreationInformation
from office365.sharepoint.fields.field_text import FieldText
from office365.sharepoint.fields.field_type import FieldType


class TestField(SPTestCase):
    target_field = None   # type: Field
    target_field_name = "Title"

    def test_1_get_site_fields(self):
        site_fields = self.client.site.root_web.fields.get().execute_query()
        self.assertGreater(len(site_fields), 0)

    def test_2_get_field(self):
        title_field = self.client.site.root_web.fields.\
            get_by_internal_name_or_title(self.target_field_name).get().execute_query()
        self.assertIsNotNone(title_field.internal_name)
        self.assertEqual(title_field.internal_name, self.target_field_name)
        self.assertIsInstance(title_field, FieldText)
        self.assertIsNotNone(title_field.max_length)

    def test_3_get_field_by_title(self):
        title_field = self.client.site.root_web.fields.get_by_title(self.target_field_name).get().execute_query()
        self.assertIsNotNone(title_field.internal_name)
        self.assertEqual(title_field.internal_name, self.target_field_name)

    def test_4_create_site_field(self):
        field_name = "Title_" + uuid.uuid4().hex
        create_field_info = FieldCreationInformation(field_name, FieldType.Text)
        created_field = self.client.site.root_web.fields.add(create_field_info).execute_query()
        self.assertEqual(created_field.properties["Title"], field_name)
        self.__class__.target_field = created_field

    def test_5_update_site_field(self):
        field_to_update = self.__class__.target_field
        updated_field_name = "Title_" + uuid.uuid4().hex
        field_to_update.set_property('Title', updated_field_name).update().execute_query()

        updated_field = self.client.site.root_web.fields.get_by_title(updated_field_name).get().execute_query()
        self.assertIsNotNone(updated_field.id)
        self.assertEqual(updated_field.title, updated_field_name)

    def test_6_delete_site_field(self):
        field_to_delete = self.__class__.target_field
        field_to_delete.delete_object().execute_query()
