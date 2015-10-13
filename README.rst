============
calendar-cli
============

Fetch and notify daily summary for Google Calendar

.. image:: https://badge.fury.io/py/calendar-cli.svg
   :target: http://badge.fury.io/py/calendar-cli
   :alt: PyPI version

.. image:: https://travis-ci.org/mogproject/calendar-cli.svg?branch=master
   :target: https://travis-ci.org/mogproject/calendar-cli
   :alt: Build Status

.. image:: https://coveralls.io/repos/mogproject/calendar-cli/badge.svg?branch=master&service=github
   :target: https://coveralls.io/github/mogproject/calendar-cli?branch=master
   :alt: Coverage Status

.. image:: https://img.shields.io/badge/license-Apache%202.0-blue.svg
   :target: http://choosealicense.com/licenses/apache-2.0/
   :alt: License

.. image:: https://badge.waffle.io/mogproject/calendar-cli.svg?label=ready&title=Ready
   :target: https://waffle.io/mogproject/calendar-cli
   :alt: 'Stories in Ready'

------------
Dependencies
------------

* Python: 2.6 / 2.7 / 3.3 / 3.4
* pyyaml
* six
* python-dateutil
* pytz
* google-api-python-client

------------
Installation
------------

* ``pip`` command may need ``sudo``

+-------------------------+------------------------------------------+
| Operation               | Command                                  |
+=========================+==========================================+
| Install                 |``pip install calendar-cli``              |
+-------------------------+------------------------------------------+
| Upgrade                 |``pip install --upgrade calendar-cli``    |
+-------------------------+------------------------------------------+
| Uninstall               |``pip uninstall calendar-cli``            |
+-------------------------+------------------------------------------+
| Check installed version |``calendar-cli --version``                |
+-------------------------+------------------------------------------+
| Help                    |``calendar-cli -h``                       |
+-------------------------+------------------------------------------+

---------------
Getting Started
---------------

* Download ``client_secret.json`` from Google Developers Console

   * Open `Google Developers Console <https://console.developers.google.com/project>`_
   * Select or create a project
   * Open APIs & auth -> APIs -> Google Apps API -> Calendar API: Enable API
   * Open APIs & auth -> Credentials

      * OAuth consent screen: Set a product name and save
      * Credentials: Add credentials -> OAuth 2.0 client ID -> Other: Set a name and create
      * Download a credential file by clicking the ``Download JSON`` button, then rename it ``client_secret.json``

* Create a credentials file

::

    calendar-cli setup client_secret.json

The default path to the credentials file is ``~/.credential/calendar-cli.json``.

* Print the summary of today's events on the default calendar

::

    calendar-cli


* Launch with arguments

::

    calendar-cli --date 20151014
    calendar-cli --calendar xxxxxx@group.calendar.google.com

