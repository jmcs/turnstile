Repository Configuration
========================

Common Parameters
-----------------

| parameter |                                |
|-----------|--------------------------------|
| checks    | List of checks you want to run |

Check Parameters
----------------
Some checks have check specific configuration that can be specified in a parameter with the check name.
Please look in the check documentation for more information.

List of checks
--------------
- [Branch Pattern](checks/branch-pattern.md) - Check if branch name matches one of the allowed patterns
- [Branch Release](checks/branch-release.md) - Check if release branches names contain a valid release name
- [Branch Type](checks/branch-type.md) - Check if branch type is allowed
- [Protect Master](checks/protect-master.md) - Prevents commits to master
- [Specification](checks/specification.md) - Check if commit message contains a valid specification
