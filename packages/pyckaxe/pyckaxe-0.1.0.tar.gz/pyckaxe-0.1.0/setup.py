# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyckaxe',
 'pyckaxe.abc',
 'pyckaxe.blocks',
 'pyckaxe.command',
 'pyckaxe.command.abc',
 'pyckaxe.commands',
 'pyckaxe.commands._root',
 'pyckaxe.pack',
 'pyckaxe.pack.resource',
 'pyckaxe.pack.resource.abc',
 'pyckaxe.pack.resource.function',
 'pyckaxe.pack.resource.loot_table',
 'pyckaxe.pack.resource.structure',
 'pyckaxe.utils']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'pyckaxe',
    'version': '0.1.0',
    'description': 'An expressive Minecraft utility library revolving around data manipulation and generation.',
    'long_description': '![logo]\n\n# pyckaxe\nAn expressive Minecraft utility library revolving around data manipulation and generation.\n\n[![build-badge-master]](https://travis-ci.org/Arcensoth/pyckaxe)\n[![quality-badge-master]](https://app.codacy.com/project/Arcensoth/pyckaxe/dashboard)\n[![coverage-badge-master]](https://codecov.io/gh/Arcensoth/pyckaxe/branch/master)\n[![package-badge]](https://pypi.python.org/pypi/pyckaxe/)\n[![version-badge]](https://pypi.python.org/pypi/pyckaxe/)\n[![style-badge]](https://github.com/ambv/black)\n\nYou may be interested in `pyckaxe` if you:\n\n- are a technical/creative player, or\n- make adventure maps or minigames, or\n- use command/data generators, or\n- write your own generators, or\n- work on large/complex projects, or\n- just want to over-engineer something.\n\nThe goal of `pyckaxe` is to provide a flexible suite of development tools for technical Minecraft players:\n\n- A complete hierarchy of **commands** and their subcommands, as well as frequently used **selectors** and **positions** to go along with them.\n- A thorough collection of game object and **data tag (NBT)** representations, for things like **blocks**, **items**, and **entities**.\n- Auto-completion, argument suggestion, and type validation for all representations.\n- Utilities for building datapacks and resources via custom-written generators.\n\n[logo]: https://i.imgur.com/FkxD7fJ.png\n[build-badge-master]: https://img.shields.io/travis/Arcensoth/pyckaxe/master.svg?label=build\n[quality-badge-master]: https://img.shields.io/codacy/grade/a01ea39de1ed48319c18365ad5545f65/master.svg?label=quality\n[coverage-badge-master]: https://img.shields.io/codecov/c/github/Arcensoth/pyckaxe/master.svg?label=coverage\n[package-badge]: https://img.shields.io/pypi/v/pyckaxe.svg\n[version-badge]: https://img.shields.io/pypi/pyversions/pyckaxe.svg\n[style-badge]: https://img.shields.io/badge/code%20style-black-000000.svg\n',
    'author': 'Arcensoth',
    'author_email': 'arcensoth@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Arcensoth/pyckaxe',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
