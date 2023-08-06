import logging

import yaml

from baseten.common import api
from baseten.common.core import raises_api_error

logger = logging.getLogger(__name__)


class BasetenWorkflow:
    """A workflow. Provide either the workflow_id or the workflow_version_id."""
    def __init__(self,
                 workflow_id: str,
                 workflow_version_id: str = None,
                 workflow_name: str = None):
        if not workflow_id and not workflow_version_id:
            raise ValueError(
                'Either workflow_id or workflow_version_id must be provided.')
        self._workflow_id = workflow_id
        self._workflow_version_id = workflow_version_id
        self._workflow_name = workflow_name

    @property
    def workflow_name(self):
        return self._workflow_name

    @property
    def workflow_version_id(self):
        return self._workflow_version_id

    @raises_api_error
    def create_workflow_action(self, action_name: str, action_code_path: str,
                               action_entrypoint: str):
        """Create an action.
        Args:
            action_name (str): The name of the action
            action_code_path (str): The path to the action's .py file.
            action_entrypoint (str): If action_code_path is a .py file, the name of the
                function which is the entrypoint for the action.
        Returns:
            [type]: [description]
        """
        config = {'entrypoint': action_entrypoint}
        action_code = open(action_code_path, 'r').read()
        action_data = {'code': action_code, 'config': config}
        return api.create_workflow_action(self._workflow_id, action_name, action_data)

    @raises_api_error
    def publish(self):
        """Publish the workflow.
        """
        return api.publish_workflow(self._workflow_version_id)

    @raises_api_error
    def update_workflow(self, workflow_yaml_filepath):
        """Update a workflow.
        Args:
            workflow_yaml_filepath (str): The workflow yaml file path.
        """
        workflow_config = yaml.safe_load(open(workflow_yaml_filepath, 'r'))
        resp = api.update_workflow(self._workflow_id, workflow_config)
        # Setting the version ID so that a future `publish` call publishes this new workflow version.
        self._workflow_version_id = resp['id']
        return resp
