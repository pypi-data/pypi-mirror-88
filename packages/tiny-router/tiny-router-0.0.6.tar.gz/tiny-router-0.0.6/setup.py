# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tiny_router', 'tiny_router.simple_regex']

package_data = \
{'': ['*']}

install_requires = \
['typing-extensions>=3.7.4,<4.0.0']

setup_kwargs = {
    'name': 'tiny-router',
    'version': '0.0.6',
    'description': 'Tiny HTTP router',
    'long_description': '# tiny-router\n\n[![PyPI](https://img.shields.io/pypi/v/tiny-router)](https://pypi.org/project/tiny-router/)\n[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/tiny-router)](https://pypi.org/project/tiny-router/)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n[![license](https://img.shields.io/github/license/nekonoshiri/tiny-router)](https://github.com/nekonoshiri/tiny-router/blob/main/LICENSE)\n\nA tiny HTTP router like this:\n\n```Python\nfrom tiny_router import SimpleRouter\n\nrouter = SimpleRouter()\n\n\n@router.get("/users")\ndef list_users():\n    ...\n\n\n@router.post("/users")\ndef create_user():\n    ...\n\n\nanother_router = SimpleRouter()\nrouter.include(another_router)\n\nroute = router.resolve("GET", "/users")\n```\n\n## Features\n\n- `SimpleRouter`: exact-match router\n- `SimpleRegexRouter`: simple regex-based router\n- Abstract `Router`: user can implement their own routers\n- Support for type hints\n\n## Usage\n\nSee `examples/` directory of [repository](https://github.com/nekonoshiri/tiny-router).\n',
    'author': 'Shiri Nekono',
    'author_email': 'gexira.halen.toms@gmail.com',
    'maintainer': 'Shiri Nekono',
    'maintainer_email': 'gexira.halen.toms@gmail.com',
    'url': 'https://github.com/nekonoshiri/tiny-router',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.2,<4.0.0',
}


setup(**setup_kwargs)
