# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from flask import current_app, url_for
from udata.core.dataset.preview import PreviewPlugin


SUPPORTED_MIME_TYPES = (
    'text/csv',
    'application/vnd.ms-excel',
    'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
)


class TabularPreview(PreviewPlugin):
    fallback = True

    @property
    def server_url(self):
        return current_app.config.get('TABULAR_CSVAPI_URL')

    def can_preview(self, resource):
        has_config = bool(self.server_url)
        is_supported = resource.mime in SUPPORTED_MIME_TYPES
        is_remote = resource.filetype == 'remote'
        allow_remote = current_app.config.get('TABULAR_ALLOW_REMOTE')
        is_allowed = allow_remote or not is_remote
        max_size = current_app.config.get('TABULAR_MAX_SIZE')
        size_ok = not max_size or resource.filesize <= max_size

        return all((has_config, is_supported, is_allowed, size_ok))

    def preview_url(self, resource):
        return url_for('tabular.preview', url=resource.url)
