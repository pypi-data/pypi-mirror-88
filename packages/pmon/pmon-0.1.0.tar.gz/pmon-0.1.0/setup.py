# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pmon']

package_data = \
{'': ['*']}

install_requires = \
['psutil>=5.7.3,<6.0.0', 'typer[all]>=0.3.2,<0.4.0']

entry_points = \
{'console_scripts': ['pmon = pmon.cli:app']}

setup_kwargs = {
    'name': 'pmon',
    'version': '0.1.0',
    'description': 'A process monitor for linux',
    'long_description': '## pmon\n\nA process monitor for linux\n\n```\n$ pmon 23245\n\nrss       vms       pss       swap      uss       cpu (%)   mem (%)\n1.06G     2.52G     1.05G     0B        1.05G     0.00      6.83\n1.06G     2.52G     1.05G     0B        1.05G     0.00      6.83\n1.12G     2.58G     1.11G     0B        1.11G     64.20     7.22\n1.12G     2.58G     1.11G     0B        1.11G     0.00      7.22\n```\n\n### Install\n\n```\npipx install pmon\n```\n',
    'author': 'Panos Mavrogiorgos',
    'author_email': 'pmav99@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/pmav99/pmon',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
