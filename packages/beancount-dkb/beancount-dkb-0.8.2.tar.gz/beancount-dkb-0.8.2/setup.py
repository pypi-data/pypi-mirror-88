# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['beancount_dkb']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'beancount-dkb',
    'version': '0.8.2',
    'description': 'Beancount Importer for DKB CSV exports',
    'long_description': "Beancount DKB Importer\n======================\n\n.. image:: https://github.com/siddhantgoel/beancount-dkb/workflows/beancount-dkb/badge.svg\n    :target: https://github.com/siddhantgoel/beancount-dkb/workflows/beancount-dkb/badge.svg\n\n.. image:: https://img.shields.io/pypi/v/beancount-dkb.svg\n    :target: https://pypi.python.org/pypi/beancount-dkb\n\n.. image:: https://img.shields.io/pypi/pyversions/beancount-dkb.svg\n    :target: https://pypi.python.org/pypi/beancount-dkb\n\n.. image:: https://img.shields.io/badge/code%20style-black-000000.svg\n    :target: https://github.com/psf/black\n\n:code:`beancount-dkb` provides an Importer for converting CSV exports of\nDKB_ (Deutsche Kredit Bank) account summaries to the Beancount_ format.\n\nInstallation\n------------\n\n.. code-block:: bash\n\n    $ pip install beancount-dkb\n\nIn case you prefer installing from the Github repository, please note that\n:code:`master` is the development branch so :code:`stable` is what you should be\ninstalling from.\n\nUsage\n-----\n\n.. code-block:: python\n\n    from beancount_dkb import ECImporter, CreditImporter\n\n    IBAN_NUMBER = 'DE99 9999 9999 9999 9999 99' # your real IBAN number\n\n    CARD_NUMBER = '9999 9999 9999 9999'         # your real Credit Card number\n\n    CONFIG = [\n        ECImporter(\n            IBAN_NUMBER,\n            'Assets:DKB:EC',\n            currency='EUR',\n            file_encoding='utf-8',\n        ),\n\n        CreditImporter(\n            CARD_NUMBER,\n            'Assets:DKB:Credit',\n            currency='EUR',\n            file_encoding='utf-8',\n        )\n    ]\n\nFAQ\n---\n\n.. code-block:: bash\n\n    ERROR:root:Importer beancount_dkb.ec.ECImporter.identify() raised an unexpected error: 'utf-8' codec can't decode byte 0xf6 in position 17: invalid start byte\n\nChange the :code:`file_encoding` parameter. It seems like the CSV exports are\n:code:`ISO-8859-1` encoded, but :code:`utf-8` seems like a useful default.\n\nContributing\n------------\n\nContributions are most welcome!\n\nPlease make sure you have Python 3.5+ and Poetry_ installed.\n\n1. Git clone the repository -\n   :code:`git clone https://github.com/siddhantgoel/beancount-dkb`\n\n2. Install the packages required for development -\n   :code:`poetry install`\n\n3. That's basically it. You should now be able to run the test suite -\n   :code:`poetry run py.test`.\n\n.. _Beancount: http://furius.ca/beancount/\n.. _DKB: https://www.dkb.de/\n.. _Poetry: https://poetry.eustace.io/\n",
    'author': 'Siddhant Goel',
    'author_email': 'me@sgoel.org',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/siddhantgoel/beancount-dkb',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.5,<4.0',
}


setup(**setup_kwargs)
