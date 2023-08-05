# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['fuchar', 'fuchar.fonts']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['fuchar = fuchar.__main__:main']}

setup_kwargs = {
    'name': 'fuchar',
    'version': '2020.11.0a1',
    'description': 'Simple Python Text Renderer',
    'long_description': '# fuchar\n',
    'author': 'Shane R. Spencer',
    'author_email': '305301+whardier@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/whardier/fuchar',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
