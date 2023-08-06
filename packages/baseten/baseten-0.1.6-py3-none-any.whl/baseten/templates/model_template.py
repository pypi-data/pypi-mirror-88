from jinja2 import Template

model_template = Template(
    """
model:
{% if model_type %}
    model_type: {{ model_type }}
{% endif %}
{% if model_framework %}
    model_framework: {{ model_framework }}
{% endif %}
model_features:
    input_type: {{ input_type }}
    features:
{% for feature_name in feature_names %}
        - {{ feature_name }}
{% endfor %}
    class_labels:
{% for class_label in class_labels %}
        - {{ class_label }}
{% endfor %}
""", trim_blocks=True)
