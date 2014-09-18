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

About the Brandon font
======================

Outernet uses a font called `Brandon Grotesque`_. Since this font cannot be
legally shipped along with the rest of the source code, the CSS for the project
will not compile correctly. You should either omit all references to the font
by modifying the source, or obtain the font and add the necessary code for it.


.. _Bottle framework: http://bottlepy.org/
.. _Brandon Grotesque: http://www.myfonts.com/fonts/hvdfonts/brandon-grotesque/
