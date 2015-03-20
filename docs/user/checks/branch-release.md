Branch Release Check
--------------------


Check if the release of a release branch (release/*) matches a pattern. By default this pattern is ``^R(?:\d|\_|\.)+$`` 
but it's configurable:

    branch-release:
        pattern: '*.'