# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sqlalchemy_querybuilder']

package_data = \
{'': ['*']}

install_requires = \
['sqlalchemy']

setup_kwargs = {
    'name': 'sqlalchemy-querybuilder',
    'version': '0.1.4',
    'description': 'Build sqlalchemy queries from jQuery-Query json',
    'long_description': 'SQLAlchemy query builder for jQuery QueryBuilder\n================================================\n\n[![Project Status: Active – The project has reached a stable, usable state and is being actively developed.](https://www.repostatus.org/badges/latest/active.svg)](https://www.repostatus.org/#active) [![builds.sr.ht status](https://builds.sr.ht/~ocurero/sqlalchemy-querybuilder/.build.yml.svg)](https://builds.sr.ht/~ocurero/sqlalchemy-querybuilder/.build.yml?) [![codecov](https://codecov.io/gh/ocurero/sqlalchemy-querybuilder/branch/master/graph/badge.svg)](https://codecov.io/gh/ocurero/sqlalchemy-querybuilder) [![readthedocs](https://readthedocs.org/projects/sqlalchemy-querybuilder/badge/?version=latest&style=flat)](https://sqlalchemy-querybuilder.readthedocs.io/)\n\nThis package implements a sqlalchemy query builder for json data\ngenerated with (but not limited to) [`jQuery QueryBuilder`](http://querybuilder.js.org/).\n\n* Open Source: Apache 2.0 license.\n* Website: <https://sr.ht/~ocurero/sqlalchemy-querybuilder/>\n* Documentation: <https://sqlalchemy-querybuilder.readthedocs.io/>\n\nQuickstart\n----------\n\nUsing **sqlalchemy-querybuilder** is very simple:\n\n```python\n\nfrom sqlalchemy_querybuilder import Filter\nfrom myapp import models, query\n\n    rules = {\n            "condition": "OR",\n            "rules": [{\n                       "field": "mytable.myfield",\n                       "operator": "equal",\n                       "value": "foo"\n                       },\n                      ],\n             }\n\n    myfilter = Filter(models, query)\n    print(myfilter.querybuilder(rules))\n```\n',
    'author': 'Oscar Curero',
    'author_email': 'oscar@curero.es',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://sr.ht/~ocurero/sqlalchemy-querybuilder/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
