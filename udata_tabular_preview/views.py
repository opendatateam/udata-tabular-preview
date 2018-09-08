# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os

from flask import abort, current_app, render_template, Blueprint

from udata import assets

from . import settings as DEFAULTS

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
    for key, default in DEFAULTS.__dict__.items():
        state.app.config.setdefault(key, default)
    with state.app.app_context():
        for key, manifest in MANIFESTS.items():
            assets.register_manifest(key, filename=manifest)


@blueprint.add_app_template_global
def tabular_manifest(ui, filename):
    '''
    Get an UI asset path from its manifest
    '''
    static_root = assets.cdn_for('tabular.static', filename=ui, _external=True)
    asset = assets.from_manifest(ui, filename, raw=True)
    return '/'.join((static_root, asset))
