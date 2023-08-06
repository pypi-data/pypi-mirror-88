.. _index:

===================
Django Crashlog
===================

Django application to log into the database any Exception that occurs into the application.
Each exception is available in the Admin, with the same layout of the Django debug page


Install
=======

configure your `settings.py`, add `CrashLogMiddleware` after `AuthenticationMiddleware`::

    INSTALLED_APPS = (
        ....,
        'crashlog'
    )


    MIDDLEWARE_CLASSES = (
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'crashlog.middleware.CrashLogMiddleware',
    )

Manually log exception
======================
::

    try:
        ...
    except Exception as e:
        process_Exception(e)


Ignore some Exceptions
======================

To skip logging of specific exception, configure your ``settings`` as below::


    CRASHLOG_IGNORE_EXCEPTIONS = ('module.name.Exception',)


Changelog
=========

.. toctree::
:maxdepth: 2


        changes

