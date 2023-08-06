# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['xact',
 'xact._meta',
 'xact.cfg',
 'xact.cfg._meta',
 'xact.cfg.data',
 'xact.cfg.data._meta',
 'xact.cli',
 'xact.cli._meta',
 'xact.gen',
 'xact.gen._meta',
 'xact.host',
 'xact.host._meta',
 'xact.log',
 'xact.node',
 'xact.node._meta',
 'xact.proc',
 'xact.proc._meta',
 'xact.queue',
 'xact.queue._meta',
 'xact.sys',
 'xact.sys._meta',
 'xact.sys.orchestration',
 'xact.util',
 'xact.util._meta']

package_data = \
{'': ['*']}

install_requires = \
['Jinja2>=2.1',
 'ansible==2.9.13',
 'click',
 'cryptography',
 'dill',
 'jsonschema',
 'loguru',
 'numpy',
 'paramiko',
 'psutil>=5.0',
 'pytest>=5.2',
 'pyyaml',
 'pyzmq',
 'setproctitle',
 'toml',
 'xmltodict']

entry_points = \
{'console_scripts': ['xact = xact.cli.command:grp_main']}

setup_kwargs = {
    'name': 'xact',
    'version': '0.0.3.dev0',
    'description': 'Model based design for developers',
    'long_description': 'XACT: Model based design for developers\n#######################################\n\nXact is a tool for configuring and deploying software intensive systems,\nfrom simulations running on cloud infrastructure to distributed intelligent\nsensing systems running on edge devices.\n\nXact defines a unified configuration data structure for specifying component\ndependencies and for configuring various types of messaging middleware,\nenabling distributed dataflow systems to be rapidly and conveniently\ndescribed and deployed.\n\nIt is intended to support model based systems and software engineering\nprocesses and to be a foundation for future design automation tools.\n',
    'author': 'William Payne',
    'author_email': 'will@xplain.systems',
    'maintainer': 'William Payne',
    'maintainer_email': 'will@xplain.systems',
    'url': 'http://xplain.systems',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6.1',
}


setup(**setup_kwargs)
