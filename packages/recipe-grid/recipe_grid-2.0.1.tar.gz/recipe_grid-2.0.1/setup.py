# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['recipe_grid',
 'recipe_grid.parser',
 'recipe_grid.renderer',
 'recipe_grid.scripts',
 'recipe_grid.static_site',
 'recipe_grid.static_site.templates']

package_data = \
{'': ['*']}

install_requires = \
['jinja2>=2.11.2,<3.0.0',
 'lxml>=4.6.1,<5.0.0',
 'marko>=0.9.1,<0.10.0',
 'peggie>=0.2.0,<0.3.0']

entry_points = \
{'console_scripts': ['recipe-grid = recipe_grid.scripts.recipe_grid:main',
                     'recipe-grid-lint = '
                     'recipe_grid.scripts.recipe_grid_lint:main',
                     'recipe-grid-site = '
                     'recipe_grid.scripts.recipe_grid_site:main']}

setup_kwargs = {
    'name': 'recipe-grid',
    'version': '2.0.1',
    'description': 'A tool for generating table-based recipe descriptions.',
    'long_description': None,
    'author': 'Jonathan Heathcote',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/mossblaser/recipe_grid',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
