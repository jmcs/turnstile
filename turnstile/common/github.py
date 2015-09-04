"""
Common functions and regex expressions for github
"""

import re

GITHUB_REGEX = re.compile(
    r'^(https://github.com/|\w+@github\.com:)(?P<repository>[a-zA-Z0-9_\-]+/[a-zA-Z0-9_\-]+)\.git$')
GITHUB_ISSUE_REGEX = re.compile(r'^(([a-zA-Z0-9_\-]*|[a-zA-Z0-9_\-]+/[a-zA-Z0-9_\-]+)#|GH-)(?P<issue>\d+)$')


def extract_repository_from_url(git_url):
    """

    :param git_url:
    :return:
    :rtype: str | None


    >>> extract_repository_from_url('https://github.com/zalando/turnstile.git')
    'zalando/turnstile'
    >>> extract_repository_from_url('git@github.com:zalando-stups/senza.git')
    'zalando-stups/senza'
    >>> extract_repository_from_url('git@bitbucket.org:jmcs/somerepo.git') is None
    True
    """

    match = GITHUB_REGEX.match(git_url)
    if match:
        return match.group('repository')
    else:
        return None


def extract_issue_number(github_reference):
    """
    Extracts the issue number from the github reference

    :param github_reference:
    :type github_reference: str
    :return:
    :rtype: int | None

    >>> extract_issue_number('#42')
    42
    >>> extract_issue_number('GH-24')
    24
    >>> extract_issue_number('zalando#26')
    26
    >>> extract_issue_number('zalando/turnstile#36')
    36
    >>> extract_issue_number('JIRA-1000') is None
    True
    """

    match = GITHUB_ISSUE_REGEX.match(github_reference)
    if match:
        return int(match.group('issue'))
    else:
        return None
