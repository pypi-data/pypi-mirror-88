# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sphinx_revealjs', 'sphinx_revealjs.themes']

package_data = \
{'': ['*'],
 'sphinx_revealjs.themes': ['sphinx_revealjs/*',
                            'sphinx_revealjs/static/.gitignore']}

install_requires = \
['docutils', 'sphinx']

setup_kwargs = {
    'name': 'sphinx-revealjs',
    'version': '0.12.1',
    'description': 'Sphinx extension with theme to generate Reveal.js presentation',
    'long_description': "sphinx-revealjs\n===============\n\n.. image:: https://img.shields.io/pypi/v/sphinx-revealjs.svg\n    :target: https://pypi.org/project/sphinx-revealjs/\n\n.. image:: https://github.com/attakei/sphinx-revealjs/workflows/Testings/badge.svg\n    :target: https://github.com/attakei/sphinx-revealjs/actions\n\n.. image:: https://travis-ci.org/attakei/sphinx-revealjs.svg?branch=master\n    :target: https://travis-ci.org/attakei/sphinx-revealjs\n\n\nSphinx extention with theme to generate Reveal.js presentation\n\nOrverview\n---------\n\nThis extension generate Reveal.js presentation\nfrom **standard** reStructuredText.\n\nIt include theses features.\n\n* Custom builder to translate from reST to reveal.js style HTML\n* Template to be enable to render presentation local imdependent\n\nInstallation\n------------\n\n.. code-block:: bash\n\n    $ pip install sphinx-revealjs\n\n\nUsage\n-----\n\n1. Create your sphinx documentation\n2. Edit `conf.py` to use this extension\n\n    .. code-block:: python\n\n        extensions = [\n            'sphinx_revealjs',\n        ]\n\n3. Write source for standard document style\n\n4. Build sources as Reveal.js presentation\n\n    .. code-block:: bash\n\n        $ make revealjs\n\nChange logs\n-----------\n\nSee `it <./CHANGES.rst>`_\n\nFutures\n-------\n\n* Index template as none presentation\n* CDN support\n\nContributings\n-------------\n\nGitHub repository does not have reveal.js library.\n\nIf you use from GitHub and editable mode, Run ``tools/fetch_revealjs.py`` after install.\n\n.. code-block:: bash\n\n    $ git clone https://github.com/attakei/sphinx-revealjs\n    $ cd sphinx-revealjs\n    $ poetry install\n    $ poetry run python tools/fetch_revealjs.py\n\nCopyright\n---------\n\nApache-2.0 license. Please see `LICENSE <./LICENSE>`_.\n",
    'author': 'Kazuya Takei',
    'author_email': 'myself@attakei.net',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/attakei/sphinx-revealjs',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
