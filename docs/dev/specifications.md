Commit Specification
====================
Overview
--------
Commit specifications are urlencoded uniform resource identifiers (URI). The specification must be the first “word” of
the commit and can optionally start with a ‘#’ character that is ignored. For readability purposes the scheme of the
specification URI can be omitted if the same as the default for the repository.


Schemes
-------
### Generic
Generic specification without a special meaning. Generic specifications are always valid.
This format is used by default if scheme is missing from the URI and there is no default scheme for the repository.

### Jira
Jira specification URIs take the form of “jira:PROJECT-TICKET_NUMBER” for example “jira:CD-123”