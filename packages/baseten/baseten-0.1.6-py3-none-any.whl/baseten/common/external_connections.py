import logging

from baseten.common import api
from baseten.common.core import raises_api_error

logger = logging.getLogger(__name__)


@raises_api_error
def add_external_connection(connection_id: str, connection_uri: str) -> dict:
    """Adds an external data source connection to the user account, which can be referred to by its connection_id in
    every workflow.

    Args:
        connection_id (str): A unique identifier for this connection. This ID will be used in the workflows
            to refer to this connection. Ex: 'prod_read_only_postgres_conn'
        connection_uri (str): Ex: 'postgresql://user:password@1.1.1.1:5432/postgresdb?optional_param=value'
    """
    return api.add_external_connection(connection_id, connection_uri)


@raises_api_error
def external_connections() -> dict:
    return api.external_connections()
