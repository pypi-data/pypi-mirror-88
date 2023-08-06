import base64
import inspect
from typing import Callable

from baseten.workflow.atom import RegisteredAtom
from baseten.workflow.lambda_source import get_lambda_source


class SendSlackMessage(RegisteredAtom):
    def __init__(self, webhook_url: str, format: str, task_name: str = 'Send Slack Message'):
        super().__init__('baseten.send_slack_message',
                         task_name,
                         {
                             'webhook_url': webhook_url,
                             'format': format,
                         })


class InvokeModel(RegisteredAtom):
    def __init__(self, model_id: str, task_name: str = 'Invoke Model'):
        super().__init__('baseten.invoke_model',
                         task_name,
                         {
                             'model_id': model_id,
                         })


class ExecuteQuery(RegisteredAtom):
    def __init__(self, query_name: str, task_name: str = 'Execute Query'):
        super().__init__('baseten.execute_query',
                         task_name,
                         {
                             'query_name': query_name,
                         })


def _extract_params(python_callable: Callable):
    def annotation_to_string(annotation):
        if hasattr(annotation, '__name__'):
            return annotation.__name__
        return str(annotation)

    def param_dict(param: inspect.Parameter):
        default = param.default if param.default != inspect.Signature.empty else None
        return {
            'name': param.name,
            'default': default,
            'annotation': annotation_to_string(param.annotation),
            'kind': str(param.kind),
        }
    return [param_dict(p) for p in inspect.Signature.from_callable(python_callable).parameters.values()]


def _get_source_lines(python_callable: Callable):
    # TODO(pankaj) Tackle lambda code better, currently it picks up the entire source code line
    if inspect.isfunction(python_callable):
        if python_callable.__name__ == '<lambda>':
            return [get_lambda_source(python_callable)]
        return inspect.getsourcelines(python_callable)[0]
    return inspect.getsourcelines(type(python_callable))[0]


def _ser_obj(obj):
    import cloudpickle
    pickled = cloudpickle.dumps(obj)
    return base64.b64encode(pickled).decode('utf-8')


def _extract_callable_properties(python_callable: Callable):
    name = python_callable.__name__ if hasattr(python_callable, '__name__') else ''
    args_metadata = _extract_params(python_callable)
    source = [line[:-1] if line and line[-1] == '\n' else line
              for line in _get_source_lines(python_callable)]
    ser_code = _ser_obj(python_callable)
    return name, args_metadata, source, ser_code


class Py(RegisteredAtom):
    """Generate Atom from python callable."""
    _ATOM_NAME = 'baseten.py'

    def __init__(self,
                 python_callable: Callable,
                 expand_input_dict=True,
                 task_name='Execute Python Callable',
                 doc=None):
        if not callable(python_callable):
            raise ValueError('supplied python_callable is not a callable.')

        c_name, c_args_metadata, c_source, c_ser_code = _extract_callable_properties(python_callable)
        # TODO(pankaj) extract doc from callable python docstring
        doc = doc or ''
        conf = {
            'callable_name': c_name,
            'callable_args_metadata': c_args_metadata,
            'callable_source': c_source,
            'callable_encoded_serialized_code': c_ser_code,
            'callable_expand_input_dict': expand_input_dict,
            'doc': doc,
        }
        super().__init__(Py._ATOM_NAME, task_name, conf)


class Map(RegisteredAtom):
    """Transform input.

    Convenience method to ignore the context and transform just he input. Allows
    for lean inline transformation chaining.

    Example:
        Map(lambda _: 10) >> Map(lambda x: x * 2) >> Map(lambda x: print(x))
        Prints 20
    """

    _ATOM_NAME = 'baseten.map'

    def __init__(self,
                 python_callable: Callable,
                 expand_input_dict=False,
                 task_name='Map',
                 doc=None):
        if not callable(python_callable):
            raise ValueError('supplied python_callable is not a callable.')

        c_name, c_args_metadata, c_source, c_ser_code = _extract_callable_properties(python_callable)
        # TODO(pankaj) extract doc from callable python docstring
        doc = doc or ''
        conf = {
            'callable_name': c_name,
            'callable_args_metadata': c_args_metadata,
            'callable_source': c_source,
            'callable_encoded_serialized_code': c_ser_code,
            'callable_expand_input_dict': expand_input_dict,
            'doc': doc,
        }
        super().__init__(Map._ATOM_NAME, task_name, conf)
