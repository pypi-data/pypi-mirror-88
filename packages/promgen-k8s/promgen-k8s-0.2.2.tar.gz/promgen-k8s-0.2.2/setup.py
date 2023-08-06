# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['promgen_k8s']

package_data = \
{'': ['*']}

install_requires = \
['pyyaml']

setup_kwargs = {
    'name': 'promgen-k8s',
    'version': '0.2.2',
    'description': 'A modular Prometheus 2 configuration file generator to monitor multiple Kubernetes clusters with a single Prometheus instance.',
    'long_description': None,
    'author': 'Christian Nicolai',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/cmur2/promgen-k8s',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.5,<4.0',
}


setup(**setup_kwargs)
