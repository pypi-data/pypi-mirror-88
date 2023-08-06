# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['supertimer']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'supertimer',
    'version': '0.3.0',
    'description': 'Contextmanager to print or log execution time of code blocks',
    'long_description': '# supertimer\n\nContextmanager to print or log execution time of code blocks\n\nOriginal url: https://github.com/mariushelf/supertimer\n\n\n# Etymology\n\nThis package provides a timer. But the name `timer` was already taken.\nSo I needed a new name. Inspired by my recently freshly flamed up\nlove for the good old Super Nintendo, I thought that this timer could\nas well be *super*.\n\n# License\n\n[MIT](LICENSE)\n\n\n# Changelog\n\n## v0.3.0\n* convenience classes `print_timer`, `debug_timer` and `info_timer`\n* make timer function configurable\n\n## v0.2.0\n* mention success or error after execution\n\n## v0.1.0\n* First release\n\n\n# Author\n\nMarius Helf ([helfsmarius@gmail.com](mailto:helfsmarius@gmail.com))\n',
    'author': 'Marius Helf',
    'author_email': 'helfsmarius@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
