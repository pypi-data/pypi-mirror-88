ecommerce plugin for `Grvlms <https://docs.grvlms.groove.education>`__
===================================================================================

Installation
------------

::

    pip install git+https://github.com/groovetch/grvlms-ecommerce

Usage
-----

::

    grvlms plugins enable ecommerce
    grvlms ecommerce config -i (variable configuration option)
    grvlms local start
    grvlms local init
    
Configuration
-------------

- ``ECOMMERCE_MYSQL_DATABASE`` (default: ``"ecommerce"``)
- ``ECOMMERCE_MYSQL_USERNAME`` (default: ``"ecommerce"``)
- ``ECOMMERCE_MYSQL_PASSWORD`` (default: ``"{{ 8|random_string }}"``)
- ``ECOMMERCE_SECRET_KEY`` (default: ``"{{ 20|random_string }}"``)
- ``ECOMMERCE_OAUTH2_KEY`` (default: ``"ecommerce"``)
- ``ECOMMERCE_OAUTH2_SECRET`` (default: ``"{{ 8|random_string }}"``)
- ``ECOMMERCE_API_KEY`` (default: ``"{{ 20|random_string }}"``)


License
-------

This software is licensed under the terms of the AGPLv3.

Release Note
------------

- Merged edt-45/adding-ecommerce-configuration
