# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class DashEditor(Component):
    """A DashEditor component.
EditorComponent is an example component.
It takes a property, `label`, and
displays it.
It renders an input with the property `value`
which is editable by the user.

Keyword arguments:
- id (string; optional): The ID used to identify this component in Dash callbacks.
- dataSources (dict; required): The layout of the  components displayed inside the grid.
- fig (dict; optional): The layout of the  components displayed inside the grid."""
    @_explicitize_args
    def __init__(self, id=Component.UNDEFINED, dataSources=Component.REQUIRED, fig=Component.UNDEFINED, **kwargs):
        self._prop_names = ['id', 'dataSources', 'fig']
        self._type = 'DashEditor'
        self._namespace = 'dash_editor'
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'dataSources', 'fig']
        self.available_wildcard_properties =            []

        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}

        for k in ['dataSources']:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')
        super(DashEditor, self).__init__(**args)
