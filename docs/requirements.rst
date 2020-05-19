.. _requirements:

Requirements
============

You need a Linux machine or Unix-like setup (theoretically an Apple machine
should work) that has the following software installed:

* `Python3`_ (with development libraries, pip and virtualenv)
* `GNU Privacy Guard`_
* `Tesseract`_, plus its language files matching your document base.
* `Imagemagick`_ version 6.7.5 or higher
* `unpaper`_
* `libpoppler-cpp-dev`_ PDF rendering library
* `optipng`_

.. _Python3: https://python.org/
.. _GNU Privacy Guard: https://gnupg.org
.. _Tesseract: https://github.com/tesseract-ocr
.. _Imagemagick: http://imagemagick.org/
.. _unpaper: https://github.com/unpaper/unpaper
.. _libpoppler-cpp-dev: https://poppler.freedesktop.org/
.. _optipng: http://optipng.sourceforge.net/

Notably, you should confirm how you access your Python3 installation.  Many
Linux distributions will install Python3 in parallel to Python2, using the
names ``python3`` and ``python`` respectively.  The same goes for ``pip3`` and
``pip``.  Running Paperless with Python2 will likely break things, so make sure
that you're using the right version.

For the purposes of simplicity, ``python`` and ``pip`` is used everywhere to
refer to their Python3 versions.

In addition to the above, there are a number of Python requirements, all of
which are listed in a file called ``Pipfile`` in the project root directory.

If you're not working on a virtual environment (like Docker), you
should probably be using a virtualenv, but that's your call.  The reasons why
you might choose a virtualenv or not aren't really within the scope of this
document.  Needless to say if you don't know what a virtualenv is, you should
probably figure that out before continuing.


.. _requirements-apple:

Problems with Imagemagick & PDFs
--------------------------------

Some users have `run into problems`_ with getting ImageMagick to do its thing
with PDFs.  Often this is the case with Apple systems using HomeBrew, but other
Linuxes have been a problem as well.  The solution appears to be to install
ghostscript as well as ImageMagick:

.. _run into problems: https://github.com/the-paperless-project/paperless/issues/25

.. code:: bash

    $ brew install ghostscript
    $ brew install imagemagick
    $ brew install libmagic


.. _requirements-baremetal:

Python-specific Requirements: No Virtualenv
-------------------------------------------

If you don't care to use a virtual env, then installation of the Python
dependencies is easy:

.. code:: bash

    $ cd /path/to/paperless
    $ pipenv lock -r > requirements.txt
    $ pip install --user --requirement requirements.txt

This will download and install all of the requirements into
``${HOME}/.local``.  Remember that your distribution may be using ``pip3`` as
mentioned above.

If you don't have Pipenv installed, then you can install it using ``pip``:

.. code:: Bash

    $ pip install --user pipenv


.. _requirements-virtualenv:

Python-specific Requirements: Virtualenv
----------------------------------------

Using a virtualenv for Paperless is very easy, thanks to Pipenv. If you don't
have Pipenv installed, then you can install it using ``pip``:

.. code:: Bash

    $ pip install --user pipenv

With Pipenv available, it is trivial to create the virtual environment and
install the requirements:

.. code:: bash

    $ cd /path/to/paperless
    $ pipenv --python 3
    $ pipenv install

Now you're ready to go. Just remember to enter the virtual environment
created by Pipenv using ``pipenv shell`` whenever you want to use Paperless.


.. _requirements-documentation:

Documentation
-------------

As generation of the documentation is not required for the use of Paperless,
dependencies for this process are not included in ``Pipfile``. If you'd like
to generate your own docs locally, you'll need to:

.. code:: bash

    $ pip install sphinx

and then cd into the ``docs`` directory and type ``make html``.

If you are using Docker, you can use the following commands to build the
documentation and run a webserver serving it on `port 8001`_:

.. code:: bash

    $ pwd
    /path/to/paperless

    $ docker build -t paperless:docs -f docs/Dockerfile .
    $ docker run --rm -it -p "8001:8000" paperless:docs

.. _port 8001: http://127.0.0.1:8001
