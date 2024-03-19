import pytest

from udata.core.dataset.factories import ResourceFactory

from udata_tabular_preview.explore import can_explore

DUMMY_EXTRAS_GOOD = [{ 'analysis:parsing:finished_at': '1987-12-23T10:55:00.000000+00:00' }, { 'analysis:parsing:finished_at': 'toto' }]
DUMMY_EXTRAS_BAD = [{}, { 'dummy': 'extras' }]
MAX_SIZE = 50000

pytestmark = [
    pytest.mark.usefixtures('clean_db'),
    pytest.mark.options(PLUGINS=['tabular']),
    pytest.mark.frontend,
]

@pytest.mark.parametrize('extras', DUMMY_EXTRAS_GOOD)
@pytest.mark.options(TABULAR_EXPLORE_URL='http://preview.me')
@pytest.mark.options(TABULAR_API_URL='http://tabular-api.me/')
def test_can_explore(extras):
    resource = ResourceFactory(extras=extras)
    assert can_explore(resource)

@pytest.mark.parametrize('extras', DUMMY_EXTRAS_BAD)
@pytest.mark.options(TABULAR_EXPLORE_URL='http://preview.me')
@pytest.mark.options(TABULAR_API_URL='http://tabular-api.me/')
@pytest.mark.options(TABULAR_SUPPORTED_MIME_TYPES=[])
def test_cant_explore(extras):
    resource = ResourceFactory(extras=extras)
    assert not can_explore(resource)
