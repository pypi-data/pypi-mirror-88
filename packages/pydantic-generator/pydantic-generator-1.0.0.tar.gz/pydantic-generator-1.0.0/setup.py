# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pydantic_generator',
 'pydantic_generator.core',
 'pydantic_generator.core.parser']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['pydanticgen = pydantic_generator.main:main']}

setup_kwargs = {
    'name': 'pydantic-generator',
    'version': '1.0.0',
    'description': 'pydantic-generator generates the pydantic model classes.',
    'long_description': '# pydantic-generator\n\npydantic-generator generates a pydantic schema module from a json file.\n\n## install\n\npydantic-generates uses `ast.unparse()` and therefore only supports python 3.9+.\n\n```shell\n$ python3.9 -m pip install pydantic-generator\n$ pydanticgen --help\nusage: pydanticgen [-h] -i INPUT_ [-o OUTPUT]\n\noptional arguments:\n  -h, --help            show this help message and exit\n  -i INPUT_, --input_ INPUT_, --input INPUT_\n  -o OUTPUT, --output OUTPUT\n```\n\n## example\n\n```shell\n$ ls\nresponse.json\n$ cat response.json\n{\n  "menu": {\n    "id": "file",\n    "value": "File",\n    "popup": {\n      "menuitem": [\n        {\n          "value": "New",\n          "onclick": "CreateNewDoc()"\n        },\n        {\n          "value": "Open",\n          "onclick": "OpenDoc()"\n        },\n        {\n          "value": "Close",\n          "onclick": "CloseDoc()"\n        }\n      ]\n    }\n  }\n}\n\n# this command generates Response.json\n$ pydanticgen -i response.json\n$ ls\nresponse.json Response.py\n$ cat Response.py\nfrom pydantic import BaseModel\n\nclass Response(BaseModel):\n\n    class Menu(BaseModel):\n        id: str\n        value: str\n\n        class Popup(BaseModel):\n\n            class Menuitem(BaseModel):\n                value: str\n                onclick: str\n            menuitem: list[Menuitem]\n        popup: Popup\n    menu: Menu\n```\n\n(This sample can be found at https://json.org/example.html.)\n',
    'author': 'rhoboro',
    'author_email': 'rhoboro@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/rhoboro/pydantic-generator',
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
