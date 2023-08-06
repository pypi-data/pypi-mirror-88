# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['niaaml_gui',
 'niaaml_gui.widgets',
 'niaaml_gui.windows',
 'niaaml_gui.windows.threads']

package_data = \
{'': ['*']}

install_requires = \
['NiaPy>=2.0.0rc12,<3.0.0',
 'PyQt5>=5.15.2,<6.0.0',
 'QtAwesome>=1.0.2,<2.0.0',
 'niaaml==1.0.0rc7']

setup_kwargs = {
    'name': 'niaaml-gui',
    'version': '0.1.7',
    'description': '',
    'long_description': None,
    'author': 'Luka Pečnik',
    'author_email': 'lukapecnik96@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
