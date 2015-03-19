Branch Has Specification Check
------------------------------

Checks if the branch name includes the specification id. 

By default this check is ignored on master, but you can define more branches to be ignored using regex:

    branch-has-specification:
        exceptions:
            - "^release\/"