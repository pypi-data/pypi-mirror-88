# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['odetam']

package_data = \
{'': ['*']}

install_requires = \
['deta>=0.7.0,<0.8.0', 'pydantic>=1.7,<2.0', 'ujson>=4.0,<5.0']

setup_kwargs = {
    'name': 'odetam',
    'version': '1.0.2',
    'description': 'A simple ODM (Object Document Mapper) for Deta Base, based on pydantic.',
    'long_description': '# ODetaM\n\n[![Build Status](https://travis-ci.org/rickh94/ODetaM.svg?branch=main)](https://travis-ci.org/rickh94/ODetaM)\n[![codecov](https://codecov.io/gh/rickh94/odetam/branch/main/graph/badge.svg?token=BLDIMHU9FB)](https://codecov.io/gh/rickh94/odetam)\n\nA simple ODM (Object Document Mapper) for [Deta Base](https://deta.sh) base on\n[pydantic](https://github.com/samuelcolvin/pydantic/).\n\n## Installation\n\n`pip install odetam`\n\n## Usage\n\nCreate pydantic models as normal, but inherit from `DetaModel` instead of pydantic\nBaseModel. You will need to set the environment variable `PROJECT_KEY` to your Deta\nproject key so that databases can be accessed/created. This is a secret key, so handle\nit appropriately (hence the environment variable). Intended for use with FastAPI, but\nthe Deta API is not asynchronous, so any framework could potentially be used.\n\nBases will be automatically created based on model names (changed from\nPascalCase/CamelCase case to snake_case). A `key` field (Deta\'s unique id) will be\nautomatically added to any model. You can supply the key on creation, or Deta will\ngenerate one automatically and it will be added to the object when it is saved.\n\n## Example\n\n```python\nimport datetime\nfrom typing import List\n\nfrom odetam import DetaModel\n\n\nclass Captain(DetaModel):\n    name: str\n    joined: datetime.date\n    ships: List[str]\n\n\n# create\nkirk = Captain(\n    name="James T. Kirk",\n    joined=datetime.date(2252, 1, 1),\n    ships=["Enterprise"],\n)\n\nsisko = Captain(\n    name="Benjamin Sisko",\n    joined=datetime.date(2350, 1, 1),\n    ships=["Deep Space 9", "Defiant"],\n)\n\n# initial save, key is now set\nkirk.save()\n\n# update the object\nkirk.ships.append("Enterprise-A")\n\n# save again, this will be an update\nkirk.save()\n\nsisko.save()\n\nCaptain.get_all()\n# [\n#     Captain(\n#         name="James T. Kirk", \n#         joined=datetime.date(2252, 01, 01), \n#         ships=["Enterprise", "Enterprise-A"],\n#         key="key1",\n#     ),\n#     Captain(\n#         name="Benjamin Sisko",\n#         joined=datetime.date(2350, 01, 01), \n#         ships=["Deep Space 9", "Defiant"],\n#         key="key2",\n#     ),\n# ]\n\nCaptain.get("key1")\n# Captain(\n#     name="James T. Kirk", \n#     joined=datetime.date(2252, 01, 01), \n#     ships=["Enterprise", "Enterprise-A"],\n#     key="key1",\n# )\n\nCaptain.query(Captain.name == "James T. Kirk")\n# Captain(\n#     name="James T. Kirk", \n#     joined=datetime.date(2252, 01, 01), \n#     ships=["Enterprise", "Enterprise-A"],\n#     key="key1",\n# )\n\nCaptain.query(Captain.ships.contains("Defiant"))\n# Captain(\n#     name="Benjamin Sisko",\n#     joined=datetime.date(2350, 01, 01),\n#     ships=["Deep Space 9", "Defiant"],\n# )\n\nCaptain.query(Captain.name.prefix("Ben"))\n# Captain(\n#     name="Benjamin Sisko",\n#     joined=datetime.date(2350, 01, 01),\n#     ships=["Deep Space 9", "Defiant"],\n# )\n\nkirk.delete()\nCaptain.delete_key("key2")\n\nCaptain.get_all()\n# []\n\n# you can also save several at once for better speed\nCaptain.put_many([kirk, sisko])\n# [\n#     Captain(\n#         name="James T. Kirk", \n#         joined=datetime.date(2252, 01, 01), \n#         ships=["Enterprise", "Enterprise-A"],\n#         key="key1",\n#     ),\n#     Captain(\n#         name="Benjamin Sisko",\n#         joined=datetime.date(2350, 01, 01), \n#         ships=["Deep Space 9", "Defiant"],\n#         key="key2",\n#     ),\n# ]\n\n```\n\n## Save\n\nModels have the `.save()` method which will always behave as an upsert, updating a\nrecord if it has a key, otherwise creating it and setting a key. Deta has pure insert\nbehavior, but it\'s less performant. If you need it, please open a pull request.\n\n## Querying\n\nAll basic comparison operators are implemented to map to their equivalents as\n`(Model.field >= comparison_value)`. There is also a `.contains()` and `.not_contains()`\nmethod for strings and lists of strings, as well as a `.prefix()` method for strings.\nThere is also a `.range()` for number types that takes a lower and upper bound. You can\nalso use `&`  as AND and `|` as OR. ORs cannot be nested within ands, use a list of\noptions as comparison instead. You can use as many ORs as you want, as long as they\nexecute after the ANDs in the order of operations. This is due to how the Deta Base api\nworks.\n\n## Deta Base\n\nDirect access to the base is available in the dunder attribute `__db__`, though the\npoint is to avoid that.\n\n## Exceptions\n\n- `DetaError`: Base exception when anything goes wrong.\n- `ItemNotFound`: Fairly self-explanatory...\n- `NoProjectKey`: `PROJECT_KEY` env var has not been set correctly. See Deta\n  documentation.\n- `InvalidDetaQuery`: Something is wrong with queries. Make sure you aren\'t using\n  queries with unsupported types',
    'author': 'Rick Henry',
    'author_email': 'rickhenry@rickhenry.dev',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
