import pytest

from udata.core.dataset.factories import ResourceFactory

from udata_tabular_preview.explore import can_explore

DUMMY_MIMES = ['text/csv', 'text/toto']
DUMMY_EXTRAS = [{ 'analysis:mime-type': 'text/csv' }, { 'check:headers:content-type': 'text/toto' }]
MAX_SIZE = 50000

pytestmark = [
    pytest.mark.usefixtures('clean_db'),
    pytest.mark.options(PLUGINS=['tabular']),
    pytest.mark.frontend,
]

@pytest.mark.parametrize('extras', DUMMY_EXTRAS)
@pytest.mark.options(TABULAR_EXPLORE_URL='http://preview.me')
@pytest.mark.options(TABULAR_API_URL='http://tabular-api.me/')
@pytest.mark.options(TABULAR_SUPPORTED_MIME_TYPES=DUMMY_MIMES)
def test_can_explore(extras):
    resource = ResourceFactory(extras=extras)
    assert can_explore(resource)

@pytest.mark.parametrize('extras', DUMMY_EXTRAS)
@pytest.mark.options(TABULAR_EXPLORE_URL='http://preview.me')
@pytest.mark.options(TABULAR_API_URL='http://tabular-api.me/')
@pytest.mark.options(TABULAR_SUPPORTED_MIME_TYPES=[])
def test_cant_explore(extras):
    resource = ResourceFactory(extras=extras)
    assert not can_explore(resource)
