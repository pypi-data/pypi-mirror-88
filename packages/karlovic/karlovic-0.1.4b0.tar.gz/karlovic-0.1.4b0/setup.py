# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['karlovic', 'karlovic.forms', 'karlovic.plugins']

package_data = \
{'': ['*']}

install_requires = \
['Pillow>=7.1.0',
 'bottle>=0.12.18',
 'cheroot>=8.3.0',
 'jaraco.functools>=3.0.0']

setup_kwargs = {
    'name': 'karlovic',
    'version': '0.1.4b0',
    'description': 'Can only serve machine learning models.',
    'long_description': '============\nModel Server\n============\n\nNOTE: Currently in beta development. Breaking changes may happen at any time.\n\nThe Karlovic library aims to simplify the process of setting up a htts server that serves machine learning models.\n\nInstall\n=======\n\n.. code-block::\n\n    pip install karlovic\n\nUsage\n=====\n\n.. code-block:: python\n\n    from karlovic import model_server\n\n    def bottle_configuration_function(bottle):\n      # Configure bottle\n      pass\n\n    plugins = [\n      SomePlugin,\n      ...\n    ]\n\n    app, run_server = model_server(plugins, bottle_configuration_function)\n\n    # Use the app decorator to define endpoints\n    @app.get(\'/hello\')\n    def hello():\n      return "<h1>Hello World</h1>"\n\n    @app.post(\'/world\')\n    def hello(image):\n      return "some response"\n\n    use_image_form(app, [\'/world\'])\n    # Creates GET \'/world/form\' that posts an\n    # image to \'/world\'\n\n    run_server()\n\n',
    'author': 'Aiwizo',
    'author_email': 'filip@aiwizo.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/aiwizo/karlovic',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
