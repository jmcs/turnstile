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
    Returns a check function
    :param hook_name: Which hook is fetching the check
    :param check_name: Name of check module
    :return: check function
    :rtype: function
    """

    # TODO return none on error
    logger = output.get_sub_logger(hook_name, 'load_check')
    checks_module = 'git_hooks.checks.' + hook_name.replace('-', '_')
    sub_module_name = '.' + check_name
    logger.debug('Loading %s from %s', sub_module_name, checks_module)
    sub_module = importlib.import_module(sub_module_name, checks_module)
    check_function = sub_module.check
    return check_function
