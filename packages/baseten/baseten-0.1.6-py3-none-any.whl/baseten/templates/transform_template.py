# flake8: noqa

from jinja2 import Template

feature_transform_python_template = Template("""
def transform_input(input_data):
    \"\"\"
    Transforms input dict of feature data into the model input as given by the input signature of the model.

    Args:
        input_data (Dict): a dict of input names to values
        {
{% for input_name, _ in input_data %}
                '{{ input_name }}': INPUT_VALUE,
{% endfor %}

        }
     Returns:
        A list of transformed values.
    \"\"\"
    # TODO: Your transform code goes here:
    return []
""", trim_blocks=True)

output_transform_python_template = Template("""
def transform_model_output(model_output_data):
    \"\"\"
    Transforms the output of the model into a human-understandable string.

    Args:
        model_output_data (Dict): The output of the model as a dict with keys:
            'prediction' (Union[float, List]): float or list depending on the model
            'probabilities' (List[float], optional)
            'explainability' (Dict, optional)
     Returns:
        A human-understandable string.
    \"\"\"
    # TODO: Your model output transform code goes here:
    return ''
""", trim_blocks=True)

feature_transform_config_template = Template(
"""transform_name: {{ transform_name }}
transform_type: feature_transform
transform_inputs:
{% for input_name, input_type in input_data %}
    - {{ input_name }}:
        type: {{ input_type }}
{% endfor %}""", trim_blocks=True)

output_transform_config_template = Template(
"""transform_name: {{ transform_name }}
transform_type: output_transform
""", trim_blocks=True)


transform_view_template = Template(
"""transform_name: {{ transform_name }}
transform_inputs:
{% for input_name, input_type in input_data %}
    - {{ input_name }}:
        display_name: {{ input_name }}
        type: {{ input_type }}
{% if input_type == 'categorical' %}
        categories: []
{% endif %}
{% if input_type == 'float' %}
        min: # optional minimum for float value
        max: # optional maximum for float value
{% endif %}
{% if input_type == 'int' %}
        min: # optional minimum for int value
        max: # optional maximum for int value
{% endif %}
{% endfor %}""", trim_blocks=True)
