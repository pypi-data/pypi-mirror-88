Django-Crashlog
===============

Ispired by django-db-log (https://github.com/dcramer/django-db-log),
intended to be used for small apps/local development.

Use Sentry (https://github.com/getsentry/sentry) for serious error logging.



Install
-------

configure your settings.py

.. code-block::python

    INSTALLED_APPS = (
        ....,
        'crashlog'
    )

    MIDDLEWARE_CLASSES = (
        ....,
        'crashlog.middleware.CrashLogMiddleware',
    )

See full doc at https://django-crashlog.readthedocs.io/en/develop/
