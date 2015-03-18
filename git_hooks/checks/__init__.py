import collections
import importlib

import git_hooks.common.output as output

CheckResult = collections.namedtuple('CheckResult', ['successful', 'details'])


class CheckResult(object):
    def __init__(self, successful=True, details=None):
        """
        :type successful: bool
        :type details: list
        """
        self.successful = successful
        self.details = details or list()

    def add_detail(self, detail):
        """
        Adds detail to a check
        :type detail: str
        """
        self.details.append(detail)


class Check(object):

    """
    Decorator that wraps a check
    """

    def __init__(self, description):
        """
        :param description: Check description
        :type description: str
        """
        self.description = description

    def __call__(self, function):
        function.description = self.description
        return function


def load_check(hook_name, check_name):
    """
    Returns a check function.
    Checks for hook_name are stored git_hooks.checks.[hook_name].[check_name] and should be a function name check

    :param hook_name: Which hook is fetching the check
    :param check_name: Name of check module
    :return: check function
    :rtype: function
    """

    # TODO document where checks are stored and how in dev guide
    # TODO return none on error
    logger = output.get_sub_logger(hook_name, 'load_check')
    checks_module = 'git_hooks.checks.' + hook_name.replace('-', '_')
    sub_module_name = '.' + check_name.replace('-', '_')  # TODO document this change in dev guide
    logger.debug('Loading %s from %s', check_name, checks_module)
    try:
        sub_module = importlib.import_module(sub_module_name, checks_module)
    except ImportError:
        logger.debug("Check %s not found. Maybe it belongs to the other hook", check_name)
        return None
    check_function = sub_module.check
    return check_function


def get_checks(hook_name, checklist):
    """
    Load all the checks for a repository ignoring unknown checks

    :param hook_name: Which hook is fetching the checks
    :type hook_name: str
    :param checklist: List of check names
    :type checklist: [str]
    :return: [function]
    """
    checks_for_hook = list()
    for check_name in checklist:
        check = load_check(hook_name, check_name)
        if check:
            checks_for_hook.append(check)
    return checks_for_hook
