import pytest

import turnstile.models.message as message
from turnstile.checks import CheckIgnore
from turnstile.checks.commit_msg.branch_release import check


def test_check():
    commit1 = message.CommitMessage('release/R10_00', 'https://github.com/zalando-bus/turnstile/issues/42 message')
    result1 = check(None, {}, commit1)
    assert result1.successful
    assert result1.details == []

    with pytest.raises(CheckIgnore):
        commit2 = message.CommitMessage('master', 'https://github.com/zalando-bus/turnstile/issues/42 message')
        check(None, {}, commit2)

    with pytest.raises(CheckIgnore):
        commit3 = message.CommitMessage('feature/whatever',
                                        'https://github.com/zalando-bus/turnstile/issues/42 message')
        check(None, {}, commit3)

    commit4 = message.CommitMessage('release/10_00', 'https://github.com/zalando-bus/turnstile/issues/42 message')
    result4 = check(None, {}, commit4)
    assert not result4.successful
    assert result4.details == ["'10_00' doesn't match '^R(?:\\d|\\_|\\.)+$'."]

    commit5 = message.CommitMessage('release/10_00', 'https://github.com/zalando-bus/turnstile/issues/42 message')
    result5 = check(None, {'branch-release': {'pattern': '.*'}}, commit5)
    assert result5.successful
    assert result5.details == []
