import asana
import configparser
from asana.rest import ApiException


class Kanban():

    def __init__(self) -> None:

        # Configure OAuth2 access token for authorization: oauth2
        configuration = asana.Configuration()
        config = configparser.ConfigParser()
        config.read('config.ini')
        configuration.access_token = config['Asana']['asana_token']
        self.default = config['Default']
        # create an instance of the API class
        self.client = asana.ApiClient(configuration)
        self.workspaces = None
        self.teams = None
        self.projects = None
        self.tasks = None
        self.get_all()

    def get_workspaces(self):
        try:
            # create an instance of the API class
            api_instance = asana.WorkspacesApi(self.client)
            # Get multiple workspaces
            api_response = api_instance.get_workspaces()
            data = api_response.to_dict()['data']
            self.workspaces = [ d['gid'] for d in data ]
        except ApiException as e:
            print("Exception when calling WorkspacesApi->get_workspaces: %s\n" % e)

    def get_teams_in_workspace(self, workspace_gid=None):
        try:
            # create an instance of the API class
            api_instance = asana.TeamsApi(self.client)
            if workspace_gid is None:
                # workspace_gid = self.workspaces[0]
                workspace_gid = self.default['my_workspace_gid']
            # Get multiple teams
            api_response = api_instance.get_teams_for_workspace(workspace_gid)
            data = api_response.to_dict()['data']
            # self.teams = [ d['gid'] for d in data ]
            self.teams = {}
            for d in data:
                self.teams[d['gid']] = d['name']
        except ApiException as e:
            print("Exception when calling TeamsApi->get_teams_for_workspace: %s\n" % e)

    def get_projects_in_team(self, team_gid=None):
        try:
            # create an instance of the API class
            api_instance = asana.ProjectsApi(self.client)
            if team_gid is None:
                team_gid = self.default['my_team_gid']
            # Get multiple projects
            api_response = api_instance.get_projects_for_team(team_gid)
            data = api_response.to_dict()['data']
            # self.projects = [ d['gid'] for d in data ]
            self.projects = {}
            for d in data:
                self.projects[d['gid']] = d['name']
        except ApiException as e:
            print("Exception when calling ProjectsApi->get_projects_in_team: %s\n" % e)

    def get_all(self):
        self.get_workspaces()
        self.get_teams_in_workspace()
        self.get_projects_in_team()
        # self.get_tasks()