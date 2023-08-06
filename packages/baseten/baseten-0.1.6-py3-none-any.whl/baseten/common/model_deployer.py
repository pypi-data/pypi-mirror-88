import copy
import json
import logging
import re
import tempfile
import zipfile
from functools import reduce
from typing import IO, Any, Callable, List, Optional, Tuple

import joblib
import requests
from colorama import Fore, Style

import baseten
from baseten.baseten_deployed_model import BasetenDeployedModel
from baseten.common import api
from baseten.common.core import (FrameworkNotSupportedError,
                                 ModelInputShapeError, ModelNotSupportedError,
                                 raises_api_error)
from baseten.common.settings import API_URL_BASE, SKLEARN, TENSORFLOW
from baseten.common.util import (infer_sklearn_packages,
                                 infer_tensorflow_packages, zipdir)

logger = logging.getLogger(__name__)


@raises_api_error
def deploy_model(serialized_model: IO[Any],
                 model_framework: str,
                 model_name: str = None,
                 model_type: str = None,
                 input_shape: List[int] = None,
                 feature_names: List[str] = None,
                 feature_summary: dict = None,
                 class_labels: List[str] = None,
                 model_framework_req: List[str] = None) -> BasetenDeployedModel:
    """Create a model version based on the serialized_model. If baseten wasn't initialized with a model_id, then
    create a model first and then create the model version.

    Args:
        serialized_model (file): A file-like object that is the serialized representation of the model object.
        model_framework (str): The framework used to create the model.
        model_name (str, optional): The name of the model to be created, if necessary.
        model_type (str, optional): The type of the model to be created.
        input_shape (List[int], optional): The shape of the model's input; e.g: [10] for a model with 10 features;
            [28, 28] for a model with 2 input dimensions of size 28 each.
        feature_names (list, optional): The list of feature names.
        feature_summary (dict, optional): A dict of summary stats with feature names as keys.
        class_labels (List[str], optional): The list of target class labels, if applicable.
        model_framework_req (List[str], optional): The model_framework specific requirements
    Returns:
        BasetenDeployedModel

    Raises:
        ApiError: If there was an error communicating with the server.
    """
    if not input_shape:
        input_shape = []
    if not feature_summary:
        feature_summary = {}
    if not class_labels:
        class_labels = []
    if not model_framework_req:
        model_framework_req = {}

    model_info = _exists_model(model_name, baseten.working_model_id, api.models)
    if not model_info:
        # Create a new model
        logger.info(f'Making contact with BaseTen 👋 👽')
        model_json = api.create_model(model_name)
        logger.debug(f'Created model:\n{json.dumps(model_json, indent=4)}')
        logger.info(f'Successfully registered model {Fore.BLUE}{model_name}{Style.RESET_ALL}.')
        model_id = model_json['id']
    else:
        model_id, model_name = model_info
        logger.info(f"Model '{model_name}' found. Uploading a new version.")

    baseten.working_model_id = model_id

    # Upload the model
    file_ext = _model_ext_from_framework(model_framework)
    model_key = _upload_model(serialized_model, file_ext)
    # Create the model version
    logger.info(f'{Fore.BLUE}Deploying model version.')
    model_version_json = api.create_model_version(model_id,
                                                  model_key,
                                                  model_framework,
                                                  model_type,
                                                  input_shape,
                                                  feature_names,
                                                  feature_summary,
                                                  class_labels,
                                                  model_framework_req)
    model_version_id = model_version_json['id']
    model_version_web_url = f'{API_URL_BASE}/models/{model_id}/versions/{model_version_id}'
    logger.debug(f'Created model version:\n{json.dumps(model_version_json, indent=4)}')
    logger.info(f'🏁 The model is being deployed right now 🏁')

    visit_message = f'|  Visit {Fore.BLUE}{model_version_web_url}{Style.RESET_ALL} for deployment status  |'
    visit_message_len = len(visit_message) - len(Fore.BLUE) - len(Style.RESET_ALL)
    logger.info(''.join(['-' for _ in range(visit_message_len)]))
    logger.info(visit_message)
    logger.info(''.join(['-' for _ in range(visit_message_len)]))

    return BasetenDeployedModel(model_version_id=model_version_id, model_name=model_name)


def _exists_model(model_name: Optional[str],
                  working_model_id: Optional[str],
                  models_provider: Callable) -> Optional[Tuple[str, str]]:
    """Checks if an effective model exists for the purpose of deploy or one needs to be created.

    If model name is supplied and a model with that name exists then it's picked up. Otherwise
    working model id in the session is tried.

    Returns id of model if model exists, or None
    """
    models = models_provider()['models']
    model_id_by_name = {model['name']: model['id'] for model in models}
    model_name_by_id = {model['id']: model['name'] for model in models}

    if model_name:
        if model_name in model_id_by_name:
            return model_id_by_name[model_name], model_name
        else:
            return None

    # No model_name supplied, try to work with working model id
    if working_model_id:
        if working_model_id in model_name_by_id:
            return working_model_id, model_name_by_id[working_model_id]
        else:
            logger.warning(f'Working model id not found in deployed models')
            return None

    # No model name or working model
    return None


@raises_api_error
def deploy_model_object(
    model: Any,
    model_name: str = None,
    feature_names: List[str] = None,
    class_labels: List[str] = None
) -> BasetenDeployedModel:
    """Create a model version based on the model. If baseten wasn't initialized with a model_id, then
    create a model first and then create the model version.

    Args:
        model (an in-memory model object): A model object to be deployed (e.g. a RandomForestClassifier object)
        model_name (str, optional): The name of the model to be created, if necessary.
        feature_names (List[str], optional): The list of feature names. If not provided,
            a list of feature names that match the model's input dimensions will be automatically generated.
            If the model's input has multiple dimensions, feature_names should be a flattened list of names.
        class_labels (List[str], optional): The list of target class labels, if applicable.
    Returns:
        BasetenDeployedModel

    Raises:
        FrameworkNotSupportedError: If the model framework used is not supported.
        ModelInputShapeError: feature_names does not match the model's signature.
        ApiError: If there was an error communicating with the server.
    """
    if hasattr(model, 'baseten'):
        model = copy.deepcopy(model)
        del model.baseten
    logger.info(f'🤖 Extracting 🤖 model 🤖 metadata 🤖')
    model_class = model.__class__
    model_framework, _, _ = model_class.__module__.partition('.')
    model_type = model_class.__name__
    input_shape = _model_input_shape(model, model_framework)
    logger.info(f'Preparing {Fore.BLUE}{model_framework} - {model_type}{Style.RESET_ALL} model.')

    if feature_names:
        input_features_count = reduce(lambda x, y: x * y, input_shape)
        if len(feature_names) != input_features_count:
            raise ModelInputShapeError(f'The model has {input_features_count} features but feature_names provided '
                                       f'{len(feature_names)}')

    if model_framework == SKLEARN:
        logger.info(f'Serializing {Fore.BLUE}{model_name}{Style.RESET_ALL}.')
        serialized_model = _serialize_sklearn_model(model)
        model_framework_req = infer_sklearn_packages()
        deployed_model = deploy_model(serialized_model,
                                      model_framework,
                                      model_name,
                                      model_type,
                                      input_shape,
                                      feature_names=feature_names,
                                      class_labels=class_labels,
                                      model_framework_req=model_framework_req)
        serialized_model.close()
    elif model_framework == TENSORFLOW:
        logger.info(f'Serializing {Fore.BLUE}{model_name}{Style.RESET_ALL}.')
        serialized_model = _serialize_tf_model(model)
        model_framework_req = infer_tensorflow_packages()
        deployed_model = deploy_model(serialized_model,
                                      model_framework,
                                      model_name,
                                      model_type,
                                      input_shape,
                                      feature_names=feature_names,
                                      class_labels=class_labels,
                                      model_framework_req=model_framework_req)
        serialized_model.close()
    else:
        raise FrameworkNotSupportedError(f'Models derived from {model_framework} are not currently supported.')

    if deployed_model:
        deployed_model.generate_model_template(
            model_type,
            model_framework,
            feature_names
        )
    return deployed_model


def _upload_model(serialized_model: IO, file_ext: str) -> str:
    """Uploads the serialized model to the appropriate environment

    Args:
        serialized_model (file): A file-like object that is the serialized representation of the model object.
        file_ext (str): The file extension for the saved model

    Returns:
        str: The key for the uploaded model

    Raises:
        RequestException: If there was an error communicating with the server.
    """

    model_file_name = f'model.{file_ext}'
    signed_s3_upload_post = api.signed_s3_upload_post(baseten.working_model_id, model_file_name)
    logger.debug(f'Signed s3 upload post:\n{json.dumps(signed_s3_upload_post, indent=4)}')

    # Upload the serialized model to S3
    files = {'file': (model_file_name, serialized_model)}
    form_fields = signed_s3_upload_post['form_fields']
    form_fields['AWSAccessKeyId'] = form_fields.pop('aws_access_key_id')  # S3 expects key name AWSAccessKeyId
    logger.info(f'🚀 Uploading model to BaseTen 🚀')
    resp = requests.post(signed_s3_upload_post['url'], data=form_fields, files=files)
    resp.raise_for_status()
    logger.info(f'🖖 Upload success! 🖖')

    logger.debug(f'File upload HTTP status code: {resp.status_code} and content:\n{resp.content}')

    return signed_s3_upload_post['form_fields']['key']


def _serialize_sklearn_model(model: Any) -> tempfile.SpooledTemporaryFile:
    """Serializes a model based on the scikit-learn framework.

    Args:
        model (Any): The model object.

    Returns:
        tempfile.SpooledTemporaryFile: A temporary file wrapper.
    """
    model_joblib = tempfile.TemporaryFile()
    joblib.dump(model, model_joblib, compress=True)
    model_joblib.seek(0)
    return model_joblib


def _serialize_tf_model(model: Any) -> tempfile.NamedTemporaryFile:
    """Serializes a Tensorflow model as a zipped SavedModel.

    Args:
        model (Any): The model object.

    Returns:
        tempfile.NamedTemporaryFile: A temporary zipfile.ZipFile wrapper.
    """
    temp_model_dir = tempfile.TemporaryDirectory()
    temp_file = tempfile.NamedTemporaryFile(suffix='.zip')
    model.save(temp_model_dir.name)
    zip_file = zipfile.ZipFile(temp_file.name, 'w', zipfile.ZIP_DEFLATED)
    zipdir(temp_model_dir.name, zip_file)
    zip_file.close()
    temp_model_dir.cleanup()
    temp_file.file.seek(0)
    return temp_file


def _model_ext_from_framework(model_framework: str) -> str:
    if model_framework == SKLEARN:
        return 'joblib'
    elif model_framework == TENSORFLOW:
        return 'zip'
    else:
        raise FrameworkNotSupportedError(f'Models derived from {model_framework} are not currently supported.')


def _model_input_shape(model, framework: str) -> List[int]:
    """Returns the shape of the model's input as an array; e.g: [10] for a model with 10 features; [28, 28] for a
    model with 2 input dimensions of size 28 each.
    """
    if framework == SKLEARN:
        n_features = _hack_n_features_from_sklearn_model(model)
        if n_features is None:
            return []
        return [n_features]
    elif framework == TENSORFLOW:
        input_shape = model.input_shape
        if isinstance(input_shape, list):
            raise ModelNotSupportedError("Baseten currently supports only single input models.")
        return list(input_shape[1:])  # The first dimension is None (batch size)
    else:
        raise FrameworkNotSupportedError(f'Models derived from {framework} are not currently supported.')


def _hack_n_features_from_sklearn_model(model) -> int:
    """Determines the size of the input for the given model.

    Due to inconsistent representation of feature inputs in sklearn, various methods/props
    are required to extract the input dimension based on the model type. It's a hack.

    Args:
        model: A sklearn model object.

    Returns:
        int: The number of features used to train the model.
    """
    if 'sklearn.neighbors' in str(model.__class__):
        return model._tree.data.shape[-1]
    if 'sklearn.naive_bayes.GaussianNB' in str(model.__class__):
        return model.theta_.shape[-1]
    if model.__module__ == 'sklearn.naive_bayes':
        return model.feature_log_prob_.shape[-1]
    if model.__module__ == 'sklearn.discriminant_analysis':
        return model.means_.shape[-1]
    if 'sklearn.gaussian_process' in model.__module__:
        return model.base_estimator_.X_train_.shape[-1]
    try:
        model.predict([[1]])
        n_features = 1
    except ValueError as e:
        # For many models (not the ones above), the correct input feature length is raised in the exception
        numbers = re.findall(r' (\d+)', str(e))
        n_features = [int(x) for x in numbers if x != '1'][-1]
    except Exception as e:
        logger.debug(f'Unable to determine input_shape because of: {e}, but not stopping 🤞')
        # we can't determine the input shape, but we don't want to stop the user from uploading
        n_features = None
    return n_features
