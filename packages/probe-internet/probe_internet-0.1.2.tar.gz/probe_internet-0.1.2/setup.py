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
    'version': '0.1.2',
    'description': 'Probe IP addresses and notify when connections are re-established.',
    'long_description': '# Installation\n\n```console\n$ pip install probe-internet\n```\n\n## Usage\n\nDefine a `profile.toml` similar to:\n\n```toml\n[probe]\nip = "8.8.8.8"\nport = 53\n\n# how often to probe\ninterval = 5\ntimeout = 3\n\n[twilio]\naccount_sid = "..."\nauth_token = "..."\nsource_phone_number = "+1..."\ntarget_phone_number = "+1..."\n\n# how long must the connection be down before a message is sent\nmin_interval = 30\n```\n\nRun it:\n\n```console\n$ probe-internet\n```\n',
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
