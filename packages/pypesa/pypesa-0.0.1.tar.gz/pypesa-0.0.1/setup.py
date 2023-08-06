# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pypesa']

package_data = \
{'': ['*']}

install_requires = \
['pycryptodome>=3.9.9,<4.0.0', 'requests>=2.25.0,<3.0.0']

setup_kwargs = {
    'name': 'pypesa',
    'version': '0.0.1',
    'description': 'Python Implementation for Mobile payments integrations.',
    'long_description': "# PyPesa\n\nPython Pesa SDK\n\n## Installation\n\nThis package is available in [Python Package Index](https://pypi.org/project/pyppesa/) and can be installed using `pip`\n\n```\npip install pypesa\n```\n\nThe package comprise both original open API codes and refactored codes.\n\nTo use original open API code import `open_api` module\n\n```\nfrom pypesa.open_api import APIContext, APIMethodType, APIRequest\n```\n\nTo use refactored code import `MPESA` from `vodacom` module.\n\n```\nfrom pypesa.vodacom import MPESA\n```\n\n## Features\n\n- [x] Customer-to-business\n- [x] Business-to-customer\n- [x] Business-to-business\n- [x] Reversal\n- [x] Transaction status\n\n## Pre-requisites\n\nThe following are required and are obtained from [Vodacom Open Api portal](https://openapiportal.m-pesa.com/login)\n\n- Api Key\n- Public Key\n\n## Examples\n\n### Customer to Business payment via vodacom m-pesa\n\n```python\n# vodacom M-PESA\nfrom mobile_payments.vodacom import MPESA\n\napi_key = '<your-api-key>'\npublic_key = '<open-api-public-key>'\n\nm_pesa = MPESA(api_key=api_key, public_key=public_key)\n\n# Customer to Business payment\nparameters = {\n    'input_Amount': '1000', # amount to be charged\n    'input_Country': 'TZN',\n    'input_Currency': 'TZS',\n    'input_CustomerMSISDN': '000000000001',\n    'input_ServiceProviderCode': '000000',\n    'input_ThirdPartyConversationID': 'c9e794e10c63479992a8b08703abeea36',\n    'input_TransactionReference': 'T23434ZE3',\n    'input_PurchasedItemsDesc': 'Shoes',\n}\n\nresponse = m_pesa.customer2business(parameters)\n```\n\n## License\n\nCode released under [MIT LICENSE](https://github.com/openpesa/pypesa/blob/main/LICENSE)\n",
    'author': 'Innocent Zenda',
    'author_email': 'zendainnocent@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/openpesa/pypesa.git',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
