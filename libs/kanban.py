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
        self.users = None
        self.my_tasks = None
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
            self.projects = {}
            for d in data:
                self.projects[d['gid']] = d['name']
        except ApiException as e:
            print("Exception when calling ProjectsApi->get_projects_in_team: %s\n" % e)

    def get_users_in_team(self, team_gid=None):
        try:
            # create an instance of the API class
            api_instance = asana.UsersApi(self.client)
            if team_gid is None:
                team_gid = self.default['my_team_gid']
            # Get multiple users
            api_response = api_instance.get_users_for_team(team_gid)
            data = api_response.to_dict()['data']
            self.users = {}
            for d in data:
                self.users[d['gid']] = d['name']
        except ApiException as e:
            print("Exception when calling UsersApi->get_users_in_team: %s\n" % e)

    def get_tasks_in_project(self, project_gid=None):
        try:
            # create an instance of the API class
            api_instance = asana.TasksApi(self.client)
            if project_gid is None:
                project_gid = self.default['my_project_gid']
            # Get multiple tasks
            api_response = api_instance.get_tasks_for_project(project_gid)
            data = api_response.to_dict()['data']
            self.tasks = {}
            for d in data:
                self.tasks[d['gid']] = d['name']
        except ApiException as e:
            print("Exception when calling TasksApi->get_tasks_in_project: %s\n" % e)

    def get_tasks_in_project_details(self, assignee_gid, project_gid=None):
        try:
            # create an instance of the API class
            api_instance = asana.TasksApi(self.client)
            if project_gid is None:
                project_gid = self.default['my_project_gid']
            # if assignee_gid is None:
            #     assignee_gid = self.default['my_user_gid']
            # Get multiple tasks
            opt_fields = ["approval_status","assignee","assignee.name","start_on","due_on","name","completed","completed_at"]
            api_response = api_instance.get_tasks_for_project(project_gid, opt_fields=opt_fields)
            data = api_response.to_dict()['data']
            self.my_tasks = {}
            for d in data:
                if d['assignee'] is None:
                    self.my_tasks[d['gid']] = {'name': '無名氏'}
                elif d['assignee']['gid'] == assignee_gid:
                    self.my_tasks[d['gid']] = d
        except ApiException as e:
            print("Exception when calling TasksApi->get_tasks_in_project: %s\n" % e)

    def clear_empty_dict(self, origin_dict):
        to_delete = []
        for key in list(origin_dict.keys()):
            if key == 'assignee':   # not to clean 無名氏's
                continue
            elif origin_dict[key] is None:
                to_delete.append(key)
        for td in to_delete:
            del origin_dict[td]

    def clean_empty_values_in_my_tasks(self):
        for k, v in self.my_tasks.items():
            self.clear_empty_dict(self.my_tasks[k])

    def get_all(self):
        self.get_workspaces()
        self.get_teams_in_workspace()
        self.get_projects_in_team()
        self.get_tasks_in_project()
        # self.get_tasks_in_project_details()
        # self.clean_empty_values_in_my_tasks()