# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tests', 'xestore', 'xestore.api', 'xestore.client']

package_data = \
{'': ['*'], 'xestore.api': ['domain/*']}

install_requires = \
['click',
 'eve-jwt>=0.1.3,<0.2.0',
 'httpx>=0.16.1,<0.17.0',
 'panel>=0.10.2,<0.11.0']

entry_points = \
{'console_scripts': ['xestore = xestore.cli:main']}

setup_kwargs = {
    'name': 'xestore',
    'version': '0.1.0',
    'description': 'Top-level package for xestore.',
    'long_description': '=======\nxestore\n=======\n\n\n.. image:: https://img.shields.io/pypi/v/xestore.svg\n        :target: https://pypi.python.org/pypi/xestore\n\n.. image:: https://img.shields.io/travis/jmosbacher/xestore.svg\n        :target: https://travis-ci.com/jmosbacher/xestore\n\n.. image:: https://readthedocs.org/projects/xestore/badge/?version=latest\n        :target: https://xestore.readthedocs.io/en/latest/?badge=latest\n        :alt: Documentation Status\n\n\n\n\nA simple file and document storage utility for XENONnT\n\nUsage\n-----\n\n.. code-block:: python\n\n    import xestore\n\n    xestore.login()\n\n    xestore.publish_file(path, metadata={}, private=False)\n\n    xestore.download_file("filename.npy", savedir="./", private=False)\n\n    doc = {"list": [1,2,3]}\n    xestore.publish_document(doc, name="new document", metadata={}, private=False)\n    \n\n\n\n\n* Free software: MIT\n* Documentation: https://xestore.readthedocs.io.\n\n\nFeatures\n--------\n\n* TODO\n\nCredits\n-------\n\nThis package was created with Cookiecutter_ and the `briggySmalls/cookiecutter-pypackage`_ project template.\n\n.. _Cookiecutter: https://github.com/audreyr/cookiecutter\n.. _`briggySmalls/cookiecutter-pypackage`: https://github.com/briggySmalls/cookiecutter-pypackage\n',
    'author': 'Yossi Mosbacher',
    'author_email': 'joe.mosbacher@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/jmosbacher/xestore',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
