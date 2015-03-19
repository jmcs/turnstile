Allowed Project Check
---------------------

Checks if a specification project is allowed on repository. This currently only works if your specifications are Jira
tickets.

To allow, for example, to push PF-* and CD-* tickets to your project use:

    allowed-project:
        allowed:
            - PF
            - CD