.. _specification_check:

Specification Check
-------------------

This check verifies if the commit message starts with a valid reference to a specification.
Turnstile supports several formats to link to the specification. By default it allows only URI_ specification but you
can change the allowed formats:

.. code-block:: yaml

    specification:
        allowed_format: ['uri', 'github', 'jira']

Github
~~~~~~
Checks if the specification is a `valid github reference <gh_reference_>`_.

Jira
~~~~
Checks if the specification is a valid Jira ticket key.

URI
~~~
Checks if a specification URI is a valid and absolute. This check is ignored for merge commits.

By default only HTTPS and offline URIs are accepted but you can change the allowed schemes:

.. code-block:: yaml

    specification:
        allowed_format: ['uri']
        allowed_schemes: ['https', 'ftp']

.. _gh_reference: https://help.github.com/articles/writing-on-github/#references