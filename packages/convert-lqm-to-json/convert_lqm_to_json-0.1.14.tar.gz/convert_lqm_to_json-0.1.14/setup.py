# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['convert_lqm_to_json']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['convert-lqm-to-json = convert_lqm_to_json.cli:main']}

setup_kwargs = {
    'name': 'convert-lqm-to-json',
    'version': '0.1.14',
    'description': 'Convert LG QuickMemo+ files into single, text-only JSON file',
    'long_description': '# Convert LG QuickMemo+ files into single, text-only JSON file\n\n[![Workflow](https://github.com/movecodemove/convert-lqm-to-json/workflows/.github/workflows/workflow.yml/badge.svg)](https://github.com/movecodemove/convert-lqm-to-json/actions)\n\n## Installation\n`$ pip install [--user] convert-lqm-to-json`\n\n## Usage\n`$ convert-lqm-to-json [-h] [-o [<...>]] [-v] [<source1>] ... [<sourceN>]`\n\n#### Arguments\n\n    <source>                Paths or glob patterns for resolving .lqm files;\n                            defaults to current directory.\n\n#### Options\n\n    -o  (--output-dir)      Output directory; defaults to current directory.\n    -h  (--help)            Print help message.\n    -v  (--version)         Print application version.\n',
    'author': 'Scott Steven Rodriguez',
    'author_email': 'scott@movecodemove.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/movecodemove/convert-lqm-to-json',
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
