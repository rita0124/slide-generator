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
        # create an instance of the API class
        self.client = asana.ApiClient(configuration)
        self.workspaces = None
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

    def get_all(self):
        self.get_workspaces()
        # self.get_projects()
        # self.get_tasks()