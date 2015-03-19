Branch Type Check
-----------------

Checks if the branch type is the allowed types list in the repository options. The branch type is the prefix of the 
branch name, for example feature/CD-100 is a feature branch.

Master branch is always allowed.

    branch-type:
        allowed:
            - release
            - feature