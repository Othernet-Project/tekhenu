=======
Tekhenu
=======

Content suggestion and broadcast management.

Tekhenu consists of user-facing content suggestion portal, and admin-facing
broadcast management facilities. The initial goal is to provide a complete
implementation of the former, and a basic implementation of the latter.

Future versions will include integration with the carousel encoder(s), and a
REST API for 3rd party integration wtih content suggestions.

Tekhenu is written in Python using `Bottle framework`_.

Requirements
============

Uses Python 2.7 on Google AppEngine (tested with SDK 1.9.x). Python
dependencies are listed in ``conf/requirements.txt``.

Dependencies
============

Install dependencies in ``vendor`` direcory using ``conf/requirements.txt``::

    pip install -r conf/requirements.txt -t vendor

.. note:

    When doing this, you must always remove the contents of ``vendor`` 
    directory.


.. _Bottle framework: http://bottlepy.org/
