from office365.directory.group_profile import GroupProfile
from office365.entity_collection import EntityCollection
from office365.runtime.client_result import ClientResult
from office365.runtime.resource_path import ResourcePath
from office365.teams.team import Team


class TeamCollection(EntityCollection):
    """Team's collection"""

    def __init__(self, context, resource_path=None):
        super(TeamCollection, self).__init__(context, Team, resource_path)

    def __getitem__(self, key):
        if type(key) == int:
            return self._data[key]
        return Team(self.context, ResourcePath(key, self.resource_path))

    def get(self):
        """
        :rtype: TeamCollection
        """
        return super(TeamCollection, self).get()

    def get_all(self):
        """List all teams in Microsoft Teams for an organization"""
        groups = self.context.groups.select(["id", "resourceProvisioningOptions"])
        self.context.load(groups)

        def _process_response(resp):
            for grp in groups:
                if "Team" in grp.properties["resourceProvisioningOptions"]:
                    new_team = Team(self.context, ResourcePath(grp.properties["id"], self.resource_path))
                    new_team.set_property("id", grp.properties["id"])
                    self.add_child(new_team)
        self.context.after_execute(_process_response)
        return self

    def create(self, group_name):
        """Provision a new team along with a group.

        :type group_name: str
        :rtype: ClientResult
        """

        grp_properties = GroupProfile(group_name)
        grp_properties.securityEnabled = False
        grp_properties.mailEnabled = True
        grp_properties.groupTypes = ["Unified"]
        target_group = self.context.groups.add(grp_properties)
        result = ClientResult(Team(self.context))

        def _group_created(resp):
            result.value = target_group.add_team()
        self.context.after_execute(_group_created)
        return result
