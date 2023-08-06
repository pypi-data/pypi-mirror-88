import functools
import json
import logging
from typing import Any, Dict, List

import keyring
import requests

from baseten.common import settings
from baseten.common.core import (KEYRING_SERVICE_NAME, ApiError,
                                 AuthorizationError, KEYRING_USERNAME)
from baseten.common.util import base64_encoded_json_str

logger = logging.getLogger(__name__)


def with_api_key(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        api_key = keyring.get_password(KEYRING_SERVICE_NAME, username=KEYRING_USERNAME)
        if not api_key:
            raise AuthorizationError('You must first run the `baseten login` cli command.')
        result = func(api_key, *args, **kwargs)
        return result
    return wrapper


@with_api_key
def models(api_key):
    query_string = '''
    {
      models {
        id,
        name
      }
    }
    '''

    resp = _post_graphql_query(api_key, query_string)
    return resp['data']


@with_api_key
def create_model(api_key, model_name):
    if not model_name:
        import coolname
        model_name = coolname.generate_slug(2)
    query_string = f'''
    mutation {{
      create_model(name: "{model_name}") {{
        id,
        name
      }}
    }}
    '''

    resp = _post_graphql_query(api_key, query_string)
    return resp['data']['create_model']


@with_api_key
def models_versions(api_key, model_id):
    query_string = f'''
    {{
      model(id: "{model_id}") {{
        versions {{
          id,
          s3_key,
          feature_names,
          feature_summary
        }}
      }}
    }}
    '''

    resp = _post_graphql_query(api_key, query_string)
    return resp['data']['model']


@with_api_key
def model_version_input_shape(api_key, model_version_id):
    query_string = f'''
    {{
      model_version(id: "{model_version_id}") {{
        input_shape
      }}
    }}
    '''

    resp = _post_graphql_query(api_key, query_string)
    return resp['data']['model_version']['input_shape']


@with_api_key
def create_model_version(api_key,
                         model_id,
                         s3_key,
                         model_framework,
                         model_type,
                         input_shape,
                         feature_names,
                         feature_summary,
                         class_labels,
                         model_framework_req):
    encoded_input_shape = base64_encoded_json_str(input_shape)
    encoded_feature_names = base64_encoded_json_str(feature_names)
    encoded_feature_summary = base64_encoded_json_str(feature_summary)
    encoded_class_labels = base64_encoded_json_str(class_labels)
    encoded_model_framework_req = base64_encoded_json_str(model_framework_req)
    query_string = f'''
    mutation {{
      create_model_version(model_id: "{model_id}",
                           s3_key: "{s3_key}",
                           model_framework: "{model_framework}",
                           model_type: "{model_type}",
                           encoded_input_shape: "{encoded_input_shape}",
                           encoded_feature_names: "{encoded_feature_names}",
                           encoded_feature_summary: "{encoded_feature_summary}",
                           encoded_class_labels: "{encoded_class_labels}",
                           encoded_model_framework_req: "{encoded_model_framework_req}") {{
        id,
        s3_key,
        feature_names,
        feature_summary
      }}
    }}
    '''

    resp = _post_graphql_query(api_key, query_string)
    return resp['data']['create_model_version']


@with_api_key
def create_data_transform(api_key, model_version_id, transformation_data, view_config):
    encoded_transformation_data = base64_encoded_json_str(transformation_data)
    encoded_view_config = base64_encoded_json_str(view_config)
    query_string = f'''
    mutation {{
      create_data_transform(model_version_id: "{model_version_id}",
                            encoded_transformation_data: "{encoded_transformation_data}",
                            encoded_view_config: "{encoded_view_config}") {{
        id
      }}
    }}
    '''

    resp = _post_graphql_query(api_key, query_string)
    return resp['data']['create_data_transform']


@with_api_key
def update_or_create_workflow(api_key, workflow_name, worklet_configs, query_configs):
    encoded_query_configs = base64_encoded_json_str(query_configs)
    encoded_worklet_configs = base64_encoded_json_str(worklet_configs)
    query_string = f'''
    mutation {{
      update_or_create_workflow(workflow_name: "{workflow_name}",
                                encoded_worklet_configs: "{encoded_worklet_configs}",
                                encoded_query_configs: "{encoded_query_configs}") {{
        id
        name
        worklets {{
            id
            name
        }}
        queries {{
            id
            name
        }}
      }}
    }}
    '''
    resp = _post_graphql_query(api_key, query_string)
    return resp['data']['update_or_create_workflow']


@with_api_key
def workflow(api_key, name):
    query_string = f'''
    {{
      workflow(name: "{name}") {{
        id
      }}
    }}
    '''

    resp = _post_graphql_query(api_key, query_string)
    return resp['data']['workflow']


@with_api_key
def update_workflow(api_key, workflow_id, workflow_name, worklet_configs, query_configs):
    encoded_worklet_configs = base64_encoded_json_str(worklet_configs)
    encoded_query_configs = base64_encoded_json_str(query_configs)
    query_string = f'''
    mutation {{
      update_workflow(workflow_id: "{workflow_id}",
                      name: "{workflow_name}",
                      encoded_worklet_configs: "{encoded_worklet_configs}",
                      encoded_query_configs: "{encoded_query_configs}") {{
        id
        name
        worklets {{
            id
            name
        }}
        queries {{
            id
            name
        }}
      }}
    }}
    '''
    resp = _post_graphql_query(api_key, query_string)
    return resp['data']['update_workflow']


@with_api_key
def create_workflow_action(api_key, workflow_id, action_name, workflow_action_config):
    encoded_workflow_action_data = base64_encoded_json_str(workflow_action_config)
    query_string = f'''
    mutation {{
      create_workflow_action(workflow_id: "{workflow_id}",
                      name: "{action_name}",
                      encoded_workflow_action_data: "{encoded_workflow_action_data}") {{
        id
      }}
    }}
    '''

    resp = _post_graphql_query(api_key, query_string)
    return resp['data']['create_workflow_action']


@with_api_key
def publish_workflow(api_key, workflow_version_id: str) -> Dict:
    query_string = f'''
    mutation {{
      publish_workflow_version(id: "{workflow_version_id}") {{
        id
      }}
    }}
    '''
    resp = _post_graphql_query(api_key, query_string)
    return resp['data']['publish_workflow_version']


@with_api_key
def transform_data(api_key, data_transform_id: str, input_data: Dict) -> Dict:
    predict_url = f'{settings.API_URL_BASE}/data_transforms/{data_transform_id}/invoke'
    resp = _post_rest_query(api_key, predict_url, {'input_data': input_data})
    resp.raise_for_status()
    return json.loads(resp.content)


@with_api_key
def update_transform_view(api_key, data_transform_id: str, view_config: Dict) -> Dict:
    encoded_view_config = base64_encoded_json_str(view_config)
    query_string = f'''
    mutation {{
      update_feature_transform_view(data_transform_id: "{data_transform_id}",
                                    encoded_view_config: "{encoded_view_config}") {{
        view_config
      }}
    }}
    '''

    resp = _post_graphql_query(api_key, query_string)
    return resp['data']['update_feature_transform_view']


@with_api_key
def signed_s3_upload_post(api_key, model_id, model_file_name):
    query_string = f'''
    {{
      signed_s3_upload_url(model_id: "{model_id}", model_file_name: "{model_file_name}") {{
        url,
        form_fields {{
          key,
          aws_access_key_id,
          policy,
          signature,
        }}
      }}
    }}
    '''

    resp = _post_graphql_query(api_key, query_string)
    return resp['data']['signed_s3_upload_url']


@with_api_key
def register_data_for_model(api_key, s3_key, model_version_id, data_name):
    query_string = f'''
    mutation {{
        create_sample_data_file(model_version_id: "{model_version_id}",
                                name: "{data_name}",
                                s3_key: "{s3_key}") {{
          id
        }}
    }}
    '''
    resp = _post_graphql_query(api_key, query_string)
    return resp['data']['create_sample_data_file']


@with_api_key
def deploy_explainer(api_key, s3_key, model_version_id, data_name,
                     explainer_name, explainer_definition, explainer_requirements):
    query_string = f'''
    mutation {{
        deploy_explainer(model_version_id: "{model_version_id}",
                                name: "{data_name}",
                                s3_key: "{s3_key}",
                                explainer_name: "{explainer_name}",
                                explainer_requirements: "{base64_encoded_json_str(explainer_requirements)}",
                                explainer_definition: "{base64_encoded_json_str(explainer_definition)}"),{{
          id
        }}
    }}
    '''
    resp = _post_graphql_query(api_key, query_string)
    return resp['data']['deploy_explainer']


@with_api_key
def predict_for_model(api_key, model_id: str, inputs: list, metadata: List[Dict] = None) -> List[List]:
    """Call the model's predict given the input json.

    Args:
        api_key (str)
        model_id (str)
        inputs (list)
        metadata (List[Dict]): Metadata key/value pairs (e.g. name, url), one for each input.

    Raises:
        RequestException: If there was an error communicating with the server.
    """
    predict_url = f'{settings.API_URL_BASE}/models/{model_id}/predict'
    return _predict(api_key, predict_url, inputs, metadata)


@with_api_key
def predict_for_model_version(api_key, model_version_id: str, inputs: list, metadata: List[Dict] = None) -> List[List]:
    """Call the model version's predict given the input json.

    Args:
        api_key (str)
        model_version_id (str)
        inputs (list)
        metadata (List[Dict]): Metadata key/value pairs (e.g. name, url), one for each input.

    Raises:
        RequestException: If there was an error communicating with the server.
    """
    predict_url = f'{settings.API_URL_BASE}/model_versions/{model_version_id}/predict'
    return _predict(api_key, predict_url, inputs, metadata)


@with_api_key
def explain_for_version(api_key, explainer_version_id: str, inputs: list, metadata: List[Dict] = None) -> List[List]:
    """Call the explainer version given the input json.

    Args:
        api_key (str)
        explainer_version_id (str)
        inputs (list)
        metadata (List[Dict]): Metadata key/value pairs (e.g. name, url), one for each input.

    Raises:
        RequestException: If there was an error communicating with the server.
    """
    explain_url = f'{settings.API_URL_BASE}/explainer_versions/{explainer_version_id}/explain'
    resp = _post_rest_query(api_key, explain_url, {'inputs': inputs, 'metadata': metadata})
    resp_json = json.loads(resp.content)
    return resp_json


@with_api_key
def set_primary(api_key, model_version_id: str):
    """Promote this version of the model as the primary version.

    Args:
        api_key (str)
        model_version_id (str)
    """
    query_string = f'''
    mutation {{
      update_model_version(model_version_id: "{model_version_id}", is_primary: true) {{
        id,
        is_primary,
      }}
    }}
    '''
    resp = _post_graphql_query(api_key, query_string)
    return resp['data']['update_model_version']


@with_api_key
def update_model_config(api_key, model_version_id: str, feature_names: list, class_labels: list = None):
    """Update the feature names for the model.

    Args:
        api_key (str)
        model_version_id (str)
        feature_names (list)
        class_labels (Optional[list]): applies only to classifiers.
    """
    encoded_feature_names = base64_encoded_json_str(feature_names)
    encoded_class_labels = base64_encoded_json_str(class_labels)
    query_string = f'''
    mutation {{
      update_model_version(model_version_id: "{model_version_id}",
                           encoded_feature_names: "{encoded_feature_names}",
                           encoded_class_labels: "{encoded_class_labels}") {{
        id,
        feature_names,
      }}
    }}
    '''
    resp = _post_graphql_query(api_key, query_string)
    return resp['data']['update_model_version']


@with_api_key
def invoke_worklet(api_key, workflow_id, worklet_name: str, inp, create_workflow_instance=False, dry_run=False):
    url = f'{settings.API_URL_BASE}/workflows/{workflow_id}/worklets/{worklet_name}/invoke'
    resp = _post_rest_query(api_key, url, {
        'worklet_input': inp,
        'dry_run': dry_run,
        'create_workflow_instance': create_workflow_instance,
    })
    resp_json = json.loads(resp.content)
    return resp_json


@with_api_key
def dryrun_atom(api_key, atom_name: str, atom_conf: dict, atom_input: Any, workflow_name: str):
    url = f'{settings.API_URL_BASE}/workflows/atom/run'
    resp = _post_rest_query(api_key, url, {
        'atom_name': atom_name,
        'atom_conf': atom_conf,
        'atom_input': atom_input,
        'workflow_name': workflow_name,
        'dry_run': True,
    })
    return json.loads(resp.content)


@with_api_key
def add_external_connection(api_key, connection_id, connection_uri):
    query_string = f'''
    mutation {{
      create_external_connection(connection_id: "{connection_id}",
                                 connection_uri: "{connection_uri}") {{
        connection_id
        connection_type
      }}
    }}
    '''
    resp = _post_graphql_query(api_key, query_string)
    return resp['data']['create_external_connection']


@with_api_key
def external_connections(api_key):
    query_string = f'''
    {{
      external_connections {{
        connection_id
        connection_type
      }}
    }}
    '''

    resp = _post_graphql_query(api_key, query_string)
    return resp['data']['external_connections']


@with_api_key
def install_requirements(api_key, requirements_txt):
    escaped_requirements_txt = requirements_txt.replace('\n', '\\n')  # Otherwise the mutation becomes invalid graphql.
    query_string = f'''
    mutation {{
      create_pynode_requirement(requirements_txt: "{escaped_requirements_txt}") {{
        id
        status
        error_message
      }}
    }}
    '''
    resp = _post_graphql_query(api_key, query_string)
    return resp['data']['create_pynode_requirement']


@with_api_key
def requirement_status(api_key, requirement_id):
    query_string = f'''
    {{
      pynode_requirement(id: "{requirement_id}") {{
        id
        status
        error_message
      }}
    }}
    '''

    resp = _post_graphql_query(api_key, query_string)
    return resp['data']['pynode_requirement']


def _predict(api_key, predict_url: str, inputs: list, metadata: List[Dict] = None) -> List[List]:
    resp = _post_rest_query(api_key, predict_url, {'inputs': inputs, 'metadata': metadata})
    resp_json = json.loads(resp.content)
    return resp_json['predictions']


def _headers(api_key):
    return {'Authorization': f'Api-Key {api_key}'}


def _post_graphql_query(api_key, query_string) -> dict:
    resp = requests.post(f'{settings.API_URL_BASE}/graphql/', data={'query': query_string}, headers=_headers(api_key))
    if not resp.ok:
        logger.error(f'GraphQL endpoint failed with error: {resp.content}')
        resp.raise_for_status()
    resp_dict = resp.json()
    errors = resp_dict.get('errors')
    if errors:
        raise ApiError(errors[0]['message'], resp)
    return resp_dict


def _post_rest_query(api_key, url, post_body_dict):
    resp = requests.post(url, json=post_body_dict, headers=_headers(api_key))
    resp.raise_for_status()
    return resp
