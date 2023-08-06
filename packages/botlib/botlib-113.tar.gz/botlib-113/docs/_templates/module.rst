# BOTLIB - module.rst
#
# this file is placed in the public domain

{{ fullname }}
{{ underline }}

.. automodule:: {{ fullname }}

    {% block exceptions %}
    {% if exceptions %}
    .. rubric:: exceptions

    .. autosummary::
    {% for item in exceptions %}
        {{ item }}
    {%- endfor %}
    {% endif %}
    {% endblock %}

    {% block classes %}
    {% if classes %}
    .. rubric:: classes

    .. autosummary::
    {% for item in classes %}
        {{ item }}
    {%- endfor %}
    {% endif %}
    {% endblock %}

    {% block functions %}
    {% if functions %}
    .. rubric:: functions

    .. autosummary::
    {% for item in functions %}
        {{ item }}
    {%- endfor %}
    {% endif %}
    {% endblock %}

    source
    ======
