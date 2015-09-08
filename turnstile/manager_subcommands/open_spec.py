#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Copyright 2015 Zalando SE

Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the
License. You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an
"AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific
language governing permissions and limitations under the License.
"""

from __future__ import print_function

import click
import webbrowser

import turnstile.common.config as config
import turnstile.common.git as git
import turnstile.common.github as github
import turnstile.models.specifications as specifications


@click.command('view')
@click.argument('reference', required=False)
def cmd(reference='HEAD'):
    """
    Opens the specification for commit
    """

    repository = git.get_repository()
    if not repository:
        click.secho('This command must be executed inside a repository.', fg='red', bold=True)
        raise click.Abort

    options = config.load_repository_configuration(repository.working_dir).get('specification', {})
    allowed_schemes = options.get('allowed_schemes', ['https', 'offline'])
    allowed_formats = options.get('allowed_formats', {'uri'})

    try:
        commit = repository.commit(reference)
    except git.BadName:
        click.secho("'{reference}' is not a valid commit reference.".format(reference=reference), fg='red', bold=True)
        raise click.Abort

    specification = specifications.get_specification(commit.message, allowed_formats, allowed_schemes)
    specification_format = specification.format

    if not specification_format:
        click.secho("That commit doesn't have a valid specification.", fg='red', bold=True)
        raise click.Abort

    if specification_format == 'uri':
        url = specification.identifier
    elif specification_format == 'github':
        origin = repository.remote('origin')  # type: git.remote.Remote
        git_url = origin.config_reader.get('url')
        repository = github.extract_repository_from_url(git_url)
        if repository:
            issue = github.extract_issue_number(specification.identifier)
            url = 'https://github.com/{repository}/issues/{issue}'.format(**locals())
        else:
            click.secho("{} is not a github repository.".format(git_url), fg='red', bold=True)
            raise click.Abort
    else:
        url = None

    if url:
        click.secho('Opening {}'.format(url))
        webbrowser.open(url)
    else:
        click.secho("{} specifications aren't supported yet.".format(specification_format), fg='red', bold=True)
        raise click.Abort
