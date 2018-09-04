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
        return current_app.config.get('TABULAR_PREVIEW_SERVER_URL')

    def can_preview(self, resource):
        return bool(self.server_url) and resource.mime in SUPPORTED_MIME_TYPES

    def preview_url(self, resource):
        return url_for('tabular.preview', url=resource.url)
