Commit Specification Scheme
===========================

Overview
--------
Git commits provided for SCMs such as github.com, github enterprise or stash has to follow a certain template in order
to monitor commits in an automated way.

This document defines such a template.

A commit as defined in this document contains of a specification part and an actual message part.

The specification part can be a uniform resource identifier (URI) according to `RFC 3686`_,
a `github reference <gh_reference_>`_ or a JIRA ticket key.

The specification must be the first “word” of the commit.

.. _gh_reference: https://help.github.com/articles/writing-on-github/#references
.. _`RFC 3686`: http://tools.ietf.org/html/rfc3986