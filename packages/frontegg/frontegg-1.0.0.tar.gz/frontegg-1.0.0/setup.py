# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['frontegg',
 'frontegg.baseConfig',
 'frontegg.fastapi',
 'frontegg.fastapi.secure_access',
 'frontegg.flask',
 'frontegg.flask.secure_access',
 'frontegg.helpers',
 'frontegg.sanic',
 'frontegg.sanic.secure_access']

package_data = \
{'': ['*']}

install_requires = \
['arrow>=0.15.5,<0.16.0',
 'cryptography>=3.1,<4.0',
 'pyjwt>=1.7.1,<2.0.0',
 'requests>=2.22.0,<3.0.0']

extras_require = \
{u'fastapi': ['fastapi'], u'flask': ['flask>=1.0,<2.0']}

setup_kwargs = {
    'name': 'frontegg',
    'version': '1.0.0',
    'description': 'Frontegg is a web platform where SaaS companies can set up their fully managed, scalable and brand aware - SaaS features and integrate them into their SaaS portals in up to 5 lines of code.',
    'long_description': '<p align="center">  \n  <a href="https://www.frontegg.com/" rel="noopener" target="_blank">  \n    <img style="margin-top:40px" height="50" src="https://frontegg.com/wp-content/uploads/2020/04/logo_frrontegg.svg" alt="Frontegg logo">  \n  </a>  \n</p>  \n<h1 align="center">Frontegg Python SDK</h1>  \n  \n  \n[Frontegg](https://frontegg.com/) is a web platform where SaaS companies can set up their fully managed, scalable and brand aware - SaaS features and integrate them into their SaaS portals in up to 5 lines of code.  \n  \n  \n## Installation  \nFrontegg python sdk is available as [pypi package](https://pypi.org/project/frontegg).   \n  \nBefore installing make sure that your app using python 3.  \n  \n```  \npip install frontegg  \n```  \n  ## Singing Up To Frontegg\nBefore you can start with frontegg, please make sure to [sign up](https://portal.frontegg.com/signup) in order to get your free account.\n\nAfter you signed up, you will be able to get your client ID and API key [here.](https://portal.frontegg.com/administration)\n  \n  \n## Supported Liberies\nFrontegg Slack SDK support the following liberies, and more to come:  \n  \n - [Flask](frontegg/flask)  \n - [FastAPI](frontegg/fastapi)  \n - [Sanic](frontegg/sanic)  \n  \n*If you could not find the libary you are looking for here, please [contact us](https://frontegg.com/contact) and let us know :)*  \n  \n## Debugging  \nFrontegg use the python 3 built in [loggin libary](https://docs.python.org/3/library/logging.html) to log useful debugging information.  \n  \nIn order to had those logs you can add the environment variable "FRONTEGG_DEBUG":  \n```  \nFRONTEGG_DEBUG=True  \n``` \nOr configure it in the app itself:  \n```  \nfrom frontegg import frontegg_logger  \nimport logging  \n  \nfrontegg_logger.setLevel(logging.DEBUG)  \n```',
    'author': 'Frontegg LTD',
    'author_email': 'hello@frontegg.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://frontegg.com/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
