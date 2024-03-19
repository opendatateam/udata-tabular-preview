import pytest

from udata.core.dataset.factories import ResourceFactory


DUMMY_EXTRAS = { 'analysis:parsing:finished_at': '1987-12-23T10:55:00.000000+00:00' }
MAX_SIZE = 50000

pytestmark = [
    pytest.mark.usefixtures('clean_db'),
    pytest.mark.options(PLUGINS=['tabular']),
    pytest.mark.frontend,
]

def expected_url(rid):
    return 'http://preview.me/resources/{0}'.format(rid)


@pytest.mark.options(TABULAR_EXPLORE_URL='http://preview.me')
@pytest.mark.options(TABULAR_API_URL='http://tabular-api.me/')
def test_display_preview_for_tabular_resources():
    resource = ResourceFactory(extras=DUMMY_EXTRAS)
    assert resource.preview_url == expected_url(resource.id)


@pytest.mark.options(TABULAR_EXPLORE_URL=None, TABULAR_API_URL=None)
def test_no_preview_if_no_conf():
    assert ResourceFactory(extras=DUMMY_EXTRAS).preview_url is None


@pytest.mark.options(TABULAR_EXPLORE_URL='http://preview.me',
                     TABULAR_API_URL='http://tabular-api.me/')
def test_default_allow_remote_preview():
    resources = [
        ResourceFactory(extras=DUMMY_EXTRAS),
        ResourceFactory(filetype='remote', extras=DUMMY_EXTRAS),
    ]

    for resource in resources:
        assert resource.preview_url == expected_url(resource.id)


@pytest.mark.options(TABULAR_EXPLORE_URL='http://preview.me',
                     TABULAR_API_URL='http://tabular-api.me/',
                     TABULAR_ALLOW_REMOTE=False)
def test_allow_remote_preview_false():
    local = ResourceFactory(extras=DUMMY_EXTRAS)
    remote = ResourceFactory(filetype='remote', extras=DUMMY_EXTRAS)

    assert local.preview_url == expected_url(local.id)
    assert remote.preview_url is None


@pytest.mark.options(TABULAR_EXPLORE_URL='http://preview.me',
                     TABULAR_API_URL='http://tabular-api.me/')
def test_display_preview_without_max_size():
    resource = ResourceFactory(extras=DUMMY_EXTRAS, filesize=2 * MAX_SIZE)

    assert resource.preview_url == expected_url(resource.id)
