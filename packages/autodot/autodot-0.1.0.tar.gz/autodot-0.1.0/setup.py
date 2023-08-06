# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['autodot']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'autodot',
    'version': '0.1.0',
    'description': 'Automated dotfile management using Python & Python/Click!',
    'long_description': '# autodot\n\n[![standard-readme compliant](https://img.shields.io/badge/readme%20style-standard-brightgreen.svg?style=flat-square)](https://github.com/RichardLitt/standard-readme) [![code style black](https://img.shields.io/badge/code%20style-black-%23000000)](https://github.com/psf/black) [![License MIT](https://img.shields.io/github/license/aubricus/autodot)](./LICENSE)\n\n_Automated dotfile management using Python & Python/Click!_\n\n## Background\n\nTODO: Update\n\n## Install\n\n### Dependencies\n\n- Python 3.6, 3.7, 3.8 ([pyenv] recommended)\n\n### Installation\n\n```bash\npip install -U autodot\n```\n\n## Usage\n\nSee the [documentation](https://aubricus.github.io/test_20200912_1/).\n\n```bash\n# TODO: Update\n```\n\n## Features\n\n- _TODO: Update_\n\n## Support\n\n- Python 3.6, 3.7, 3.8\n- MacOS: Tested locally, Python 3.8.2 via [pytest]\n- Linux: Ubuntu Latest, Python 3.6, 3.7, 3.8) via [GitHub Actions]\n- Windows: Not tested. ☹️\n\n## Maintainers\n\n-  [aubricus](https://github.com/aubricus)\n\n## Attribution\n\n- _TODO:Update_\n\n## Contributing\n\nIssues & pull-requests accepted. See the [CONTRIBUTING.md]\n\n_Small note: If editing the [README.md], please conform to the [standard-readme specification]._\n\n## License\n\n[MIT](./LICENSE) &copy; Aubrey Taylor 2020\n\n<!-- Links -->\n\n[setuptools]: https://setuptools.readthedocs.io/en/latest/\n[twine]: https://github.com/pypa/twine\n[pytest]: https://docs.pytest.org/en/latest/\n[tox]: https://tox.readthedocs.io/en/latest/\n[standard readme]: https://github.com/RichardLitt/standard-readme\n[black]: https://github.com/psf/black\n[pyenv]: https://github.com/pyenv/pyenv\n[github api]: https://developer.github.com/v3/licenses/\n[cookiecutter]: https://github.com/cookiecutter/cookiecutter\n[cookiecutter/cookiecutter]: https://github.com/cookiecutter/cookiecutter\n[aubricus/cookiecutter-cookiecutter]: https://github.com/aubricus/cookiecutter-cookiecutter\n[standard-readme specification]: https://github.com/RichardLitt/standard-readme\n[readme.md]: ./README.md\n[poetry]: https://python-poetry.org/docs/\n[contributing.md]: ./CONTRIBUTING.md\n[pydocstyle]: https://www.pydocstyle.org/en/stable/\n[editorconfig]: https://editorconfig.org/\n[toml]: https://toml.io/en/\n[github actions]: https://docs.github.com/en/actionss\n',
    'author': 'Aubrey Taylor',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/aubricus',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<3.9',
}


setup(**setup_kwargs)
