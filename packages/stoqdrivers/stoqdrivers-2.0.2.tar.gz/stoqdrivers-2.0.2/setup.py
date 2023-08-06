# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['stoqdrivers',
 'stoqdrivers.devices',
 'stoqdrivers.printers',
 'stoqdrivers.printers.bematech',
 'stoqdrivers.printers.daruma',
 'stoqdrivers.printers.dataregis',
 'stoqdrivers.printers.elgin',
 'stoqdrivers.printers.epson',
 'stoqdrivers.printers.fiscnet',
 'stoqdrivers.printers.perto',
 'stoqdrivers.printers.snbc',
 'stoqdrivers.printers.sweda',
 'stoqdrivers.printers.tanca',
 'stoqdrivers.printers.virtual',
 'stoqdrivers.readers',
 'stoqdrivers.readers.barcode',
 'stoqdrivers.readers.barcode.metrologic',
 'stoqdrivers.scales',
 'stoqdrivers.scales.micheletti',
 'stoqdrivers.scales.toledo']

package_data = \
{'': ['*'],
 'stoqdrivers': ['conf/*',
                 'locale/*',
                 'locale/es_ES/LC_MESSAGES/stoqdrivers.po',
                 'locale/pt_BR/LC_MESSAGES/stoqdrivers.po']}

install_requires = \
['Pillow>=3.1.2',
 'pyserial>=2.2',
 'qrcode>=5.3,<5.4',
 'zope.interface>=4.0,<5.0']

setup_kwargs = {
    'name': 'stoqdrivers',
    'version': '2.0.2',
    'description': 'Drivers for the retail sector.',
    'long_description': None,
    'author': 'Stoq Team',
    'author_email': 'dev@stoq.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.5,<4.0',
}


setup(**setup_kwargs)
