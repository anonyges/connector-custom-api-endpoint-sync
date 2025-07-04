from connectors.core.connector import Connector
from connectors.core.connector import get_logger, ConnectorError
from django.utils.module_loading import import_string
from .constants import LOGGER_NAME
from .custom_connector import CustomConnector

logger = get_logger(LOGGER_NAME)


class BaseConnector(Connector):
    """FortiSOAR Playbook calls this class first. Normmaly it calls the execute, check_health."""

    def execute(self, config: dict, operation: str, params: dict, *args, **kwargs):
        """When an operation(action) is triggered, it calls this function to trigger an operation.

        Args:
            config (dict): configuration fields given by user.
            operation (str): operation(action) which the user calls in string, must match info.json operation field.
            params (dict): paremeters that the user gives in the action

        Returns:
            returns (dict, str): Advanced user always returns in json string or dict(json). Try to return as json.dumps(dict).
        """
        return supported_operations.get(operation)(config, params)

    def check_health(self, config: dict=None, *args, **kwargs):
        """Check health is called when the new configuration is saved.

        Args:
            config (dict, optional): configuration fields given by user. Defaults to None.

        Returns:
            (dict, str): When returned in string, it prompts the value to user.
        """
        # To give error on the check_health you can trigger exception with below code.
        # raise ConnectionError("this is an error!")
        return check_health(config, *args, **kwargs)


def check_health(config: dict, params: dict = None):
    conn = CustomConnector()
    return conn.check_health(config, params)


def custom_api_endpoint_sync_call(config: dict, params: dict):
    conn = CustomConnector()
    return conn.custom_api_endpoint_sync_call(config, params)


supported_operations = {
    "check_health": check_health,
    "custom_api_endpoint_sync_call": custom_api_endpoint_sync_call,
}
