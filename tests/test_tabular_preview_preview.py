# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import pytest

from udata.core.dataset.factories import DatasetFactory, ResourceFactory

pytestmark = [
    pytest.mark.usefixtures('clean_db'),
    pytest.mark.options(PLUGINS=['tabular-preview']),
]


def test_display_preview_for_api_resources():
    # TODO: Build a dataset and a resource matching required crierions for preview
    resource = ResourceFactory()
    DatasetFactory(resources=[resource], extras={})

    assert resource.preview_url == 'http://the.expected/preview/url'


# TODO: test other cases, matching or not
