import pytest

import turnstile.models.message as message
from turnstile.checks import CheckIgnore
from turnstile.checks.commit_msg.specification import check


def test_check():
    commit_1 = message.CommitMessage('something', 'https://github.com/zalando-bus/turnstile/issues/42 m€sságe')
    result_1 = check(None, {}, commit_1)
    assert result_1.successful
    assert result_1.details == []

    commit_2 = message.CommitMessage('something', 'invalid-1')
    result_2 = check(None, {}, commit_2)
    assert not result_2.successful
    assert result_2.details == ['invalid-1 is not a valid specification URI.']

    # Merge messages are ignored
    with pytest.raises(CheckIgnore):
        commit_3 = message.CommitMessage('something', 'Merge stuff')
        check(None, {}, commit_3)

    commit_4 = message.CommitMessage('something', 'ftp://example.com/spec')
    result_4 = check(None, {'specification': {'allowed_schemes': ['https']}}, commit_4)
    assert not result_4.successful
    assert result_4.details == ['ftp is not allowed. Allowed schemes are: https']

    commit_5 = message.CommitMessage('something', 'ftp://example.com/spec')
    result_5 = check(None, {'specification': {'allowed_schemes': ['https', 'ftp']}}, commit_5)
    assert result_5.successful
    assert result_5.details == []
