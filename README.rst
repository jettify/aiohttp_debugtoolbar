aiohttp-debugtoolbar
====================
.. image:: https://travis-ci.org/aio-libs/aiohttp-debugtoolbar.svg?branch=master
    :target: https://travis-ci.org/aio-libs/aiohttp-debugtoolbar
    :alt: |Build status|
.. image:: https://codecov.io/gh/aio-libs/aiohttp-debugtoolbar/branch/master/graph/badge.svg
  :target: https://codecov.io/gh/aio-libs/aiohttp-debugtoolbar
    :alt: |Coverage status|
.. image:: https://img.shields.io/pypi/v/aiohttp-debugtoolbar.svg
    :target: https://pypi.python.org/pypi/aiohttp-debugtoolbar
    :alt: PyPI
.. image:: https://badges.gitter.im/Join%20Chat.svg
    :target: https://gitter.im/aio-libs/Lobby
    :alt: Chat on Gitter

**aiohttp_debugtoolbar** provides a debug toolbar for your aiohttp_
web application.  Library is port of pyramid_debugtoolbar_ and
still in early development stages. Basic functionality has been
ported:

* basic panels
* intercept redirects
* intercept and pretty print exception
* interactive python console
* show source code

.. image:: https://raw.githubusercontent.com/aio-libs/aiohttp_debugtoolbar/master/demo/aiohttp_debugtoolba_sceenshot.png


Ported Panels
-------------
``HeaderDebugPanel``, ``PerformanceDebugPanel``, ``TracebackPanel``,
``SettingsDebugPanel``, ``MiddlewaresDebugPanel``, ``VersionDebugPanel``,
``RoutesDebugPanel``,  ``RequestVarsDebugPanel``, ``LoggingPanel``


Help Needed
-----------
Are you coder looking for a project to contribute to
python/asyncio libraries? This is the project for you!


Install and Configuration
-------------------------
::

    $ pip install aiohttp_debugtoolbar


In order to plug in ``aiohttp_debugtoolbar``, call
``aiohttp_debugtoolbar.setup`` on your app.

.. code:: python

    import aiohttp_debugtoolbar
    app = web.Application(loop=loop)
    aiohttp_debugtoolbar.setup(app)

Note:

  This middleware needs a response that contains a valid HTML document to work.(i.e. *content_type: 'text/html'* and contains *</head>* and *</body>* tags.)


Full Example
------------

.. code:: python

    import asyncio
    import jinja2
    import aiohttp_debugtoolbar
    import aiohttp_jinja2

    from aiohttp import web


    @aiohttp_jinja2.template('index.html')
    async def basic_handler(request):
        return {'title': 'example aiohttp_debugtoolbar!',
                'text': 'Hello aiohttp_debugtoolbar!',
                'app': request.app}


    async def exception_handler(request):
        raise NotImplementedError


    async def init(loop):
        # add aiohttp_debugtoolbar middleware to you application
        app = web.Application(loop=loop)
        # install aiohttp_debugtoolbar
        aiohttp_debugtoolbar.setup(app)

        template = """
        <html>
            <head>
                <title>{{ title }}</title>
            </head>
            <body>
                <h1>{{ text }}</h1>
                <p>
                  <a href="{{ app.router['exc_example'].url() }}">
                  Exception example</a>
                </p>
            </body>
        </html>
        """
        # install jinja2 templates
        loader = jinja2.DictLoader({'index.html': template})
        aiohttp_jinja2.setup(app, loader=loader)

        # init routes for index page, and page with error
        app.router.add_route('GET', '/', basic_handler, name='index')
        app.router.add_route('GET', '/exc', exception_handler,
                             name='exc_example')
        return app


    loop = asyncio.get_event_loop()
    app = loop.run_until_complete(init(loop))
    web.run_app(app, host='127.0.0.1', port=9000)

Settings
--------
.. code:: python

    aiohttp_debugtoolbar.setup(app, hosts=['172.19.0.1', ])

Supported options


- enabled: The debugtoolbar is disabled if False. By default is set to True.
- intercept_redirects: If True, intercept redirect and display an intermediate page with a link to the redirect page. By default is set to True.
- hosts: The list of allow hosts. By default is set to ['127.0.0.1', '::1'].
- exclude_prefixes: The list of forbidden hosts. By default is set to [].
- check_host: If False, disable the host check and display debugtoolbar for any host. By default is set to True.
- max_request_history: The max value for storing requests. By default is set to 100.
- max_visible_requests: The max value of display requests. By default is set to 10.
- path_prefix: The prefix of path to debugtoolbar. By default is set to '/_debugtoolbar'.


Thanks!
-------

I've borrowed a lot of code from following projects. I highly
recommend to check them out:

* pyramid_debugtoolbar_
* django-debug-toolbar_
* flask-debugtoolbar_

Play With Demo
--------------

https://github.com/aio-libs/aiohttp_debugtoolbar/tree/master/demo

Requirements
------------

* aiohttp_
* aiohttp_jinja2_


.. _Python: https://www.python.org
.. _asyncio: http://docs.python.org/3/library/asyncio.html
.. _aiohttp: https://github.com/KeepSafe/aiohttp
.. _aiopg: https://github.com/aio-libs/aiopg
.. _aiomysql: https://github.com/aio-libs/aiomysql
.. _aiohttp_jinja2: https://github.com/aio-libs/aiohttp_jinja2
.. _pyramid_debugtoolbar: https://github.com/Pylons/pyramid_debugtoolbar
.. _django-debug-toolbar: https://github.com/django-debug-toolbar/django-debug-toolbar
.. _flask-debugtoolbar: https://github.com/mgood/flask-debugtoolbar
