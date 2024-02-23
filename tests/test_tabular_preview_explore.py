import pytest

from udata.core.dataset.factories import ResourceFactory

from udata_tabular_preview.explore import can_explore

MIME_TYPE = 'text/csv'
DUMMY_MIMES = ['text/csv', 'text/toto']
MAX_SIZE = 50000

pytestmark = [
    pytest.mark.usefixtures('clean_db'),
    pytest.mark.options(PLUGINS=['tabular']),
    pytest.mark.frontend,
]

@pytest.mark.parametrize('mime', DUMMY_MIMES)
@pytest.mark.options(TABULAR_EXPLORE_URL='http://preview.me')
@pytest.mark.options(TABULAR_API_URL='http://tabular-api.me/')
@pytest.mark.options(TABULAR_SUPPORTED_MIME_TYPES=DUMMY_MIMES)
def test_can_explore(mime):
    resource = ResourceFactory(mime=mime)
    assert can_explore(resource)

@pytest.mark.parametrize('mime', DUMMY_MIMES)
@pytest.mark.options(TABULAR_EXPLORE_URL='http://preview.me')
@pytest.mark.options(TABULAR_API_URL='http://tabular-api.me/')
@pytest.mark.options(TABULAR_SUPPORTED_MIME_TYPES=[])
def test_cant_explore(mime):
    resource = ResourceFactory(mime=mime)
    assert not can_explore(resource)
