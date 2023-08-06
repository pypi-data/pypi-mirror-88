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
    'version': '0.2.1',
    'description': 'A process monitor for linux',
    'long_description': '## pmon\n\nA process monitor for linux that shows detailed RAM usage info.\n\n```\n$ pmon 261071\nvms       rss       pss       uss       shared    swap      rss (%)   pss (%)   uss (%)   cpu (%)\n2.576G    1.122G    1.110G    1.107G    99.699M   0B        7.22      7.14      7.12      0.00\n2.576G    1.122G    1.110G    1.107G    99.699M   0B        7.22      7.14      7.12      12.23\n2.576G    1.122G    1.110G    1.107G    99.699M   0B        7.22      7.14      7.12      6.48\n```\n\n### Rationale\n\nMeasuring RAM usage on Linux can be\n[tricky](https://web.archive.org/web/20120520221529/http://emilics.com/blog/article/mconsumption.html).\nProbably the most correct way to measure it is to use\n[`USS`](https://gmpy.dev/blog/2016/real-process-memory-and-environ-in-python), i.e:\n\n> USS (Unique Set Size) is the memory which is unique to a process and which would be freed if the\n> process was terminated right now.\n\nUnfortunately, tools like `top` and `htop` do not report this metric. Nevertheless,\n[psutil](https://github.com/giampaolo/psutil) does collect it, so, we use it as the backend to monitor\nRAM usage.\n\n### Install\n\n```\npipx install pmon\n```\n\n### Usage\n\n```\npmon --help\n```\n',
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
