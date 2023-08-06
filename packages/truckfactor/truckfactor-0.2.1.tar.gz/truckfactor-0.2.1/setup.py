# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['truckfactor']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.19.4,<2.0.0', 'pandas>=1.1.5,<2.0.0']

entry_points = \
{'console_scripts': ['truckfactor = truckfactor.compute:run']}

setup_kwargs = {
    'name': 'truckfactor',
    'version': '0.2.1',
    'description': ' Tool to compute the truck factor of a Git repository ',
    'long_description': '# What is this?\n\nThis tool, `truckfactor` computes the \n[truck (bus/lorry/lottery) factor](https://en.wikipedia.org/wiki/Bus_factor) for a \ngiven Git repository.\n\nThe truck factor is\n\n  > the number of people on your team that have to be hit by a truck (or quit) \n  > before the project is in serious trouble\n  >\n  > L. Williams and R. Kessler, Pair Programming Illuminated. Addison Wesley, 2003.\n\nOne of the earliest occurrences of the term in a real project was in the Python\nmailing list: \n["If Guido was hit by a bus?"](https://legacy.python.org/search/hypermail/python-1994q2/1040.html)\n\n\n## Installation\n\n```\npip install truckfactor\n```\n\n### Requirements\n\nThe tool requires that `git` is installed and accessible on `PATH`.\n\n\n## How to use it?\n\nYou have to either point the tool to a directory containing a Git repository or\nto a URL with a remote repository. In case a URL is given, the tool will clone\nthe repository into a temporary directory.\n\nFrom the terminal, the tool can be run as in the following:\n\n```bash\n$ truckfactor <path_or_url_to_repository>\nThe truck factor of <path_to_repository> is: <number>\n```\n\nFor now, it just returns on line of text ending in the number of the truck \nfactor for that repository.\n\n\nCalling it from code:\n\n```python\nfrom truckfactor.compute import main\n\n\ntruckfactor = main("<path_to_repo>")\n```\n\n\n# How does the tool compute the truck factor?\n\nIn essence the tool does the following:\n\n  * Reads a git log from the repository\n  * Computes for each file who has the _knowledge ownership_ of it.\n    - A contributor has knowledge ownership of a file when she edited the most \n    lines in it.\n    - That computation is inspired by \n    [A. Thornhill _Your Code as a Crime Scene_](https://pragprog.com/titles/atcrime/your-code-as-a-crime-scene/).\n    - Note, only for text files knowledge ownership is computed. The tool may \n    not, return a good answer for repositories containing only binary files.\n  * Then similar to [G. Avelino et al. *A novel approach for estimating Truck Factors*](https://peerj.com/preprints/1233.pdf) \n  low-contributing authors are removed from the analysis as long as still more \n  than half of all files have a knowledge owner. The amount of remaining \n  knowledge owners is the truck factor of the given repository.\n',
    'author': 'HelgeCPH',
    'author_email': 'ropf@itu.dk',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/HelgeCPH/truckfactor',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
