import json
import logging
import os
import pathlib
import tempfile
import time
from typing import Dict, List, Union

import h5py
import numpy as np
import pandas as pd
import requests
import yaml

from baseten.common import api
from baseten.common.core import (BASETEN_CONFIG_DIRECTORY,
                                 SampleDataInputShapeError, raises_api_error)
from baseten.common.explainer_config import \
    raises_invalid_explainer_configuration
from baseten.common.util import (coerce_data_as_numpy_array,
                                 generate_feature_transform_template,
                                 generate_output_transform_template)
from baseten.templates.model_template import model_template
from baseten.workflows import BasetenWorkflow

logger = logging.getLogger(__name__)

REQUIREMENTS_INSTALLATION_STATUS_RETRY_INTERVAL_SEC = 3
REQUIREMENTS_INSTALLATION_STATUS_MAX_TRIES = 20


def _build_h5_data_object(feature_data_np, target_data, metadata, data_temp_directory):
    data_temp_file = pathlib.PurePath(data_temp_directory, 'tmp.h5')
    data = {'features': feature_data_np}
    if np.any(target_data):
        data['targets'] = coerce_data_as_numpy_array(target_data)
    if np.any(metadata):
        data['metadata'] = json.dumps(metadata)

    h5_data = h5py.File(data_temp_file, mode='w')
    h5_sample_data_group = h5_data.create_group('sample_data')
    for key, np_obj in data.items():
        if key == 'metadata':
            dt = h5py.string_dtype(encoding='utf-8')
            h5_sample_data_group.create_dataset(key, data=np_obj, dtype=dt)
        else:
            h5_sample_data_group.create_dataset(key, data=np_obj)
    h5_data.close()
    return data_temp_file


@raises_api_error
def install_requirements(req_filepath: str):
    with open(req_filepath, 'r') as fp:
        requirements_txt = fp.read()
    logger.info(f'🚀 Sending requirements to BaseTen 🚀')
    resp = api.install_requirements(requirements_txt)
    status = resp['status']
    if status == 'PROCESSING':
        logger.info('🐳 Requirements are being installed 🐳')

        requirement_id = resp['id']
        tries = 0
        while tries < REQUIREMENTS_INSTALLATION_STATUS_MAX_TRIES:
            time.sleep(REQUIREMENTS_INSTALLATION_STATUS_RETRY_INTERVAL_SEC)
            resp = api.requirement_status(requirement_id)
            status = resp['status']
            if status != 'PROCESSING':
                break
            tries += 1
        else:
            logger.info('⌛ Requirements are still being installed. Check the status by running '
                        f'baseten.requirements_status(\'{requirement_id}\') ⌛')
    if status == 'SUCCEEDED':
        logger.info('🖖 Installed requirements successfully 🖖')
    elif status == 'FAILED':
        error_message = resp['error_message']
        logger.info(f'⚠️ Failed to install requirements. Error: "{error_message}" ⚠️')


@raises_api_error
def requirements_status(requirement_id: str):
    return api.requirement_status(requirement_id)


class BasetenDeployedExplainer:
    def __init__(self, explainer_version_id: str):
        self._explainer_version_id = explainer_version_id

    @raises_api_error
    def explain(self,
                inputs: Union[List, pd.DataFrame, np.ndarray],
                metadata: Union[pd.DataFrame, List[Dict]] = None) -> List[List]:
        if isinstance(inputs, pd.DataFrame):
            inputs_list = inputs.to_dict('records')
        elif isinstance(inputs, (list, np.ndarray)):
            inputs_np_array = np.array(inputs)
            inputs_list = inputs_np_array.tolist()
        else:
            raise TypeError('predict can be called with either a list, a pandas DataFrame, or a numpy array.')

        if isinstance(metadata, pd.DataFrame):
            metadata = metadata.to_dict(orient='records')

        return api.explain_for_version(self._explainer_version_id, inputs_list, metadata)


class BasetenDeployedModel:
    """A model backed by baseten serving. Provide either the model_id or the model_version_id."""
    def __init__(self, model_id: str = None,
                 model_version_id: str = None,
                 model_name: str = None):
        if not model_id and not model_version_id:
            raise ValueError('Either model_id or model_version_id must be provided.')

        if model_id and model_version_id:
            raise ValueError('Must provide either model_id or model_version_id; not both.')

        self._model_id = model_id
        self._model_version_id = model_version_id
        self._model_name = model_name
        self._model_config = None

    @property
    def model_version_id(self):
        return self._model_version_id

    @raises_api_error
    def predict(self,
                inputs: Union[List, pd.DataFrame, np.ndarray],
                metadata: Union[pd.DataFrame, List[Dict]] = None) -> List[List]:
        """Invokes the model given the input dataframe.

        Args:
            inputs: The data representing one or more inputs to call the model with.
                Accepted types are: list, pandas.DataFrame, and numpy.ndarray
            metadata (Union[pd.DataFrame, List[Dict]]): Metadata key/value pairs (e.g. name, url), one for each input.

        Returns:
            A list of inferences for each given input; e.g.: [[3], [9]] would indicate the prediction for the
            first input in inputs_df is [3], and the prediction for the second is [9].

        Raises:
            TypeError: If the provided inputs is not of a supported type.
            ApiError: If there was an error communicating with the server.
        """
        if isinstance(inputs, pd.DataFrame):
            inputs_list = inputs.to_dict('records')
        elif isinstance(inputs, (list, np.ndarray)):
            inputs_np_array = np.array(inputs)
            inputs_list = inputs_np_array.tolist()
        else:
            raise TypeError('predict can be called with either a list, a pandas DataFrame, or a numpy array.')

        if isinstance(metadata, pd.DataFrame):
            metadata = metadata.to_dict(orient='records')

        if self._model_version_id:
            return api.predict_for_model_version(self._model_version_id, inputs_list, metadata)
        return api.predict_for_model(self._model_id, inputs_list, metadata)

    @raises_api_error
    def update_model_config(self, model_config_file_path: str):
        """Update the model's feature names and output class labels (if any) based on the config
        found at `model_config_file_path`

        Args:
            model_config_file_path (str): The path to the model config file
        """
        config_yaml = yaml.safe_load(open(model_config_file_path, 'r'))
        feature_names = list(config_yaml['model_features']['features'])
        class_labels = config_yaml.get('model_class_labels', [])
        api.update_model_config(self._model_version_id, feature_names, class_labels)

    @raises_api_error
    def create_data_transform(self, model_config_path: str, transform_name: str):
        """Create a new data transform.

        Args:
            model_config_path (str): The path of this model's config folder
            transform_name (str)
        """
        transform_python_file_path = f'{model_config_path}/{transform_name}.py'
        transform_config_file_path = f'{model_config_path}/{transform_name}_config.yml'
        transform_view_file_path = f'{model_config_path}/{transform_name}_view.yml'
        transform_code = open(transform_python_file_path, 'r').read()
        transform_config = yaml.safe_load(open(transform_config_file_path, 'r'))
        if os.path.exists(transform_view_file_path):
            view_config = yaml.safe_load(open(transform_view_file_path, 'r'))
        else:
            view_config = {}
        transformation_data = {'code': transform_code, 'config': transform_config}
        # TODO validations
        return api.create_data_transform(self._model_version_id, transformation_data, view_config)

    @raises_api_error
    def create_workflow(self, workflow_name: str, workflow_yaml_filepath: str) -> BasetenWorkflow:
        """Create a workflow.
        Args:
            workflow_name (str): The name of the new workflow.
            workflow_yaml_filepath (str): The workflow yaml file path.

        Returns:
            BasetenWorkflow: A BasetenWorkflow instance.
        """
        with open(workflow_yaml_filepath, 'r') as config_file:
            workflow_config = config_file.read()
        response = api.create_workflow(self._model_version_id, workflow_name, workflow_config)
        workflow = BasetenWorkflow(
            workflow_id=response['id'],
            workflow_version_id=response['workflow_versions'][0]['id'],  # The workflow version ID that was just created
            workflow_name=response['name'])
        return workflow

    @raises_api_error
    def transform_data(self, data_transform_id: str, input_data: Dict) -> Dict:
        """Invokes the transform and returns a dict with transformed data and some metadata.

        Args:
            data_transform_id (str)
            input_data (Dict):  Data to be transformed.

        Returns:
            A dict with keys: 'success' (required) and 'transform_invocation_id', 'transform_output', 'error' (optional)
        """
        return api.transform_data(data_transform_id, input_data)

    def generate_feature_transform_template(self, transform_name: str, input_names: List[str], input_types: List[str]):
        return generate_feature_transform_template(model_version_id=self.model_version_id,
                                                   transform_name=transform_name,
                                                   input_names=input_names,
                                                   input_types=input_types)

    def generate_output_transform_template(self, transform_name: str):
        return generate_output_transform_template(model_version_id=self.model_version_id,
                                                  transform_name=transform_name)

    @raises_api_error
    def update_transform_view(self, data_transform_id: str, transform_view_config_file_path: str):
        """Update the transform's view config based on the config file found at `transform_view_file_path`

        Args:
            data_transform_id (str)
            transform_view_config_file_path (str): The path to the transform view config
                file. e.g: './baseten_model_configs/models/2vq0y3d/my_awesome_transform_view.yml'
        """
        view_config = yaml.safe_load(open(transform_view_config_file_path, 'r'))
        return api.update_transform_view(data_transform_id, view_config)

    @raises_api_error
    def set_primary(self):
        """Promote this version of the model as the primary version.
        Raises:
            ApiError: If there was an error communicating with the server.
        """
        if not self._model_version_id:
            raise ValueError('Only a BasetenDeployedModel backed by a model_version can be set as primary.')
        return api.set_primary(self._model_version_id)

    @raises_api_error
    def upload_sample_data(self,
                           feature_data: Union[np.ndarray, pd.DataFrame, List[List]],
                           target_data: Union[np.ndarray, pd.DataFrame, List] = None,
                           metadata: List[Dict] = None,
                           data_name: str = 'validation_data',
                           ) -> Dict:
        """Upload a subset of the training/validation data to be used for
            - Summary statistics for the model
            - To detect model drift
            - To use as baseline data for model interpretability
            - To seed new data in the client.

        Training and validation data with targets must be uploaded with the targets separate.

        Args:
            feature_data (Union[np.ndarray, pd.DataFrame, List[List]]): The feature data to upload.
            target_data (Union[np.ndarray, pd.DataFrame, List[List]]): The target data to upload.
            metadata (List[Dict]): Metadata key/value pairs for the dataset.
            data_name (str): The name of the data set.

        Returns:
            Dict: The status of the upload.
        """

        feature_data_np = coerce_data_as_numpy_array(feature_data)
        self.validate_feature_data_shape(feature_data_np)

        signed_s3_upload_post = api.signed_s3_upload_post(self.model_version_id, data_name)
        logger.debug(f'Signed s3 upload post:\n{json.dumps(signed_s3_upload_post, indent=4)}')

        with tempfile.TemporaryDirectory() as data_temp_directory:
            data_temp_file = _build_h5_data_object(feature_data_np, target_data, metadata, data_temp_directory)
            files = {'file': (f'{data_name}.h5', open(data_temp_file, 'rb'))}
            form_fields = signed_s3_upload_post['form_fields']
            form_fields['AWSAccessKeyId'] = form_fields.pop('aws_access_key_id')
            s3_key = form_fields['key']
            requests.post(signed_s3_upload_post['url'], data=form_fields, files=files)
        return api.register_data_for_model(s3_key, self.model_version_id, data_name)

    def deploy_explainer(self,
                         explainer_name: str,
                         feature_data: Union[np.ndarray, pd.DataFrame, List[List]] = None,
                         target_data: Union[np.ndarray, pd.DataFrame, List] = None,
                         metadata: List[Dict] = None,
                         data_name: str = 'explainer_background_data.h5',
                         custom_explainer_file: str = None,
                         custom_requirements_file: str = None,
                         ) -> Dict:
        """Deploy an explainer for the model.

        Args:
            explainer_name (str): What type of explainer to deploy. Options include 'ShapTreeExplainer',
                'ShapLinearExplainer', 'ShapKernelExplainer', 'AlibiAnchorTabular', 'AlibiCounterFactual',
                'CustomExplainer'.
            feature_data (Union[np.ndarray, pd.DataFrame, List[List]], optional):
                Background data used by the explainer. Defaults to None.
            target_data (Union[np.ndarray, pd.DataFrame, List], optional):
                Targets for the background feature data. Defaults to None.
            metadata (List[Dict], optional): Optional metadata for the explainer. Defaults to None.
            data_name (str, optional): Name for background data. Defaults to 'explainer_background_data.h5'.
            custom_explainer_file (str, optional): If explainer_name is CustomExplainer, the user
                must provide the path to the file which implements the CustomExplainer class.
                Defaults to None.
            custom_requirements_file (str, optional): Path to requirements.txt file for non built-in
                requirements for the CustomExplainer, eg, scikit-learn, tensorflow, SHAP, etc.
                Defaults to None.
        """
        raises_invalid_explainer_configuration(
            explainer_name,
            self.model_config['model'].get('model_framework', ''),
            self.model_config['model'].get('model_type', ''),
            feature_data,
            self.model_config['model_features'].get('feature_names', ''),
            custom_explainer_file,
        )

        if feature_data is not None:
            feature_data_np = coerce_data_as_numpy_array(feature_data)
            self.validate_feature_data_shape(feature_data_np)
        else:
            feature_data_np = np.array([])

        if custom_explainer_file:
            with open(custom_explainer_file, 'r') as f:
                explainer_definition = f.read()
        else:
            explainer_definition = ''

        if custom_requirements_file:
            with open(custom_requirements_file, 'r') as f:
                requirements_txt = f.read()
        else:
            requirements_txt = ''

        signed_s3_upload_post = api.signed_s3_upload_post(self.model_version_id, data_name)
        logger.debug(f'Signed s3 upload post:\n{json.dumps(signed_s3_upload_post, indent=4)}')

        with tempfile.TemporaryDirectory() as data_temp_directory:
            data_temp_file = _build_h5_data_object(feature_data_np, target_data, metadata, data_temp_directory)
            files = {'file': (f'{data_name}.h5', open(data_temp_file, 'rb'))}
            form_fields = signed_s3_upload_post['form_fields']
            form_fields['AWSAccessKeyId'] = form_fields.pop('aws_access_key_id')
            s3_key = form_fields['key']
            requests.post(signed_s3_upload_post['url'], data=form_fields, files=files)
        return BasetenDeployedExplainer(
            api.deploy_explainer(s3_key, self.model_version_id, data_name,
                                 explainer_name, explainer_definition, requirements_txt)['id'])

    def validate_feature_data_shape(self, feature_data: np.ndarray):
        feature_data_shape = self.feature_shape(feature_data)
        model_input_shape = api.model_version_input_shape(self.model_version_id)
        if model_input_shape != feature_data_shape:
            raise SampleDataInputShapeError(f'The model has shape {model_input_shape}'
                                            f' but {feature_data_shape} provided for sample data.')

    def feature_shape(self, feature_data: np.ndarray) -> List:
        return list(feature_data.shape)[1:]

    @property
    def _model_config_path(self):
        return f'{BASETEN_CONFIG_DIRECTORY}/{self.model_version_id}/'

    @property
    def _model_config_file(self):
        return f'{self._model_config_path}model_config.yml'

    @property
    def model_config(self):
        if self._model_config is None:
            try:
                with open(self._model_config_file, 'r') as f:
                    self._model_config = yaml.safe_load(f)
            except Exception as e:
                logger.error(f'Unable to load model config for model_version_id {self.model_version_id} due to {e}')
                self._model_config = {}
        return self._model_config

    def generate_model_template(self,
                                model_type: str = None,
                                model_framework: str = None,
                                feature_names: List[str] = None,
                                class_labels: List[str] = None,
                                input_type: str = 'structured_data'):
        # TODO: validations
        data = {
            'model_type': model_type,
            'model_framework': model_framework,
            'input_type': input_type,
            'feature_names': feature_names or [],
            'class_labels': class_labels or []
        }

        if not os.path.exists(self._model_config_path):
            os.makedirs(self._model_config_path)
        with open(self._model_config_file, 'w') as f:
            f.writelines(model_template.render(data))
        return self._model_config_path
