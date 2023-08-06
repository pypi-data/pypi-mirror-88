# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['life_stream_cli',
 'life_stream_cli.subcommands',
 'life_stream_cli.subcommands.config']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.1.2,<8.0.0',
 'colorama>=0.4.4,<0.5.0',
 'prompt-toolkit>=3.0.8,<4.0.0',
 'requests>=2.25.0,<3.0.0',
 'termcolor>=1.1.0,<2.0.0']

entry_points = \
{'console_scripts': ['lst = life_stream_cli:cli']}

setup_kwargs = {
    'name': 'life-stream-cli',
    'version': '0.2.1',
    'description': 'A client for the Life Stream service',
    'long_description': '# life-stream-cli\n\n# Overview\n\nLife is a stream of events, thought noise and ideas are coming every day. The Life Stream service is intended to organize\nsmall notes. Simply save them under the one or more tags. You can find them later easily.\nIf you want to forget something, simply put it down. \n\n## How to distribute\n\n1. `python -m pep517.build .`\n2. `twine upload dist/*`\n3. `pip install life-stream-cli`\n\n## Useful tips\n\n- (Development) Switching between profiles `lst config --set active-profile=default`',
    'author': 'Sergey Royz',
    'author_email': 'zjor.se@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/zjor/life-stream-cli',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
