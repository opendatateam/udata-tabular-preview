from flask import abort, current_app, render_template, Blueprint

from udata import assets

from . import settings as DEFAULTS

blueprint = Blueprint('tabular', __name__, url_prefix='/tabular',
                      template_folder='templates',
                      static_folder='static')


@blueprint.route('/preview/')
def preview():
    if current_app.config.get('PREVIEW_MODE') is None:
        abort(404)
    return render_template('tabular/preview.html')


@blueprint.record
def init_preview(state):
    for key, default in DEFAULTS.__dict__.items():
        state.app.config.setdefault(key, default)


@blueprint.add_app_template_global
def tabular_static(ui, filename):
    '''
    Get an UI asset path
    '''
    static_root = assets.cdn_for('tabular.static', filename=ui, _external=True)
    asset_type = filename.split('.')[1]
    return f"{static_root}/{asset_type}/{filename}"
