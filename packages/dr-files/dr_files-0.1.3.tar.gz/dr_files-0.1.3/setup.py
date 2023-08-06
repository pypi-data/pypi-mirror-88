# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['dr_files', 'dr_files.pb']

package_data = \
{'': ['*']}

install_requires = \
['nptdms>=1.1.0,<2.0.0',
 'numpy>=1.18.2,<2.0.0',
 'protobuf>=3.11.3,<4.0.0',
 'scipy>=1.4.1,<2.0.0']

setup_kwargs = {
    'name': 'dr-files',
    'version': '0.1.3',
    'description': 'Read and convert Mechbase files (.dr) to known file formats',
    'long_description': '# DR Files\n\nRead and convert MECHBASE files (.dr) to known file formats\n\n## MECHBASE\n\n[MECHBASE](https://arpedon.com/products/mechbase/)® is a complete preventive solution that was developed by [Arpedon, P.C.](https://arpedon.com/), in order to help you store and trend your equipment status.\n\n## MECHBASE files format\n\nMECHBASE files have the following structure:\n\n* 2 bytes - the size of the header in bytes, in little-endian short integer format\n* next N bytes - the header, in [this protobuf format](pb/headers_pb2.proto)\n* remaining bytes - the values of the signals, with each value represented in 2 bytes, like below (signal has 3 channels in this example):\n    * next 2 bytes - first value of the first channel, in little-endian short integer format\n    * next 2 bytes - first value of the second channel, in little-endian short integer format\n    * next 2 bytes - first value of the third channel, in little-endian short integer format\n    * next 2 bytes - second value of the first channel, in little-endian short integer format\n    * next 2 bytes - second value of the second channel, in little-endian short integer format\n    * next 2 bytes - second value of the third channel, in little-endian short integer format\n    * ...\n\n### Converting values to actual measured values\n\n* divide the value by the maximum short value (32767)\n* multiply the value with the channel reference value\n* add the channel offset to the value\n* multiply the value with 1000 and divide by the channel sensitivity value\n* if channel db_reference exists and is positive\n    * multiply the log10 of the absolute value divided by the db_reference with 20 - `20 * log10(abs(value) / db_reference)`\n    * add the channel pregain to the value\n\nReference code can be found in the `value_converter` function.\n',
    'author': 'Antonis Kalipetis',
    'author_email': 'akalipetis@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
