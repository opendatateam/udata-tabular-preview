from flask import Blueprint

from udata import assets
from udata.frontend import template_hook
from udata_front import theme

from udata_tabular_preview.explore import can_explore

from . import settings as DEFAULTS

blueprint = Blueprint('tabular', __name__, url_prefix='/tabular',
                      template_folder='templates',
                      static_folder='static')


def can_explore_dataset(ctx):
    dataset = ctx.get('dataset', None)
    return dataset and any(can_explore(resource) for resource in dataset.resources)


@template_hook('footer.snippets', when=can_explore_dataset)
def load_explore_script(ctx):
    return theme.render('script.html')


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
