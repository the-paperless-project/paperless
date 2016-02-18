.. _setup:

Setup
=====

Paperless isn't a very complicated app, but there are a few components, so some
basic documentation is in order.  If you go follow along in this document and
still have trouble, please open an `issue on GitHub`_ so I can fill in the gaps.

.. _issue on GitHub: https://github.com/danielquinn/paperless/issues


.. _setup-download:

Download
--------

The source is currently only available via GitHub, so grab it from there, either
by using ``git``:

.. code:: bash

    $ git clone https://github.com/danielquinn/paperless.git
    $ cd paperless

or just download the tarball and go that route:

.. code:: bash

    $ wget https://github.com/danielquinn/paperless/archive/master.zip
    $ unzip master.zip
    $ cd paperless-master


.. _setup-installation:

Installation & Configuration
----------------------------

You can go two routes with setting up and running Paperless.  The *Vagrant*
route is quick & easy, but means you're running a VM which comes with memory
consumption etc.  Alternatively the standard, "bare metal" approach is a little
more complicated.


.. _setup-installation-standard:

Standard (Bare Metal)
.....................

1. Install the requirements as per the :ref:`requirements <requirements>` page.
2. Change to the ``src`` directory in this repo.
3. Edit ``paperless/settings.py`` and be sure to set the values for:
    * ``CONSUMPTION_DIR``: this is where your documents will be dumped to be
      consumed by Paperless.
    * ``PASSPHRASE``: this is the passphrase Paperless uses to encrypt/decrypt
      the original document.  The default value attempts to source the
      passphrase from the environment, so if you don't set it to a static value
      here, you must set ``PAPERLESS_PASSPHRASE=some-secret-string`` on the
      command line whenever invoking the consumer or webserver.
    * ``OCR_THREADS``: this is the number of threads the OCR process will spawn
      to process document pages in parallel. The default value gets sourced from
      the environment-variable ``PAPERLESS_OCR_THREADS`` and expects it to be an
      integer. If the variable is not set, Python determines the core-count of
      your CPU and uses that value.
4. Initialise the database with ``./manage.py migrate``.
5. Create a user for your Paperless instance with
   ``./manage.py createsuperuser``. Follow the prompts to create your user.
6. Start the webserver with ``./manage.py runserver <IP>:<PORT>``.
   If no specifc IP or port are given, the default is ``127.0.0.1:8000``.
   You should now be able to visit your (empty) `Paperless webserver`_ at
   ``127.0.0.1:8000`` (or whatever you chose).  You can login with the
   user/pass you created in #5.
7. In a separate window, change to the ``src`` directory in this repo again, but
   this time, you should start the consumer script with
   ``./manage.py document_consumer``.
8. Scan something.  Put it in the ``CONSUMPTION_DIR``.
9. Wait a few minutes
10. Visit the document list on your webserver, and it should be there, indexed
    and downloadable.

.. _Paperless webserver: http://127.0.0.1:8000


.. _setup-installation-vagrant:

Vagrant Method
..............

1. Install `Vagrant`_.  How you do that is really between you and your OS.
2. Run ``vagrant up``.  An instance will start up for you.  When it's ready and
   provisioned...
3. Run ``vagrant ssh`` and once inside your new vagrant box, edit
   ``/opt/paperless/src/paperless/settings.py`` and set the values for:
    * ``CONSUMPTION_DIR``: this is where your documents will be dumped to be
      consumed by Paperless.
    * ``PASSPHRASE``: this is the passphrase Paperless uses to encrypt/decrypt
      the original document.  The default value attempts to source the
      passphrase from the environment, so if you don't set it to a static value
      here, you must set ``PAPERLESS_PASSPHRASE=some-secret-string`` on the
      command line whenever invoking the consumer or webserver.
4. Initialise the database with ``/opt/paperless/src/manage.py migrate``.
5. Still inside your vagrant box, create a user for your Paperless instance with
   ``/opt/paperless/src/manage.py createsuperuser``. Follow the prompts to
   create your user.
6. Start the webserver with ``/opt/paperless/src/manage.py runserver 0.0.0.0:8000``.
   You should now be able to visit your (empty) `Paperless webserver`_ at
   ``172.28.128.4:8000``.  You can login with the user/pass you created in #5.
7. In a separate window, run ``vagrant ssh`` again, but this time once inside
   your vagrant instance, you should start the consumer script with
   ``/opt/paperless/src/manage.py document_consumer``.
8. Scan something.  Put it in the ``CONSUMPTION_DIR``.
9. Wait a few minutes
10. Visit the document list on your webserver, and it should be there, indexed
    and downloadable.

.. _Vagrant: https://vagrantup.com/
.. _Paperless server: http://172.28.128.4:8000

.. _setup-installation-docker:

Docker Method
.............

1. Install `Docker`_.
2. Run ``docker build -t paperless .``. Get a cup of coffee as the image builds for the first time.
3. Run ``docker run -d -p 8000:8000 paperless`` then navigate to https://localhost:8000

The Docker image supports the following environment variables. These variables can be passed into the ``docker run`` command above with the ``-e MY_VAR my_value`` flag.

- PAPERLESS_PASSPHRASE (default: some-secret-string)
- CONSUMPTION_DIR (default: /opt/consumption)
- USERNAME (default: admin)
- EMAIL (default: admin@example.com)
- PASSWORD (default: paperless)

.. _Docker: https://www.docker.com/

.. _making-things-a-little-more-permanent:

Making Things a Little more Permanent
-------------------------------------

Once you've tested things and are happy with the work flow, you can automate the
process of starting the webserver and consumer automatically.  If you're running
on a bare metal system that's using Systemd, you can use the service unit files
in the ``scripts`` directory to set this up.  If you're on a SysV or other
startup system (like the Vagrant box), then you're currently on your own.
