# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fastapi_template',
 'fastapi_template.template.hooks',
 'fastapi_template.template.{{cookiecutter.project_name}}',
 'fastapi_template.template.{{cookiecutter.project_name}}.migrations',
 'fastapi_template.template.{{cookiecutter.project_name}}.migrations.versions',
 'fastapi_template.template.{{cookiecutter.project_name}}.src',
 'fastapi_template.template.{{cookiecutter.project_name}}.src.api',
 'fastapi_template.template.{{cookiecutter.project_name}}.src.api.dummy_db',
 'fastapi_template.template.{{cookiecutter.project_name}}.src.api.httpbin',
 'fastapi_template.template.{{cookiecutter.project_name}}.src.api.redis_api',
 'fastapi_template.template.{{cookiecutter.project_name}}.src.models',
 'fastapi_template.template.{{cookiecutter.project_name}}.src.services',
 'fastapi_template.template.{{cookiecutter.project_name}}.src.services.db',
 'fastapi_template.template.{{cookiecutter.project_name}}.src.services.elastic',
 'fastapi_template.template.{{cookiecutter.project_name}}.src.services.httpbin',
 'fastapi_template.template.{{cookiecutter.project_name}}.tests']

package_data = \
{'': ['*'],
 'fastapi_template': ['template/*'],
 'fastapi_template.template.{{cookiecutter.project_name}}': ['envs/*',
                                                             'systemd/*']}

install_requires = \
['cookiecutter>=1.7.2,<2.0.0',
 'pre-commit>=2.8.2,<3.0.0',
 'pygit2>=1.4.0,<2.0.0',
 'termcolor>=1.1.0,<2.0.0']

entry_points = \
{'console_scripts': ['fastapi_template = fastapi_template.main:main']}

setup_kwargs = {
    'name': 'fastapi-template',
    'version': '1.2.2',
    'description': 'Feature-rich robust FastAPI template',
    'long_description': '![python version](https://img.shields.io/pypi/pyversions/fastapi_template?style=flat-square) ![Build status](https://img.shields.io/github/workflow/status/s3rius/FastAPI-template/Release%20python%20package?style=flat-square) [![version](https://img.shields.io/pypi/v/fastapi_template?style=flat-square)](https://pypi.org/project/fastapi-template/)\n\n<div align="center">\n<img src="https://raw.githubusercontent.com/s3rius/FastAPI-template/master/images/logo.png" width=700>\n<div><i>Fast and flexible general-purpose template for your API.</i></div>\n</div>\n\n\n## Usage\n⚠️ [Git](https://git-scm.com/downloads), [Python](https://www.python.org/), and [Docker-compose](https://docs.docker.com/compose/install/) must be installed and accessible ⚠️\n\n```bash\npython3 -m pip install fastapi_template\nfastapi_template\n# Answer prompts questions\n# ???\n# 🍪 Enjoy your new project 🍪\ncd new_project\ndocker-compose up --build\n```\n\n## Features\nCurrently supported features:\n- redis\n- systemd units\n- Example (dummy) SQLAlchemy model\n- Elastic Search support\n- Scheduler support\n',
    'author': 'Pavel Kirilin',
    'author_email': 'win10@list.ru',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/s3rius/FastAPI-template',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
