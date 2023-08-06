# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['kharosthi']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'kharosthi.numbers',
    'version': '0.1.2',
    'description': 'A module to represent kharosthi numbers',
    'long_description': '# Kharosthi numbers\nA naive representation of Kharosthi numerals, and a way to do simple arithmetic on them (actually, we\'re cheating and doing arithmetic on `int` versions of the numbers).\n\nCurrently only supports numbers less than 10000. The naive conversion algorithm currently can\'t deal with arbitrarily big numbers, so we only support "𐩇" with a maximum value of 9 in front of it.\n\nAlso, 0 and negative integers are not representable in Kharosthi, and not valid numbers.\n\n## Requirements\nPython >= 3.6\n\n## Usage\n```python\nfrom kharosthi.numbers import KharosthiNumber as K\n\nsum = K.from_int(5) + K.from_int(50)\n\n# 7 - 4 = 3\nint(difference) = K("𐩃𐩂") - K("𐩃")\n```\n\nReference: https://en.wikipedia.org/wiki/Kharosthi#Numerals\n',
    'author': 'Ulrik Johansson',
    'author_email': 'ulrik@ulrik.io',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ulrikjohansson/kharosthi_numbers',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
