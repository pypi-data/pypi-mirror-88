# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sphinx_guru_builder']

package_data = \
{'': ['*'], 'sphinx_guru_builder': ['theme/*']}

install_requires = \
['pyaml>=20.4.0,<21.0.0']

setup_kwargs = {
    'name': 'sphinx-guru-builder',
    'version': '0.1.1',
    'description': 'Sphinx Builder for Guru',
    'long_description': '# sphinx-guru-builder\n\n## Installation\n\n```\n$ pip install sphinx-guru-builder\n```\n\n## Usage\n\n1. Add the extension to your `conf.py`.\n\n```py\nextensions = [\n    "sphinx_guru_builder",\n]\n```\n\n2. Optionally, add `html_published_location` to create a link on each page to\n   the original docs.\n\n```py\nhtml_published_location = "https://example.com/docs"`\n```\n\n3. Build your docs.\n\n```\n$ sphinx-build -b guru source_dir build_dir\n```\n\n4. Upload the generated `guru.zip` file in the parent directory of the\n   `build_dir`.\n\nSee [Guru API docs](https://developer.getguru.com/docs/guru-sync-manual-api) for instruction on how to upload the archive.\n',
    'author': 'Jean-Martin Archer',
    'author_email': 'jm@jmartin.ca',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/j-martin/sphinx-guru-builder',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
