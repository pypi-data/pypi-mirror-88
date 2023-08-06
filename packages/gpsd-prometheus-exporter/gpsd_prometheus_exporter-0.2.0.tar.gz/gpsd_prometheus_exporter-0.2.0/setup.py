# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['gpsd_prometheus_exporter']

package_data = \
{'': ['*']}

install_requires = \
['argparse>=1.4.0,<2.0.0',
 'gps>=3.19,<4.0',
 'gpsd-py3>=0.3.0,<0.4.0',
 'prometheus-client>=0.9.0,<0.10.0']

entry_points = \
{'console_scripts': ['gpsd-exporter = gpsd_prometheus_exporter.main:main']}

setup_kwargs = {
    'name': 'gpsd-prometheus-exporter',
    'version': '0.2.0',
    'description': 'Monitor GPSD with Prometheus',
    'long_description': "# gpsd_prometheus_exporter\nPrometheus Exporter for GPSD\n\n## Prereqs\n* python\n* pip\n* USB GPS device compatible with gpsd\n* gpsd installed and running\n\nIt's a good idea to make sure that gpsd is working and reporting data. Verify\nusing gpsmon or similar:\n\n![gpsmon example output](img/gpsmon.png)\n\n## Usage Instructions\n\n```\ngpsd-exporter --help\n\nUsage: gpsd-exporter [OPTIONS]\n\nOptions:\n  -b, --bind TEXT     Specify alternate bind address [default: 0.0.0.0]\n  -p, --port INTEGER  Specify alternate port [default: 8000]\n  -d, --debug         Turns on more verbose logging, prints output [default:\n                      False]\n\n  --help              Show this message and exit.\n```\n### Example\n\nStart the exporter on all addresses and port 9999:\n\n```gpsd-exporter -b 0.0.0.0 -p 9999```\n\n\n### Adding this exporter to Prometheus\n```\n  - job_name: gps\n    static_configs:\n    - targets: ['boat-pi:8000']\n      labels:\n        group: 'gps'\n        location: 'Boat'\n```",
    'author': 'Mark S',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
