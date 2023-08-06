# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tktimer']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'tktimer',
    'version': '0.1.0',
    'description': 'Timer (stopwatch and countdown) widgets for tkinter',
    'long_description': '# tktimer \n\n**tktimer** is a set of tkinter widgets including a Stopwatch widget and a Countdown widget.\n\n## Installing\n\n```sh\n$ pip install tktimer\n```\n\n## Usage\n\nThe timers have two methods: `start()` and `pause()`.\n\nYou can find example programs in `examples/`.\n\n**Available options**:\n\n|     option      | description |  default  |\n| --------- |:------------------|----------|\n| `parent`  | set the parent widget. ||\n| `prefix`  | set text before timer value.| `""`|\n| `suffix`  | set text after timer value.|`""`|\n| `unit`    | set the unit (available: `second`, `minute`, `hour`, `day`, `week`, `year`).|`second`|\n| `beginning` | set starting point (in seconds). specific to `Countdown`.|`10`|\n| `update_every`| set updating time every X milliseconds.|`10`|\n| `precision`   | set counting precision (number of digits after the decimal point).|`2`|\n| `offset`| set time offset (in seconds). specific to `Stopwatch`.|`10`|\n\n## FAQ\n\n**How can I continue the timer after restarting my app?**\n\nYou can get the elapsed time (in seconds) with `timer.value.get()` on exit and set `offset` later on, which will make the timer start counting from `offset`. For `Countdown`, tweak `beginning` instead of `offset`.\n\n**I\'m not happy with how my timer looks like. Can I change its appearance?**\n\nYes, timers are ultimately just tkinter labels which means you can do anything you would to an ordinary `tkinter.Label`.\n\n## Licensing\n\nLicensed under the [MIT License](https://opensource.org/licenses/MIT). For details, see [LICENSE](https://github.com/adder46/tktimer/blob/master/LICENSE).',
    'author': 'adder46',
    'author_email': 'dedmauz69@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
