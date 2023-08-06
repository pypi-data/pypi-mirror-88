import os
from pathlib import Path

SKLEARN = 'sklearn'
TENSORFLOW = 'tensorflow'

DEBUG = False
CONFIG_FILE_PATH = f'{Path.home()}/.baseten_config'


def _api_url_base() -> str:
    try:
        with open(CONFIG_FILE_PATH) as config_file:
            server_url = config_file.read().strip().rstrip('/')
            if server_url:
                return server_url
    except IOError:
        pass
    baseten_cli_env = os.environ.get('BASETEN_ENV')
    if baseten_cli_env == 'production':
        return 'https://app.baseten.co'
    if baseten_cli_env == 'staging':
        return 'https://staging.app.baseten.co'
    return 'http://127.0.0.1:8000'


API_URL_BASE = _api_url_base()
