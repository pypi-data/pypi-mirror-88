# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['combu']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'combu',
    'version': '1.0.0',
    'description': 'Execute your method with combination parameters.',
    'long_description': "# combu\n\n[![build](https://circleci.com/gh/takelushi/combu.svg?style=svg)](https://circleci.com/gh/takelushi/combu) ![python](doc/badge/python.svg) [![license](doc/badge/license.svg)](https://opensource.org/licenses/MIT) ![coverage](doc/badge/coverage.svg)\n\nExecute your method with combination parameters.\n\n## Use cases\n\n* Testing\n   * Test pattern.\n* Machine learning\n   * Model validation.\n   * Grid search.\n* Web Scraping\n   * Query parameters pattern.\n\n## Install\n\n```sh\npip install conbu\n```\n\n## Tutorial\n\n### Simple usage\n\n#### One time loop\n\n```python\nimport combu\n\ndef func(v1, v2):\n   return v1 + v2\n\n\nparams = {'v1': ['a', 'b'], 'v2': ['A', 'B']}\nfor res, param in combu.execute(func, params):\n   print(res, param)\n\n# Output\n'''\naA {'v1': 'a', 'v2': 'A'}\naB {'v1': 'a', 'v2': 'B'}\nbA {'v1': 'b', 'v2': 'A'}\nbB {'v1': 'b', 'v2': 'B'}\n'''\n\n# Set loop order\norder = ['v2', 'v1']\nfor res, param in combu.execute(func, params, order=order):\n   print(res, param)\n\n# Output\n'''\naA {'v2': 'A', 'v1': 'a'}\nbA {'v2': 'A', 'v1': 'b'}\naB {'v2': 'B', 'v1': 'a'}\nbB {'v2': 'B', 'v1': 'b'}\n'''\n```\n\n#### Reloopable by using class\n\n```python\nimport combu\n\ndef func(v1, v2):\n   return v1 + v2\n\ncomb = combu.Combu(func)\n# You can set order on initializer.\n# comb = combu.Combu(func, order=['v2', 'v1'])\n\nparams = {'v1': ['a', 'b'], 'v2': ['A', 'B']}\nfor res, param in comb.execute(params):\n   print(res, param)\n\nparams = {'v1': ['x', 'y'], 'v2': ['X', 'Y']}\nfor res, param in comb.execute(params):\n   print(res, param)\n\n# You can set order on Combu.execute().\nfor res, param in comb.execute(params, order=['v2', 'v1']):\n   print(res, param)\n```\n\n#### Hooks\n\n* Hooks flow\n\n   ```txt\n   order = [A, B]\n\n   before_a()\n   for a in A:\n      before_b()\n      before_each_a()\n      for b in B:\n         before_each_b()\n         func()\n         after_each_b()\n      after_each_a()\n      after_b()\n   after_a()\n   ```\n\n* Define hooks.\n\n   ```python\n   def func(v1, v2):\n      pass\n\n   def before_v1(v1, v2):\n      pass\n\n   # Initialize with hooks.\n   # Available:\n   # * before\n   # * after\n   # * before_each\n   # * after_each\n   comb = Comb(func, before={'v1': before_v1})\n\n   # Set a hook after initialized.\n   # Available:\n   # * set_before(k, func)\n   # * set_after(k, func)\n   # * set_before_each(k, func)\n   # * set_after_each(k, func)\n   comb.set_before('v1', before_v1)\n   ```\n\n#### Utility\n\n* Create parameter index combination.\n   * `combu.create_index`\n* Create parameter combination (not execute any function).\n   * `combu.create_value`\n* Count combinations.\n   * `combu.util.count`\n* Shuffle parameters.\n   * `combu.util.shuffle_params`\n\n## Development\n\n* Requirements: poetry, pyenv\n\n```sh\n# Setup\npoetry install\n\n# Lint & Test\nmkdir report\npoetry run flake8 --format=html --htmldir=report/flake-report .\npoetry run pytest --cov-report html:report/coverage --cov=combu tests/\n\n# Build and publish\npoetry run python create_badges.py\npoetry build\npoetry publish\n```\n",
    'author': 'Takeru Saito',
    'author_email': 'takelushi@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/takelushi/combu',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
