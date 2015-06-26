# -*- coding: utf-8 -*-

from turnstile.models.specifications import get_specification


def test_get_specification():
    spec = get_specification('something')
    assert not spec.valid

    spec = get_specification('http://spec.url')
    assert spec.scheme == u'http'

    spec = get_specification('https://spec.url')
    assert spec.scheme == u'https'
