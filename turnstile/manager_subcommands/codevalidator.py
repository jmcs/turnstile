from __future__ import print_function

import click
import git

import turnstile.checks.pre_commit.codevalidator as codevalidator
import turnstile.models.staging as staging


@click.command('codevalidator')
def cmd():
    """
    Executes the codevalidator check and optionally tries to fix the files.
    """
    repository = git.Repo()
    staging_area = staging.StagingArea(repository)
    result = codevalidator.check(None, None, staging_area)
    for detail in result.details:
        print(detail)
