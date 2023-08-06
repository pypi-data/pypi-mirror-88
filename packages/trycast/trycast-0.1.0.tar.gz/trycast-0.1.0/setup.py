# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['trycast']
setup_kwargs = {
    'name': 'trycast',
    'version': '0.1.0',
    'description': '',
    'long_description': "# trycast\n\n> **Status:** In development. Current limitations in mypy prevent the examples\n> below from actually typechecking successfully, despite functioning correctly\n> at runtime.\n\nThis module provides a single function `trycast` which can be used to parse a\nJSON-like value.\n\nHere is an example of parsing a `Point2D` object defined as a `TypedDict`:\n\n```python\nfrom bottle import HTTPResponse, request, route\nfrom trycast import trycast\nfrom typing import TypedDict\n\nclass Point2D(TypedDict):\n    x: float\n    y: float\n    name: str\n\n@route('/draw_point')\ndef draw_point_endpoint() -> None:\n    request_json = request.json  # type: object\n    if (point := trycast(Point2D, request_json)) is not None:\n        draw_point(point)  # type is narrowed to Point2D\n    else:\n        return HTTPResponse(status=400)  # Bad Request\n\ndef draw_point(point: Point2D) -> None:\n    # ...\n```\n\nIn this example the `trycast` function is asked to parse a `request_json`\ninto a `Point2D` object, returning the original object (with its type narrowed\nappropriately) if parsing was successful.\n\nMore complex types can be parsed as well, such as the `Shape` in the following\nexample, which is a tagged union that can be either a `Circle` or `Rect` value:\n\n```python\nfrom bottle import HTTPResponse, request, route\nfrom trycast import trycast\nfrom typing import Literal, TypedDict, Union\n\nclass Point2D(TypedDict):\n    x: float\n    y: float\n\nclass Circle(TypedDict):\n    type: Literal['circle']\n    center: Point2D  # a nested TypedDict!\n    radius: float\n\nclass Rect(TypedDict):\n    type: Literal['rect']\n    x: float\n    y: float\n    width: float\n    height: float\n\nShape = Union[Circle, Rect]  # a Tagged Union!\n\n@route('/draw_shape')\ndef draw_shape_endpoint() -> None:\n    request_json = request.json  # type: object\n    if (shape := trycast(Shape, request_json)) is not None:\n        draw_shape(shape)  # type is narrowed to Shape\n    else:\n        return HTTPResponse(status=400)  # Bad Request\n```\n\n## Release Notes\n\n### v0.1.0\n\n* Add support for Python 3.6, 3.7, and 3.9, in addition to 3.8.\n\n### v0.0.2\n\n* Fix README to appear on PyPI.\n* Add other package metadata, such as the supported Python versions.\n\n### v0.0.1\n\n* Initial release.\n* Supports typechecking all types found in JSON.\n",
    'author': 'David Foster',
    'author_email': 'david@dafoster.net',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/davidfstr/trycast',
    'py_modules': modules,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
