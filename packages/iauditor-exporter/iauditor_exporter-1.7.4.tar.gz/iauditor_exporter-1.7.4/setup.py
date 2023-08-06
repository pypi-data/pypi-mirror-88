# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['iauditor_exporter', 'iauditor_exporter.modules']

package_data = \
{'': ['*'],
 'iauditor_exporter': ['configs/config.yaml.sample',
                       'docs/Install-python/*',
                       'docs/css/*',
                       'docs/images/*',
                       'docs/index.md',
                       'docs/index.md',
                       'docs/install-intros/*',
                       'docs/javascripts/*',
                       'docs/requirements.txt',
                       'docs/requirements.txt',
                       'docs/script-download/*',
                       'docs/script-running/*',
                       'docs/script-setup/*',
                       'docs/understanding-the-data/*']}

install_requires = \
['PyYAML>=5.3.1,<6.0.0',
 'SQLAlchemy>=1.3.4',
 'coloredlogs>=10.0',
 'dateparser>=0.7.6,<0.8.0',
 'numpy>=1.16.4',
 'pandas>=0.24.2',
 'python_dateutil>=2.8.0',
 'pytz>=2019.2',
 'questionary>=1.5.2,<2.0.0',
 'rich>=4.2.2,<5.0.0',
 'safetyculture-sdk-python-beta>=2.2.3',
 'tqdm>=4.48.2,<5.0.0',
 'tzlocal>=2.0.0',
 'unicodecsv>=0.14.1']

extras_require = \
{'all_db': ['psycopg2>=2.8.5,<3.0.0',
            'mysqlclient>=2.0.1,<3.0.0',
            'pyodbc>=4.0.30,<5.0.0'],
 'mysql': ['mysqlclient>=2.0.1,<3.0.0'],
 'postgres': ['psycopg2>=2.8.5,<3.0.0'],
 'sql': ['pyodbc>=4.0.30,<5.0.0']}

entry_points = \
{'console_scripts': ['ia_exporter = iauditor_exporter.exporter:main']}

setup_kwargs = {
    'name': 'iauditor-exporter',
    'version': '1.7.4',
    'description': 'The iAuditor Exporter tool is the primary way to bulk export iAuditor information for use in BI tools such as PowerBI. The tool is coded in the Python programming language and can be ran simply and easily on any computer with Python installed.',
    'long_description': None,
    'author': 'Edd',
    'author_email': 'edward.abrahamsen-mills@safetyculture.io',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
