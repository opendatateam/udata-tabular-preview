from flask import current_app

from udata_tabular_preview.preview import can_preview


def can_explore(resource):
    return can_preview(resource)
