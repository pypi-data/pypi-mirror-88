# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['riordinato']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'riordinato',
    'version': '1.0.0',
    'description': 'organize your files with prefixes',
    'long_description': "# Riordinato\n\nRiordinato is a python library for organizing files with prefixes.\n\n## Installation\n\nUse the package manager [pip](https://pip.pypa.io/en/stable/) to install riordinato.\n\n```bash\npip install riordinato \n```\n\n## Usage\n\n```python\nfrom riordinato.files import Organize\n\n# Example\n# Prefix: 'python'\n# destination folder: '/home/user/documents/pythonfiles'\nprefixes = [('<prefix>', '<destination folder>'),\n            ('<prefix>', '<destination folder>')]\n\n# this variable represents the location of the folder that riordinato is going to organize\ndir = '/home/user/any folder'\n\norganize = Organize(prefixes, dir)\n\n# Organize all files in the folder\norganize.organize_all()\n\n# organizes only files containing the specified prefix\norganize.organize_specific_files('<prefix>')\n\n\n```\n\n## Contributing\nAny pull request is welcome.\n\n## License\n[MIT](https://choosealicense.com/licenses/mit/)\n",
    'author': 'Dan-',
    'author_email': 'misternutel@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/DAN-pix/Riordinato',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
