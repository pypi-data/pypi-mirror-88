import base64
import copy
import json
import logging
import os
from typing import List, Union

import numpy as np
import pandas as pd
from colorama import Fore, Style

from baseten.common import core
from baseten.templates.transform_template import (
    feature_transform_config_template, feature_transform_python_template,
    output_transform_config_template, output_transform_python_template,
    transform_view_template)

TRANSFORM_INPUT_TYPE_TO_PYTHON_TYPE = {
    'categorical': 'str',
    'float': 'float',
    'int': 'int',
    'text': 'str',
    'image': 'bytes',
    'url': 'str'
}

# list from https://scikit-learn.org/stable/developers/advanced_installation.html
SKLEARN_REQ_MODULE_NAME = {
    'numpy',
    'scipy',
    'joblib',
    'scikit-learn',
    'threadpoolctl',
}

# list from https://www.tensorflow.org/install/pip
# if problematic, lets look to https://www.tensorflow.org/install/source
TENSORFLOW_REQ_MODULE_NAME = {
    'tensorflow',
}


LOG_COLORS = {
    logging.ERROR: Fore.RED,
    logging.DEBUG: Fore.MAGENTA,
    logging.WARNING: Fore.YELLOW,
    logging.INFO: Fore.GREEN,
}


class ColorFormatter(logging.Formatter):
    def format(self, record, *args, **kwargs):
        new_record = copy.copy(record)
        if new_record.levelno in LOG_COLORS:
            new_record.levelname = "{color_begin}{level}{color_end}".format(
                level=new_record.levelname,
                color_begin=LOG_COLORS[new_record.levelno],
                color_end=Style.RESET_ALL,
            )
        return super(ColorFormatter, self).format(new_record, *args, **kwargs)


def setup_logger(package_name, level):
    baseten_logger = logging.getLogger(package_name)
    baseten_logger.setLevel(level)
    handler = logging.StreamHandler()
    formatter = ColorFormatter(fmt='%(levelname)s %(message)s')
    handler.setFormatter(formatter)
    if baseten_logger.hasHandlers():
        baseten_logger.handlers.clear()
    baseten_logger.addHandler(handler)


def generate_feature_transform_template(model_version_id: str,
                                        transform_name: str,
                                        input_names: List[str],
                                        input_types: List[str]):
    """Creates boilerplate code and config for the transform.

    Args:
        model_version_id(str)
        transform_name (str): Name given to the new transform; e.g 'my_awesome_feature_transform'
        input_names (List[str]): The names of the transform's input keys
        input_types (List[str]): The types of the transform's input keys (must be
            in TRANSFORM_INPUT_TYPE_TO_PYTHON_TYPE)
    """
    if not input_names:
        raise ValueError('Input names and input types must be 1 to 1')
    if input_types and (len(input_names) != len(input_types)):
        raise ValueError('Input names and input types must be 1 to 1')
    elif input_names and not input_types:
        # TODO attempt to infer types somewhere else (eg from training data)
        input_types = ['float' for _ in input_names]
    if not _validate_input_types(input_types):
        raise ValueError(f'Types must be one of {list(TRANSFORM_INPUT_TYPE_TO_PYTHON_TYPE.keys())}')
    input_data = [(x, y) for x, y in zip(input_names, input_types)]
    data = {
        'transform_name': transform_name,
        'input_data': input_data
    }

    path = _config_path_for_model_version(model_version_id)
    with open(f'{path}{transform_name}_config.yml', 'w') as f:
        f.writelines(feature_transform_config_template.render(data))
    with open(f'{path}{transform_name}_view.yml', 'w') as f:
        f.writelines(transform_view_template.render(data))
    with open(f'{path}{transform_name}.py', 'w') as f:
        f.writelines(feature_transform_python_template.render({'input_data': input_data}))
    return path


def generate_output_transform_template(model_version_id: str, transform_name: str):
    """Creates boilerplate code and config for the output transform.

    Args:
        model_version_id(str)
        transform_name (str): Name given to the new transform; e.g 'my_awesome_model_output_transform'
    """
    path = _config_path_for_model_version(model_version_id)
    with open(f'{path}{transform_name}_config.yml', 'w') as f:
        f.writelines(output_transform_config_template.render({'transform_name': transform_name}))
    with open(f'{path}{transform_name}.py', 'w') as f:
        f.writelines(output_transform_python_template.render())
    return path


def coerce_data_as_numpy_array(data: Union[np.ndarray, pd.DataFrame, List]) -> np.ndarray:
    """Validates that data can be coerced into a numpy array

    Args:
        data (Union[np.ndarray, pd.DataFrame, List]): The data to be transformed.

    Raises:
        TypeError: If data is wrong type.

    Returns:
        np.ndarray: A numpy array of data.
    """
    if not isinstance(data, (np.ndarray, pd.DataFrame, list)):
        raise TypeError(f'Data must be one of type [np.ndarray, pd.DataFrame, list], got {type(data)}')
    return np.array(data)


def base64_encoded_json_str(obj):
    return base64.b64encode(str.encode(json.dumps(obj))).decode('utf-8')


def _config_path_for_model_version(model_version_id: str) -> str:
    path = f'{core.BASETEN_CONFIG_DIRECTORY}/{model_version_id}/'
    if not os.path.exists(path):
        os.makedirs(path)
    return path


def _validate_input_types(input_types):
    return all([input_type in TRANSFORM_INPUT_TYPE_TO_PYTHON_TYPE.keys() for input_type in input_types])


def zipdir(path, zip_handler):
    for root, dirs, files in os.walk(path):
        relative_root = ''.join(root.split(path))
        for _file in files:
            zip_handler.write(
                os.path.join(root, _file), os.path.join(f'model{relative_root}', _file))


def print_error_response(response):
    print(Fore.YELLOW + f'{response["message"]}')
    print('---------------------------------------------------------------------------')
    print(Fore.GREEN + 'Stack Trace:')
    if 'exception' in response:
        excp = response['exception']
        for excp_st_line in excp['stack_trace']:
            print(Fore.GREEN + '---->' + Fore.WHITE + f'{excp_st_line}')
        print(Fore.RED + f'Exception: {excp["message"]}')


def pip_freeze():
    """
    This spawns a subprocess to do a pip freeze programmatically. pip is generally not supported as an API or threadsafe

    Returns: The result of a `pip freeze`

    """
    stream = os.popen('pip freeze -qq')
    this_env_requirements = [line.strip() for line in stream.readlines()]

    return this_env_requirements


def _get_entries_for_packages(list_of_requirements, desired_requirements):
    name_to_req_str = {}
    for req_name in desired_requirements:
        for full_req_str in list_of_requirements:
            if req_name == full_req_str.split('==')[0]:
                name_to_req_str[req_name] = full_req_str
    return name_to_req_str


def infer_sklearn_packages():
    return _get_entries_for_packages(pip_freeze(), SKLEARN_REQ_MODULE_NAME)


def infer_tensorflow_packages():
    return _get_entries_for_packages(pip_freeze(), TENSORFLOW_REQ_MODULE_NAME)
