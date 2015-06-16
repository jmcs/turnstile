Repository Configuration
========================

Overview
--------
Turnstile read the configuration from a ``.turnstile.yml`` file on the root of the repository.

Common Parameters
-----------------

+-----------+--------------------------------+
| parameter | Description                    |
+===========+================================+
| checks    | List of checks you want to run |
+-----------+--------------------------------+

Check Parameters
----------------
Some checks have check specific configuration that can be specified in a parameter with the check name.
Please look in the check documentation for more information.

List of checks
--------------
- :ref:`branch_pattern` - Check if branch name matches one of the allowed patterns
- :ref:`branch_release` - Check if release branches names contain a valid release name
- :ref:`branch_type` - Check if branch type is allowed
- :ref:`protect_master_check` - Prevents commits to master
- :ref:`specification_check` - Check if commit message contains a valid specification
