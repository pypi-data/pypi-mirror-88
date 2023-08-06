# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['lapis', 'lapis.cli', 'lapis.job_io', 'lapis.monitor', 'lapis.pool_io']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.1,<8.0', 'cobald>=0.12,<0.13', 'usim>=0.4,<0.5']

extras_require = \
{'doc': ['Sphinx>=3.3.1,<4.0.0',
         'sphinx-rtd-theme>=0.5.0,<0.6.0',
         'sphinxcontrib-contentui>=0.2.5,<0.3.0',
         'sphinx-click>=2.5.0,<3.0.0',
         'change-log>=0.2.0,<0.3.0'],
 'test': ['pytest>=4.3.0',
          'flake8>=3.8.4,<4.0.0',
          'flake8-bugbear>=20.11.1,<21.0.0'],
 'test:implementation_name == "cpython"': ['black>=20.8b1,<21.0']}

setup_kwargs = {
    'name': 'lapis-sim',
    'version': '0.4.2',
    'description': 'Lapis is an adaptable, performant, and interactive scheduling (Lapis) simulator',
    'long_description': '===============================================================================\nLapis is an adaptable, performant, and interactive scheduling (Lapis) simulator\n===============================================================================\n\nThe ``lapis`` library provides a framework and runtime for simulating the scheduling and usage of opportunistic\nand static resources.\n\nCommand Line Interface\n----------------------\n\nCurrently the library provides a simple command line interface that allows three modes of operation:\n\n* static provisioning of resources,\n* dynamic provisioning of resources, and\n* hybrid provisioning of resources.\n\nIn the most simple case you can apply a given workload, e.g. downloaded from the parallel workload archive to a\nstatic resource configuration:\n\n\n.. code:: bash\n\n    python3 simulate.py --log-file - static --job-file <path-to-workload> swf --pool-file <path-to-pool-definition> htcondor\n\nThe output of simulation is given to stdout. You have further options you can explore via\n\n.. code:: bash\n\n    python3 simulate.py --help\n\nand more specifically for the different operation modes with\n\n.. code:: bash\n\n    python3 simulate.py static --help\n',
    'author': 'Eileen Kuehn, Max Fischer',
    'author_email': 'mainekuehn@gmail.com',
    'maintainer': 'MatterMiners',
    'maintainer_email': 'matterminers@lists.kit.edu',
    'url': 'https://matterminers.github.io',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
