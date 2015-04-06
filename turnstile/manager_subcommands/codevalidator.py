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
    codevalidator_rc = staging_area.working_dir / '.codevalidatorrc'
    with staging_area:
        output = codevalidator.codevalidator(staging_area.files, temporary_dir=staging_area.temporary_directory,
                                             custom_config=codevalidator_rc)
    print(output)
