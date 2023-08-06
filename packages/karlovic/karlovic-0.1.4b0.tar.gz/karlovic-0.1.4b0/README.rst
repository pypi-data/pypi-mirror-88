============
Model Server
============

NOTE: Currently in beta development. Breaking changes may happen at any time.

The Karlovic library aims to simplify the process of setting up a htts server that serves machine learning models.

Install
=======

.. code-block::

    pip install karlovic

Usage
=====

.. code-block:: python

    from karlovic import model_server

    def bottle_configuration_function(bottle):
      # Configure bottle
      pass

    plugins = [
      SomePlugin,
      ...
    ]

    app, run_server = model_server(plugins, bottle_configuration_function)

    # Use the app decorator to define endpoints
    @app.get('/hello')
    def hello():
      return "<h1>Hello World</h1>"

    @app.post('/world')
    def hello(image):
      return "some response"

    use_image_form(app, ['/world'])
    # Creates GET '/world/form' that posts an
    # image to '/world'

    run_server()

