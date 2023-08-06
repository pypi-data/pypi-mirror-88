=================
threedi-ws-client
=================


.. image:: https://img.shields.io/pypi/v/threedi-ws-client.svg
        :target: https://pypi.python.org/pypi/threedi_ws_client

.. image:: https://img.shields.io/travis/larsclaussen/threedi-ws-client.svg
        :target: https://travis-ci.org/larsclaussen/threedi_ws_client

.. image:: https://readthedocs.org/projects/threedi-ws-client/badge/?version=latest
        :target: https://threedi-ws-client.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status


Quick start
-----------

Create a virtual python > 3.6 environment, run::

    pip install -r requirements.txt

The `active_simulations` command takes a required keyword argument `--env` with
the options

- prod (production obviously)
- stag (staging obviously)
- local

You have to create a corresponding `.env` file for the destination environment.
The `prod.env` file could look something like this::

    API_USERNAME='micheal.jackson'
    API_PASSWORD='sefdiee92u43dmslzxsad'
    API_HOST='https://api.3di.live/v3.0'


To start the client run::

    python threedi_ws_client/commands/active_simulations.py --env=<prod | stag | local>

* Free software: MIT license
* Documentation: https://threedi-ws-client.readthedocs.io.


Features
--------

* TODO

Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
