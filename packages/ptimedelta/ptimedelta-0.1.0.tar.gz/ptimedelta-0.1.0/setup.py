# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ptimedelta']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'ptimedelta',
    'version': '0.1.0',
    'description': 'Pretty Timedelta. Convert your timedelta objects to the pretty strings and vice versa.',
    'long_description': '# ptimedelta\n\nConvert string time periods to timedelta objects and vice versa. \n\n## Features\n1. Supports Python2.7, Python3+.\n\n## Warning\nProject under a development.\n\n## Examples\n```pydocstring\n>>> import ptimedelta as ptd\n>>> ptd.to_timedelta("12m34s")\ndatetime.timedelta(seconds=754)\n```\n',
    'author': 'Anton Goy',
    'author_email': 'g.a.s.s@mail.ru',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/antongoy/ptimedelta',
    'packages': packages,
    'package_data': package_data,
}


setup(**setup_kwargs)
