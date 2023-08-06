# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['avro_to_python_types']

package_data = \
{'': ['*']}

install_requires = \
['astor>=0.8.1,<0.9.0']

setup_kwargs = {
    'name': 'avro-to-python-types',
    'version': '0.1.0',
    'description': 'A library for converting avro schemas to python types.',
    'long_description': '# avro-to-python-types\n\nA library for converting avro schemas to python types.\n\nCurrently, it supports converting `record`s to `TypedDict`. If you would like to see more features added, please open up an issue.\n\n## Why would I want this?\n\nThis library is target to people writing code generation for python apps that are using avro.\n\n## Example usage\n\n```python\nfrom avro_to_python_types import schema_to_typed_dict\n\nwith open(test_json_file) as f:\n    avro_schema = f.read()\n    output = schema_to_typed_dict(avro_schema)\n    print(output)\n```\n\nThe avro schema will produce the following python\n\n```json\n{\n  "namespace": "example.avro",\n  "type": "record",\n  "name": "User",\n  "fields": [\n    { "name": "name", "type": "string" },\n    { "name": "favorite_number", "type": ["int", "null"] },\n    { "name": "favorite_color", "type": ["string", "null"] },\n    {\n      "name": "address",\n      "type": {\n        "type": "record",\n        "name": "AddressUSRecord",\n        "fields": [\n          { "name": "streetaddress", "type": "string" },\n          { "name": "city", "type": "string" }\n        ]\n      }\n    },\n    {\n      "name": "other_thing",\n      "type": {\n        "type": "record",\n        "name": "OtherThing",\n        "fields": [\n          { "name": "thing1", "type": "string" },\n          { "name": "thing2", "type": ["int", "null"] }\n        ]\n      }\n    }\n  ]\n}\n```\n\n```python\nfrom typing import TypedDict, Optional\n\nclass AddressUSRecord(TypedDict):\n    streetaddress: str\n    city: str\n\n\nclass OtherThing(TypedDict):\n    thing1: str\n    thing2: Optional[int]\n\n\nclass User(TypedDict):\n    name: str\n    favorite_number: Optional[int]\n    favorite_color: Optional[str]\n    address: AddressUSRecord\n    other_thing: OtherThing\n```\n',
    'author': 'Dan Green-Leipciger',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/dangreenisrael/avro-to-python-types',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
