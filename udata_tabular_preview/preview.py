# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from urllib import quote_plus

from flask import current_app
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
        return '{server}?csv={url}'.format(
            server=self.server_url,
            url=quote_plus(resource.url)
        )
