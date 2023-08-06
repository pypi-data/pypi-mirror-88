# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['iubeo']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'iubeo',
    'version': '0.2.0',
    'description': 'Friendlier way to write your config.',
    'long_description': '[![Build Status](https://travis-ci.com/isik-kaplan/iubeo.svg?branch=master)](https://travis-ci.com/isik-kaplan/iubeo)\n[![PyPI - License](https://img.shields.io/pypi/l/iubeo.svg)](https://pypi.org/project/iubeo/)\n[![PyPI - Downloads](https://img.shields.io/pypi/dm/iubeo.svg)](https://pypi.org/project/iubeo/)\n\n\n## What is *iubeo*?\n\nFriendlier way to write your config.\n\n## What is it good for?\n\nYou write how you want to read your config.\n\n```py\nfrom iubeo import config\n\ndef list_from_string(val):\n    return val.split(\',\')\n\nCONFIG = config({\n    \'DATABASE\': {\n        \'USER\': str,\n        \'PASSWORD\': str,\n        \'HOST\': str,\n        \'PORT\': str,\n    },\n    \'ALLOWED_HOSTS\': list_from_string,\n})\n```\n\nIt creates the environment variable names for you, and reads them from the environment, casting it to the final nodes.\n\nNow your can just chain the attributes, and if it is the last node on the above dictionary, you get the environment\nvariable casted to given callable.\n\n```.env\nDATABASE__USER=isik-kaplan\nDATABASE__PASSWORD=isik-kaplan-db-password\nDATABASE__HOST=localhost\nDATABASE__PORT=5432\nALLOWED__HOSTS=isik-kaplan.com,api.isik-kaplan.com,www.isik-kaplan.com\n```\n\nare read from the environment, and are casted when you access the attribute.\n\n```py\nCONFIG.DATABASE.USER # "isik-kaplan"\nCONFIG.DATABASE.PASSWORD # "isik-kaplan-db-password"\nCONFIG.DATABASE.HOST # "localhost"\nCONFIG.DATABASE.PORT # "5432"\nCONFIG.ALLOWED_HOSTS # ["isik-kaplan.com", "api.isik-kaplan.com", "www.isik-kaplan.com"]\n```\n\nIubeo also comes with couple of pre-configured functions to read common environment variable types:\n```py\nfrom iubeo import config, comma_separated_list, boolean\n\nCONFIG = config({\n    \'DATABASE\': {\n        \'USER\': str,\n        \'PASSWORD\': str,\n        \'HOST\': str,\n        \'PORT: str,\n    },\n    \'ALLOWED_HOSTS\': comma_separated_list,\n    \'DEBUG\': boolean,\n})\n```\n',
    'author': 'isik-kaplan',
    'author_email': 'isik.kaplan@outlook.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/isik-kaplan/iubeo',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
