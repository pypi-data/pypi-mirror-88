from office365.runtime.resource_path_service_operation import ResourcePathServiceOperation
from office365.sharepoint.base_entity import BaseEntity


class ListTemplate(BaseEntity):

    def __init__(self, context, resource_path=None):
        """
        Represents a list definition or a list template, which defines the fields and views for a list.
            List definitions are contained in files within
            \\Program Files\\Common Files\\Microsoft Shared\\Web Server Extensions\\12\\TEMPLATE\\FEATURES,
            but list templates are created through the user interface or through the object model when a list is
            saved as a template.
            Use the Web.ListTemplates property (section 3.2.5.143.1.2.13) to return a ListTemplateCollection
            (section 3.2.5.92) for a site collection. Use an indexer to return a single list definition or
            list template from the collection.

        """
        super().__init__(context, resource_path)

    @property
    def internal_name(self):
        """Gets a value that specifies the identifier for the list template.
        :rtype: str or None
        """
        return self.properties.get('InternalName', None)

    def set_property(self, name, value, persist_changes=True):
        super(ListTemplate, self).set_property(name, value, persist_changes)
        if self._resource_path is None:
            if name == "Name":
                self._resource_path = ResourcePathServiceOperation(
                    "GetByName", [value], self._parent_collection.resource_path)
        return self
