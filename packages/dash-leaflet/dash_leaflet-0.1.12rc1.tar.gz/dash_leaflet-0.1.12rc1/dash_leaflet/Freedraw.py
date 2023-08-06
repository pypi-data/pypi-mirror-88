# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class Freedraw(Component):
    """A Freedraw component.
Freedraw is a wrapper of react-leaflet-freedraw.

Keyword arguments:
- children (a list of or a singular dash component, string or number; optional): Attribution
- modes (list of a value equal to: "CREATE", "EDIT", "DELETE", "APPEND", "ALL"s; default ["ALL"]): Which modes to enable.
- markers (dict; optional): Markers return. markers has the following type: dict containing keys 'action', 'positions'.
Those keys have the following types:
  - action (string; optional)
  - positions (list; optional)
- options (dict; optional): Options to https://github.com/Wildhoney/Leaflet.FreeDraw
- className (string; optional): A custom class name to assign to the image. Empty by default.
- id (string; optional): The ID used to identify this component in Dash callbacks"""
    @_explicitize_args
    def __init__(self, children=None, modes=Component.UNDEFINED, markers=Component.UNDEFINED, options=Component.UNDEFINED, className=Component.UNDEFINED, id=Component.UNDEFINED, **kwargs):
        self._prop_names = ['children', 'modes', 'markers', 'options', 'className', 'id']
        self._type = 'Freedraw'
        self._namespace = 'dash_leaflet'
        self._valid_wildcard_attributes =            []
        self.available_properties = ['children', 'modes', 'markers', 'options', 'className', 'id']
        self.available_wildcard_properties =            []

        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}

        for k in []:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')
        super(Freedraw, self).__init__(children=children, **args)
