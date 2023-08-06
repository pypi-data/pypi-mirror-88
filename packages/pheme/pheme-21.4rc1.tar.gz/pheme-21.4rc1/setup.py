# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pheme',
 'pheme.parser',
 'pheme.scripts',
 'pheme.templatetags',
 'pheme.templatetags.charts',
 'pheme.transformation',
 'pheme.transformation.scanreport',
 'pheme.version']

package_data = \
{'': ['*']}

install_requires = \
['coreapi>=2.3.3,<3.0.0',
 'django==2.2.2',
 'djangorestframework==3.9.0',
 'matplotlib==3.0.2',
 'pyyaml>=5.3.1,<6.0.0',
 'rope>=0.17,<0.19',
 'uritemplate>=3.0.1,<4.0.0',
 'weasyprint>=51,<53',
 'xmltodict>=0.12.0,<0.13.0']

entry_points = \
{'console_scripts': ['pheme-parameter = pheme.scripts.parameter:main']}

setup_kwargs = {
    'name': 'pheme',
    'version': '21.4rc1',
    'description': 'report-generation-service',
    'long_description': '![Greenbone Logo](https://www.greenbone.net/wp-content/uploads/gb_logo_resilience_horizontal.png)\n\n# Pheme - Greenbone Static Report Generator <!-- omit in toc -->\n\n**pheme** is a service to create scan reports. It is maintained by [Greenbone Networks].\n\n[Pheme](https://en.wikipedia.org/wiki/Pheme) is the personification of fame and renown.\n\nOr in this case personification of a service to generate reports.\n\n## Table of Contents <!-- omit in toc -->\n\n- [Installation](#installation)\n  - [Requirements](#requirements)\n- [Development](#development)\n- [API overview](#api-overview)\n- [Maintainer](#maintainer)\n- [Contributing](#contributing)\n- [License](#license)\n\n## Installation\n\n### Requirements\n\nPython 3.7 and later is supported.\n\nBesides python `pheme` also needs to have\n\n- libcairo2-dev\n- pango1.0\n\ninstalled.\n\n## Development\n\n**pheme** uses [poetry] for its own dependency management and build\nprocess.\n\nFirst install poetry via pip\n\n    python3 -m pip install --user poetry\n\nAfterwards run\n\n    poetry install\n\nin the checkout directory of **pheme** (the directory containing the\n`pyproject.toml` file) to install all dependencies including the packages only\nrequired for development.\n\nAfterwards activate the git hooks for auto-formatting and linting via\n[autohooks].\n\n    poetry run autohooks activate\n\nValidate the activated git hooks by running\n\n    poetry run autohooks check\n\n## API overview\n\nTo get an overview of the API you can start this project\n\n```\npoetry run python manage.py runserver\n```\n\nand then go to [swagger](http://localhost:8000/docs/)\n\n## Usage\n\nIn order to prepare the data structure the XML report data needs to be posted to `pheme` with a grouping indicator (either by host or nvt).\n\nE.g.:\n\n```\n> curl -X POST \'http://localhost:8000/transform?grouping=nvt\'\\\n    -H \'Content-Type: application/xml\'\\\n    -H \'Accept: application/json\'\\\n    -d @test_data/longer_report.xml\n  \n  "scanreport-nvt-9a233b0d-713c-4f22-9e15-f6e5090873e3"⏎\n```\n\nThe returned identifier can be used to generate the actual report. \n\nSo far a report can be either in:\n- application/json\n- application/xml\n- text/csv\nE.g.\n\n```\n> curl -v \'http://localhost:8000/report/scanreport-nvt-9a233b0d-713c-4f22-9e15-f6e5090873e3\' -H \'Accept: application/csv\'\n```\n\nFor visual report like\n\n- application/pdf\n- text/html\n\nthe corresponding css and html template needs to be put into pheme first:\n\n```\n> curl -X PUT localhost:8000/parameter\\\n    -H \'x-api-key: SECRET_KEY_missing_using_default_not_suitable_in_production\'\\\n    --form vulnerability_report_html_css=@path_to_css_template\\\n    --form vulnerability_report_pdf_css=@path_to_css_template\\\n    --form vulnerability_report=@path_to_html_template\n```\n\nafterwards it can be get as usual:\n\n```\n> curl -v \'http://localhost:8000/report/scanreport-nvt-9a233b0d-713c-4f22-9e15-f6e5090873e3\' -H \'Accept: application/pdf\'\n```\n\n## Maintainer\n\nThis project is maintained by [Greenbone Networks GmbH][Greenbone Networks]\n\n## Contributing\n\nYour contributions are highly appreciated. Please\n[create a pull request](https://github.com/greenbone/pheme/pulls)\non GitHub. Bigger changes need to be discussed with the development team via the\n[issues section at GitHub](https://github.com/greenbone/pheme/issues)\nfirst.\n\n## License\n\nCopyright (C) 2020 [Greenbone Networks GmbH][Greenbone Networks]\n\nLicensed under the [GNU Affero General Public License v3.0 or later](LICENSE).\n\n[Greenbone Networks]: https://www.greenbone.net/\n[poetry]: https://python-poetry.org/\n[autohooks]: https://github.com/greenbone/autohooks\n',
    'author': 'Greenbone Networks GmbH',
    'author_email': 'info@greenbone.net',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
