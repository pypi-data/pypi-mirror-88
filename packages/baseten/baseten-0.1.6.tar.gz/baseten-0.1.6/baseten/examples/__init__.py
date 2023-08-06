import importlib

BASETEN_PRETRAINED_MODELS = {  # Map model names to files where they are defined.
    'mnist_tensorflow': 'mnist'
}


def deploy_pretrained_model(model_name: str):
    if model_name not in BASETEN_PRETRAINED_MODELS:
        raise Exception(f'{model_name} is not available as a pretrained baseten model.')
    model_file = BASETEN_PRETRAINED_MODELS[model_name]
    module = importlib.import_module(f'baseten.examples.{model_file}')
    return module.deploy_pretrained_model()
