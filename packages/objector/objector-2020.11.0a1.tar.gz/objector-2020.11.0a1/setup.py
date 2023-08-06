# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['objector']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'objector',
    'version': '2020.11.0a1',
    'description': 'Object recursion, mapping, and iteration tools',
    'long_description': '# objectify\nData recursion, mapping, and iteration tools\n',
    'author': 'Shane R. Spencer',
    'author_email': '305301+whardier@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/whardier/objector',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
