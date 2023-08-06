# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pypads_padre',
 'pypads_padre.app',
 'pypads_padre.app.backends',
 'pypads_padre.bindings',
 'pypads_padre.bindings.resources',
 'pypads_padre.bindings.resources.mapping',
 'pypads_padre.concepts',
 'pypads_padre.injections',
 'pypads_padre.injections.analysis',
 'pypads_padre.injections.loggers']

package_data = \
{'': ['*']}

install_requires = \
['pypads-onto>=0.2.2,<0.3.0', 'pypads>=0.4.0,<0.5.0']

setup_kwargs = {
    'name': 'pypads-padre',
    'version': '0.4.0',
    'description': 'PyPads_PaDRe aims to to add additional machine learning concepts into the world of pypads.',
    'long_description': '# PadrePads\nAn extension of pypads that implements and tracks other concepts from machine learning experiments.   \n\n[![Documentation Status](https://readthedocs.org/projects/pypads-onto/badge/?version=latest)](https://pypads.readthedocs.io/projects/pypads-onto/en/latest/?badge=latest)\n[![PyPI version](https://badge.fury.io/py/pypads-padre.svg)](https://badge.fury.io/py/pypads-padre)  \n\n<!--- ![Build status](https://gitlab.padim.fim.uni-passau.de/RP-17-PaDReP/padre-pads/badges/master/pipeline.svg) --->\n\n# Intalling\nThis tool requires those libraries to work:\n\n    Python (>= 3.6),\n    pypads (>= 0.1.8)\n    \nPadrePads only support python 3.6 and higher. To install pypads_padre run this in you terminal\n\n**Using source code**\n\nFirst, you have to install **poetry** if not installed\n\n    pip install poetry\n    poetry build (in the root folder of the repository padre-pads/)\n\nThis would create two files under dist/ that can be used to install,\n\n    pip install dist/pypads-padre-X.X.X.tar.gz\n    OR\n    pip install dist/pypads-padre-X.X.X-py3-none-any.whl\n    \n \n**Using pip ([PyPi release](https://pypi.org/project/pypads-padre/))**\n\nThe package can be found on PyPi in following [project](https://pypi.org/project/pypads-padre/).\n\n    pip install pypads_padre\n\n\n### Tests\nThe unit tests can be found under \'test/\' and can be executed using\n\n    poetry run pytest test/\n\n# Documentation\n\nFor more information, look into the [official documentation of PadrePads](https://pypads.readthedocs.io/en/latest/projects/pypads-padre.html).\n\n# Scientific work disclaimer\nThis was created in scope of scientific work of the Data Science Chair at the University of Passau. If you want to use this tool or any of its resources in your scientific work include a citation.\n\n# Acknowledgement\nThis work has been partially funded by the **Bavarian Ministry of Economic Affairs, Regional Development and Energy** by means of the funding programm **"Internetkompetenzzentrum Ostbayern"** as well as by the **German Federal Ministry of Education and Research** in the project **"Provenance Analytics"** with grant agreement number *03PSIPT5C*.\n',
    'author': 'Thomas Weißgerber',
    'author_email': 'thomas.weissgerber@uni-passau.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://www.padre-lab.eu/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.0,<4.0.0',
}


setup(**setup_kwargs)
