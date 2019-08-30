.. _logging:

Logging
=======

By default paperless logs to standard output and to the database. Logs can be browsed from the paperless web interface in the ``Log`` section.

Sentry
------

Paperless can be configured to send errors to the  `sentry.io`_ error tracking software by setting the ``PAPERLESS_SENTRY_DSN`` value in ``paperless.conf``.

.. _sentry.io: https://sentry.io/welcome/

Custom logger
-------------

Paperless support customizing the logging configuration by using a ``/etc/paperless/logging.yml`` file. This file should be in the yaml format and is passed without modification to the python logging ``dictConfig``. For more information
about the format see:

    - `Django logging documentation`_
    - `Python logging dictConfig documentation`_

.. _Django logging documentation: https://docs.djangoproject.com/en/2.1/topics/logging/
.. _Python logging dictConfig documentation: https://docs.python.org/3/library/logging.config.html#logging-config-dictschema

Examples
--------

Default
+++++++

.. code-block:: yaml

    version: 1
    disable_existing_loggers: False
    handlers:
        consumer:
            class: documents.loggers.PaperlessLogger
    loggers:
        documents:
            handlers:
                - consumer
            level: INFO

Send errors by email
++++++++++++++++++++

.. code-block:: yaml

    version: 1
    disable_existing_loggers: False
    handlers:
        consumer:
            class: documents.loggers.PaperlessLogger
        email:
            class: logging.handlers.SMTPHandler
            mailhost: localhost
            fromaddr: paperless@example.com
            toaddrs: 
                - foo@bar.com
            subject: oops!
            credentials:
                - root
                - hunter2
    loggers:
        documents:
            propagate: true
            handlers:
                - consumer
            level: INFO
    root:
        handlers:
            - email
        level: ERROR

Log debug to a file
+++++++++++++++++++

.. code-block:: yaml

    version: 1
    disable_existing_loggers: False
    handlers:
        consumer:
            class: documents.loggers.PaperlessLogger
        file:
            class: logging.handlers.RotatingFileHandler
            filename: paperless.log
            maxBytes: 100000000
    loggers:
        documents:
            propagate: true
            handlers:
                - consumer
            level: INFO
    root:
        handlers:
            - file
        level: DEBUG
