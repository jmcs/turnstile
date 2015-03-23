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
--------------q
* [Allowed Projects](checks/allowed-projects.md) - Check if commit is from an allowed JIRA project
* [Branch Has Specification](checks/branch-has-specification.md) - Check if branch name contains a reference to the 
  specification;
* [Branch Pattern](checks/branch-pattern.md) - Check if branch name matches one of the allowed patterns
* [Branch Release](checks/branch-release.md) - Check if release branches names contain a valid release name
* [Branch Type](checks/branch-type.md) - Check if branch type is allowed
* [Codevalidator](checks/codevalidator.md) - Check if committed files pass code validation
* [Specification](checks/specification.md) - Check if commit message contains a valid specification
