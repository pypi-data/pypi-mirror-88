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
    'version': '0.2.0',
    'description': 'Extend OpenAPI schema to collect HTTPExceptions.',
    'long_description': '<h1 align="center">\n    <strong>FastAPI Responses</strong>\n</h1>\n<p align="center">\n    <a href="https://github.com/Kludex/fastapi-responses" target="_blank">\n        <img src="https://img.shields.io/github/last-commit/Kludex/fastapi-responses" alt="Latest Commit">\n    </a>\n        <img src="https://img.shields.io/github/workflow/status/Kludex/fastapi-responses/Test">\n        <img src="https://img.shields.io/codecov/c/github/Kludex/fastapi-responses">\n    <br />\n    <a href="https://pypi.org/project/fastapi-responses" target="_blank">\n        <img src="https://img.shields.io/pypi/v/fastapi-responses" alt="Package version">\n    </a>\n    <img src="https://img.shields.io/pypi/pyversions/fastapi-responses">\n    <img src="https://img.shields.io/github/license/Kludex/fastapi-responses">\n</p>\n\n<p align="center">\n    <strong>This package is not stable. Do not use in production!</strong>\n</p>\n\nFind **HTTPException**s and turn them into documented **responses**. :tada:\n\n## Installation\n\n``` bash\npip install fastapi-responses\n```\n\n## Usage\n\nThe simplest use case happens when we have a single exception being raised. We don\'t want to document the possible response manually, so **FastAPI Responses** comes in handy.\n\n``` python\nfrom fastapi import FastAPI, HTTPException\nfrom fastapi_responses import custom_openapi\n\napp = FastAPI()\n\napp.openapi = custom_openapi(app)\n\n@app.get("/{item_id}")\ndef get_item(item_id: int):\n    if item_id == 0:\n        raise HTTPException(status_code=404, detail="Item not found.")\n    return "Item exists!"\n```\n\n### Without FastAPI Responses\n\n<img src="./assets/without.jpg" width="1000" title="Without FastAPI responses">\n\n### With FastAPI Responses\n\n<img src="./assets/with.jpg" width="1000" title="With FastAPI responses">\n\n## Roadmap\n\n- [X] Extract HTTPException from stack.\n- [ ] Extract any exception and document based on the `exception_handler` container.\n- [ ] Accept Python objects on `HTTPException` instantiation.\n\n## License\n\nThis project is licensed under the terms of the MIT license.\n',
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
