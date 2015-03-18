import git_hooks.checks as checks
import git_hooks.common.output as output


@checks.Check('Dummy Message Check')
def check(commit_message):
    """

    :param commit_message:
    :type commit_message: git_hooks.models.message.CommitMessage
    :return: If check passed or not
    :rtype: bool
    """

    result = checks.CheckResult()

    logger = output.get_sub_logger('commit-msg', 'message-dummy')
    logger.debug("Commit message is '%s' and I think it's ok", commit_message.message)
    result.add_detail('Commit Message is: {}'.format(commit_message.message))
    return result
