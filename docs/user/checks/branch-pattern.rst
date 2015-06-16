.. _branch_pattern:

Branch Pattern Check
--------------------

Checks if the branch names matches any regex pattern on list defined in the repository options.
Master branch is always allowed.

.. code-block:: yaml

    branch-pattern:
        allowed:
            - "^release/R"
            - "^feature/"