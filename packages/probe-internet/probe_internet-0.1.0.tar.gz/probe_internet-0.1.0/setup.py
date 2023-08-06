# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['probe_internet']
install_requires = \
['humanize', 'toml', 'twilio']

entry_points = \
{'console_scripts': ['probe-internet = probe_internet:main']}

setup_kwargs = {
    'name': 'probe-internet',
    'version': '0.1.0',
    'description': 'Probe IP addresses and notify when connections are re-established.',
    'long_description': None,
    'author': 'Michael Merickel',
    'author_email': 'oss@m.merickel.org',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/mmerickel/probe_internet',
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
