# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os

from flask import abort, current_app, render_template, Blueprint

from udata import assets

blueprint = Blueprint('tabular', __name__, url_prefix='/tabular',
                      template_folder='templates',
                      static_folder='static')


MANIFESTS = {
    'dataexplorer': os.path.join(blueprint.static_folder,
                                 'dataexplorer/asset-manifest.json'),
    'csvapi-front': os.path.join(blueprint.static_folder,
                                 'csvapi-front/manifest.json'),
}


@blueprint.route('/preview/')
def preview():
    if current_app.config.get('PREVIEW_MODE') is None:
        abort(404)
    return render_template('tabular/preview.html')


@blueprint.record
def init_preview(state):
    state.app.config.setdefault('TABULAR_UI', 'csvapi-front')
    with state.app.app_context():
        for key, manifest in MANIFESTS.items():
            assets.register_manifest(key, filename=manifest)
