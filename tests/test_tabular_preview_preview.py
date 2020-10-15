import pytest

from urllib.parse import quote_plus

from udata.core.dataset.factories import ResourceFactory


MIME_TYPE = 'text/csv'
DUMMY_MIMES = ['text/csv', 'text/toto']
MAX_SIZE = 50000

pytestmark = [
    pytest.mark.usefixtures('clean_db'),
    pytest.mark.options(PLUGINS=['tabular']),
    pytest.mark.frontend,
]


def expected_url(url):
    encoded_url = quote_plus(url)
    return '/tabular/preview/?url={0}'.format(encoded_url)


@pytest.mark.parametrize('mime', DUMMY_MIMES)
@pytest.mark.options(TABULAR_CSVAPI_URL='http://preview.me/')
@pytest.mark.options(TABULAR_SUPPORTED_MIME_TYPES=DUMMY_MIMES)
def test_display_preview_for_tabular_resources(mime):
    resource = ResourceFactory(mime=mime)
    assert resource.preview_url == expected_url(resource.url)


@pytest.mark.options(TABULAR_CSVAPI_URL=None)
def test_no_preview_if_no_conf():
    assert ResourceFactory(mime=MIME_TYPE).preview_url is None


@pytest.mark.options(TABULAR_CSVAPI_URL='http://preview.me/')
def test_no_preview_if_for_unknown_types():
    assert ResourceFactory(mime='not/known').preview_url is None


@pytest.mark.options(TABULAR_CSVAPI_URL='http://preview.me/')
def test_default_allow_remote_preview():
    resources = [
        ResourceFactory(mime=MIME_TYPE),
        ResourceFactory(filetype='remote', mime=MIME_TYPE),
    ]

    for resource in resources:
        assert resource.preview_url == expected_url(resource.url)


@pytest.mark.options(TABULAR_CSVAPI_URL='http://preview.me/',
                     TABULAR_ALLOW_REMOTE=False)
def test_allow_remote_preview_false():
    local = ResourceFactory(mime=MIME_TYPE)
    remote = ResourceFactory(filetype='remote', mime=MIME_TYPE)

    assert local.preview_url == expected_url(local.url)
    assert remote.preview_url is None


@pytest.mark.options(TABULAR_CSVAPI_URL='http://preview.me/')
def test_display_preview_without_max_size():
    resource = ResourceFactory(mime=MIME_TYPE, filesize=2 * MAX_SIZE)

    assert resource.preview_url == expected_url(resource.url)


@pytest.mark.options(TABULAR_CSVAPI_URL='http://preview.me/',
                     TABULAR_MAX_SIZE=MAX_SIZE)
def test_display_preview_without_resource_size():
    resource = ResourceFactory(mime=MIME_TYPE, filesize=None)

    assert resource.preview_url is None


@pytest.mark.parametrize('size', [MAX_SIZE - 1, MAX_SIZE])
@pytest.mark.options(TABULAR_CSVAPI_URL='http://preview.me/',
                     TABULAR_MAX_SIZE=MAX_SIZE)
def test_display_preview_with_max_size(size):
    resource = ResourceFactory(mime=MIME_TYPE, filesize=size)

    assert resource.preview_url == expected_url(resource.url)


@pytest.mark.options(TABULAR_CSVAPI_URL='http://preview.me/',
                     TABULAR_MAX_SIZE=MAX_SIZE)
def test_display_preview_using_extras():
    extras = {
        'check:headers:content-type': MIME_TYPE,
        'check:headers:content-length': MAX_SIZE - 1,
    }
    resource = ResourceFactory(
        mime=None,
        filesize=None,
        extras=extras
    )

    assert resource.preview_url == expected_url(resource.url)


@pytest.mark.options(TABULAR_CSVAPI_URL='http://preview.me/',
                     TABULAR_MAX_SIZE=MAX_SIZE)
def test_no_preview_for_resource_over_max_size():
    resource = ResourceFactory(mime=MIME_TYPE, filesize=MAX_SIZE + 1)

    assert resource.preview_url is None
