# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['supertimer']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'supertimer',
    'version': '0.4.0',
    'description': 'Contextmanager to print or log execution time of code blocks',
    'long_description': '# supertimer\n\nContextmanager to print or log execution time of code blocks\n\nOriginal url: https://github.com/mariushelf/supertimer\n\n\n# Etymology\n\nThis package provides a timer. But the name `timer` was already taken.\nSo I needed a new name. Inspired by my recently freshly flamed up\nlove for the good old Super Nintendo, I thought that this timer could\nas well be *super*.\n\n\n# Usage\n\n## Use as a context manager\n\nTo log the duration of a code block:\n```python\nfrom supertimer import timer\nimport time\n\nwith timer("Sleeping a bit"):\n    time.sleep(2)\n```\nThis will log:\n```\nSleeping a bit starting at 2020-12-14 18:34:54.403371\nSleeping a bit finished successfully at 2020-12-14 18:34:56.404208 after 0:00:02.000837.\n```\n\n## Use as a decorator\n\n```python\nfrom supertimer import timer\nimport time\n\n@timer("Sleeping a bit")\ndef sleep_a_bit():\n    time.sleep(2)\n\nsleep_a_bit()\n```\n\nThis will log the same message as the context manager each time\nthe decorated function is called:\n```\nSleeping a bit starting at 2020-12-14 18:34:54.403371\nSleeping a bit finished successfully at 2020-12-14 18:34:56.404208 after 0:00:02.000837.\n```\n\n\n## Configuring the output method\n\nBy default, the output is logged at loglevel `DEBUG`.\n\nThe loglevel can be changed with the `loglevel` parameter. Printing to `stdout` can be\nactivated by setting the `print` parameter to `True`. Logging can be disabled by\nsetting `log` to `False`:\n\n```python\nwith timer(loglevel=logging.INFO):\n    # logging at loglevel INFO, no printing\n    ...\n    \nwith timer(print=True, log=False):\n    # just printing, no logging\n    ...\n```\n\n## Changing the logger\n\nThe logger can be configured:\n```python\nimport logging\n\nlogger = logging.getLogger("my.custom.logger")\nwith timer(logger=logger):\n    do_something()\n```\n\nIf no logger is provided, a logger named `supertimer` is used.\n\n\n## Convenience classes\n\nThere are convenience classes which are preconfigured for a certain loglevel or\njust printing:\n* `print_timer`\n* `debug_timer`\n* `info_timer`\n\n## Configuring defaults\n\nAll constructor arguments have a `default_.*` class attribute counterpart which\nspecify defaults in case the arguments are omitted.\n\nFor example, to change the default loglevel to `WARNING` one could do:\n\n```python\ntimer.default_loglevel = logging.WARNING\nwith timer("Sleep warning"):\n    # log timings with loglevel `WARNING`\n    time.sleep(2)\n    \nwith timer("Sleep debug", loglevel=logging.DEBUG):\n    # log timings with loglevel `DEBUG`\n    time.sleep(2)\n```\n\n\n# How time is measured\n\nBy default, the start and end time are taken with `datetime.dateime.now`. The duration\nis calculated as the difference of start and end time, resulting in a \n`datetime.timedelta` object.\n\nThe timer function can be overridden:\n```python\nimport timeit\n\nwith timer(timer_func=timeit.default_timer):\n    ...\n```\nThe `timer_func` parameter expects a callable that returns a value which supports the\n`minus` operation when called without an argument.\n\n\n# License\n\n[MIT](LICENSE)\n\n\n# Changelog\n\n## 0.4.0\n* timer can now be used as a decorator\n* global default configuration\n* additional `log` parameter\n* documentation\n* change name of default logger to `supertimer`\n\n## 0.3.0\n* convenience classes `print_timer`, `debug_timer` and `info_timer`\n* make timer function configurable\n\n## 0.2.0\n* mention success or error after execution\n\n## 0.1.0\n* First release\n\n\n# Author\n\nMarius Helf ([helfsmarius@gmail.com](mailto:helfsmarius@gmail.com))\n',
    'author': 'Marius Helf',
    'author_email': 'helfsmarius@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/mariushelf/supertimer',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
