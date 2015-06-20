.. _specification_check:

Specification Check
-------------------

Checks if a specification URI is a valid and absolute. This check is ignored for merge commits.

By default only HTTPS and offline URIs are accepted but you can change the allowed schemes:

.. code-block:: yaml

    specification:
        allowed_schemes: ['https', 'ftp']