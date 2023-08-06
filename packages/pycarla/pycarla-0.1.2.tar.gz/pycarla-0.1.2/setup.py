# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pycarla']

package_data = \
{'': ['*']}

install_requires = \
['PyQt5>=5.15.2,<6.0.0',
 'jack-client>=0.5.2,<0.6.0',
 'mido>=1.2.9,<2.0.0',
 'numpy>=1.19.0,<2.0.0',
 'pysoundfile>=0.9.0,<0.10.0',
 'python-rtmidi>=1.4.6,<2.0.0',
 'sounddevice>=0.4.1,<0.5.0']

setup_kwargs = {
    'name': 'pycarla',
    'version': '0.1.2',
    'description': 'Use VST/LV2/etc. plugins with realtime abilities in Python',
    'long_description': 'pyCarla\n==========\n\n.. image:: https://zenodo.org/badge/DOI/10.5281/zenodo.4332847.svg\n   :target: https://doi.org/10.5281/zenodo.4332847\n\nA python module based on Linux commands for synthesizing MIDI events and files\nfrom python code with ultra time precision using any kind of audio plugin!\n\nSee `docs <https://pycarla.readthedocs.org>`_ for more installation and more info.\n\nCredits\n=======\n\n#. `Federico Simonetta <https://federicosimonetta.eu.org>`_\n    ``federico.simonetta`` ``at`` ``unimi.it``\n',
    'author': 'Federico Simonetta',
    'author_email': 'federico.simonetta@unimi.it',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://pycarla.readthedocs.org',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
