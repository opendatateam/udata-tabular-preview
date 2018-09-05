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
    @property
    def server_url(self):
        return current_app.config.get('TABULAR_CSVAPI_URL')

    def can_preview(self, resource):
        print('can preview', bool(self.server_url), resource.mime in SUPPORTED_MIME_TYPES, bool(self.server_url) and resource.mime in SUPPORTED_MIME_TYPES)
        return bool(self.server_url) and resource.mime in SUPPORTED_MIME_TYPES

    def preview_url(self, resource):
        print('preview_url', url_for('tabular.preview', url=resource.url))
        return url_for('tabular.preview', url=resource.url)
