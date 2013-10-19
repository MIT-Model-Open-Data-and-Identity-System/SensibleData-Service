import os

#Base directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

#Root directory of the project
ROOT_DIR = '/nowhere/SensibleData-Service/sensible_data_service/'

OPENID_SSO_SERVER_URL = 'https://nowhere/openid/xrds/'

ROOT_URL = '/sensible-dtu/'
BASE_URL = 'https://nowhere/sensible-dtu/'


#Databses
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'OPTIONS': {
            'read_default_file': os.path.join(BASE_DIR,'SECURE_my.cnf'),
        },
    }
}


PLATFORM = {
        "platform_uri": "https://54.229.13.160/sensible-data/",
        "platform_uri_token": "https://54.229.13.160/sensible-data/"+"oauth2/oauth2/token/",
        "redirect_uri": "https://54.229.13.160/sensible-dtu/"+"platform_api/redirect_uri/",
        "required_scopes": ["enroll"],
        "ip_addr": ["54.229.13.160"] #list of ip addresses of the platform authorized to make calls
}

DATA_DATABASE = {
    "backend":"mongodb",
    "params": {
        "url":"mongodb://%s:%s@ds035368.mongolab.com:35368/sensibledtu_1k_milosz",
        "database":"sensibledtu_1k_milosz"
        }
}

CONNECTORS = {
    "ConnectorFunf": True,
    "ConnectorQuestionnaire": True,
    "ConnectorFacebook": False,
}

SERVICE_NAME = "SensibleDTU-1k"
DATA_BASE_DIR = ""
DATA_LOG_DIR = DATA_BASE_DIR + "/log/"
