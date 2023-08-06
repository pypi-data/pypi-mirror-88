# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['riordinato']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'riordinato',
    'version': '1.1.0',
    'description': 'organize your files with prefixes',
    'long_description': '# Riordinato\n\nRiordinato is a python library for organizing files with prefixes.\n\n## Installation\n\nUse the package manager [pip](https://pip.pypa.io/en/stable/) to install riordinato.\n\n```bash\npip install riordinato \n```\n\n## Usage\n\nRiordinato is used to organize files by prefixes. For example, we want to move the files that have python in their name to the python folder and similar with the files that have work.\n\n```\n/home/user/documents\n├── pythonWork.py\n├── python_examples.txt\n├── family.jpg\n├── dog.png\n├── index.html\n├── work_list.txt\n├── any_work.docx\n├── python_exercise.pdf\n├── work_for_later.docx\n│\n├── python/\n└── work/\n```\n\nFirst import riordinato\n\n```py\nfrom riordinato.files import Organize\n```\n\nThe prefixes are within a list where the first value is the name and the second the destination.\n\n```py\n            #  NAME            DESTINATION\nprefixes = [(\'python\', \'/home/user/documents/python\')\n            (\'work\', \'/home/user/documets/work\')]\n# You can also use windows directory syntax\n\n```\n\nWe define a directory where we have the files we want to move.\n\n```py\npath = \'/home/user/documents\'\n```\n\nWe create the instance.\n\n```py\norganize = Organize(prefixes, path)\n```\n\nIf you want to see the files that are in the path you can print the files attribute.\n\n```py\n>>> print(organize.files)\n\n[\'pythonWork.py\', \'python_examples.txt\', \'family.jpg\', \'dog.png\', \'index.html\', \n\'work_list.txt\', \'any_work.docx\', \'work_for_later.docx\', \'python_exercise.pdf\']\n```\n\nTo organize our files we use the moveFiles method\n\n```py\norganize.moveFiles()\n```\n\nAnd our directory would look like this.\n\n```\n/home/user/documents\n├── family.jpg\n├── dog.png\n├── index.html\n├── any_work.docx          \n│\n├── python/\n│   ├── python_exercise.pdf\n│   ├── pythonWork.py\n│   └── python_examples.txt\n└── work/\n    ├── work_for_later.docx\n    └── work_list.txt\n```\n\nIf we want to move files with a specific prefix, use the "specific" parameter of the method.\n\n```py\norganize.moveFiles(specific=\'python\')\n```\n\n```\n/home/user/documents\n├── family.jpg\n├── dog.png\n├── index.html\n├── work_list.txt\n├── work_for_later.docx\n├── any_work.docx\n│\n├── python/\n│   ├── python_exercise.pdf\n│   ├── pythonWork.py\n│   └── python_examples.txt\n└── work/\n    \n```\n\n## Contributing\nA contributing.md will be added soon.\n\n## License\n[MIT](https://choosealicense.com/licenses/mit/)\n',
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
