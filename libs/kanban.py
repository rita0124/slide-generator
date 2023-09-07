import asana
import configparser
from asana.rest import ApiException

def get_workspaces():
    # Configure OAuth2 access token for authorization: oauth2
    configuration = asana.Configuration()
    config = configparser.ConfigParser()
    config.read('config.ini')
    configuration.access_token = config['Asana']['asana_token']
    api_client = asana.ApiClient(configuration)

    # create an instance of the API class
    api_instance = asana.WorkspacesApi(api_client)

    try:
        # Get multiple workspaces
        api_response = api_instance.get_workspaces()
        return api_response
    except ApiException as e:
        print("Exception when calling WorkspacesApi->get_workspaces: %s\n" % e)
