from flask import current_app
from udata.core.dataset.preview import PreviewPlugin
from urllib.parse import quote_plus


class TabularPreview(PreviewPlugin):
    fallback = True

    @property
    def preview_base_url(self):
        return current_app.config.get('TABULAR_EXPLORE_URL')

    def can_preview(self, resource):
        has_config = (
                        bool(current_app.config.get('TABULAR_CSVAPI_URL'))
                        and bool(self.preview_base_url)
        )

        supported_mimes = current_app.config.get('TABULAR_SUPPORTED_MIME_TYPES')
        extras_mime = resource.extras.get('check:headers:content-type')
        is_supported = (
            extras_mime in supported_mimes
            or resource.mime in supported_mimes
        )

        is_remote = resource.filetype == 'remote'
        allow_remote = current_app.config.get('TABULAR_ALLOW_REMOTE')
        is_allowed = allow_remote or not is_remote

        max_size = current_app.config.get('TABULAR_MAX_SIZE')
        extras_size = resource.extras.get('check:headers:content-length')
        size_ok = (
            not max_size
            or (extras_size or resource.filesize or float("inf")) <= max_size
        )

        return all((has_config, is_supported, is_allowed, size_ok))

    def preview_url(self, resource):
        return f'{self.preview_base_url}/?url={quote_plus(resource.latest)}'
