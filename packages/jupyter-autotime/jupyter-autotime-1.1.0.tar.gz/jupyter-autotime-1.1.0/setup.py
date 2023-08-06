# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['autotime']

package_data = \
{'': ['*']}

install_requires = \
['ipython>=6,<8']

setup_kwargs = {
    'name': 'jupyter-autotime',
    'version': '1.1.0',
    'description': 'Display elapsed time on Jupyter.',
    'long_description': '# jupyter-autotime\n\nDisplay elapsed time on Jupyter.\n\n![Demo](demo.gif)\n\n## Getting start\n\n1. Install\n   * On shell.\n\n      ```sh\n      pip install jupyter-autotime\n      ```\n\n   * On Jupyter.\n\n      ```python\n      !pip install jupyter-autotime\n      ```\n\n1. Enable autotime\n\n   ```python\n   %load_ext autotime\n   ```\n\n## Other usage\n\n```python\n# Reload.\n%reload_ext autotime\n\n# Disable.\n%unload_ext autotime\n```\n\n## Customization\n\n* First, import the module to hack `autotime`.\n\n   ```python\n   import autotime\n   ```\n\n* Customize timespan format.\n\n   ```python\n   def my_format_timepan(timespan: float) -> str):\n      """My custom timespan format."""\n      # e.g. \'12 sec\'\n      return \'{} sec\'.format(int(timespan))\n   autotime.format_timespan = my_format_timepan\n   ```\n\n* Customize time format.\n\n   ```python\n   # e.g. \'2020/12/10 16:15:11\'\n   autotime.TIME_FORMAT = \'%Y/%m/%d %H:%M:%S\'\n   ```\n\n* Customize output format.\n\n   ```python\n   # e.g. \'[RUNNING] 3.09 s (2020-12-10T15:58:35)\'\n   autotime.RUNNING_FORMAT = \'[RUNNING] {timespan} ({start})\'\n   # e.g. \'[FINISH] 4.02 s (2020-12-10T15:59:54~2020-12-10T15:59:58)\'\n   autotime.FINISHED_FORMAT = \'[FINISH] {timespan} ({start}~{end})\'\n   ```\n\n* Customize units.\n\n   ```python\n   # e.g. 5 分 7 秒\n   autotime.set_units(sec=\'秒\', min=\'分\', hr=\'時間\', d=\'日\')\n   ```\n\n* Customize output with method.\n\n   ```python\n   def my_format_output(timespan: float,\n                        start_time: time.struct_time,\n                        end_time: float = None,\n                        is_finished: bool = False):\n      """My Custom output format."""\n      if is_finished:\n         # e.g. \'Finished. 2.0160000000032596\'\n         return \'Finished. {}\'.format(timespan)\n      else:\n         # e.g. \'Running... 1.0159999999887077\'\n         return \'Running... {}\'.format(timespan)\n\n\n   autotime.format_output = my_format_output\n   ```\n\n   * You can access below objects on custom `format_output`.\n      * `autotime.UNITS (dict)`\n      * `autotime.format_time (method)`\n      * `autotime.TIME_FORMAT (str)`\n      * `autotime.RUNNING_FORMAT (str)`\n      * `autotime.FINISHED_FORMAT (str)`\n\n## Development\n\n* Requirements: poetry, pyenv\n\n```sh\npoetry install\n\npoetry publish\n\npip install --no-cache-dir --upgrade jupyter-autotime\n```\n',
    'author': 'Takeru Saito',
    'author_email': 'takelushi@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/takelushi/jupyter-autotime',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
