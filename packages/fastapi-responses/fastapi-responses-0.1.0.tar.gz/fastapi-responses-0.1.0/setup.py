# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fastapi_responses']

package_data = \
{'': ['*']}

install_requires = \
['fastapi>=0.62.0,<0.63.0']

setup_kwargs = {
    'name': 'fastapi-responses',
    'version': '0.1.0',
    'description': 'Extend OpenAPI schema to collect HTTPExceptions.',
    'long_description': '<h1 align="center">\n    <strong>FastAPI Responses</strong>\n</h1>\n<p align="center">\n    <a href="https://github.com/Kludex/fastapi-responses" target="_blank">\n        <img src="https://img.shields.io/github/last-commit/Kludex/fastapi-responses?style=for-the-badge" alt="Latest Commit">\n    </a>\n        <!-- <img src="https://img.shields.io/github/workflow/status/ycd/manage-fastapi/Test?style=for-the-badge"> -->\n        <img src="https://img.shields.io/codecov/c/github/Kludex/fastapi-responses?style=for-the-badge">\n    <br />\n    <!-- <a href="https://pypi.org/project/manage-fastapi" target="_blank">\n        <img src="https://img.shields.io/pypi/v/manage-fastapi?style=for-the-badge" alt="Package version">\n    </a> -->\n    <!-- <img src="https://img.shields.io/pypi/pyversions/manage-fastapi?style=for-the-badge"> -->\n    <img src="https://img.shields.io/github/license/Kludex/fastapi-responses?style=for-the-badge">\n</p>\n\n<p align="center">\n    This package is not stable. Do not use in production!\n</p>\n\nThe goal of this package is to have your responses up-to-date according to your exceptions.\n\n## Installation\n\n```bash\npip install fastapi-responses\n```\n\n## Usage\n\n```python\nfrom fastapi import FastAPI, HTTPException\nfrom fastapi_responses import custom_openapi\n\napp = FastAPI()\n\napp.openapi = custom_openapi\n\n@app.get("/{item_id}")\ndef get_item(item_id: int):\n    if item_id == 0:\n        raise HTTPException(status_code=404, detail="Item not found.")\n    return "Item exists!"\n```\n\n## license\n\nThis project is licensed under the terms of the MIT license.\n',
    'author': 'Marcelo Trylesinski',
    'author_email': 'marcelotryle@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Kludex/fastapi-responses',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
