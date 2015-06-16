Commit Specification Scheme
===========================

Overview
--------
Git commits provided for SCMs such as github.com, github enterprise or stash has to follow a certain template in order
to monitor commits in an automated way.

This document defines such a template.

A commit as defined in this document contains of a specification part and an actual message part.

The specification part is a uniform resource identifier (URI) inspired by `RFC 3686`_. The specification must be the
first “word” of the commit.

.. _`RFC 3686`: http://tools.ietf.org/html/rfc3986