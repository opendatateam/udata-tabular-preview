# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import pytest

from urllib import quote_plus

from udata.core.dataset.factories import DatasetFactory, ResourceFactory

pytestmark = [
    pytest.mark.usefixtures('clean_db'),
    pytest.mark.options(PLUGINS=['tabular-preview']),
]


@pytest.mark.parametrize('mime', [
    'text/csv',
    'application/vnd.ms-excel',
    'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
])
@pytest.mark.options(TABULAR_PREVIEW_SERVER_URL='http://preview.me/')
def test_display_preview_for_tabular_resources(mime):
    resource = ResourceFactory(mime=mime)
    DatasetFactory(resources=[resource])

    encoded_url = quote_plus(resource.url)
    expected = 'http://preview.me/?csv={0}'.format(encoded_url)
    assert resource.preview_url == expected


@pytest.mark.options(TABULAR_PREVIEW_SERVER_URL=None)
def test_no_preview_if_no_conf():
    resource = ResourceFactory(mime='text/csv')
    DatasetFactory(resources=[resource])

    assert resource.preview_url is None


@pytest.mark.options(TABULAR_PREVIEW_SERVER_URL='http://preview.me/')
def test_no_preview_if_for_unknown_types():
    resource = ResourceFactory(mime='not/known')
    DatasetFactory(resources=[resource])

    assert resource.preview_url is None
