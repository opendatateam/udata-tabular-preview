from flask import current_app, render_template, Blueprint

from udata import assets
from udata.frontend import template_hook

from udata_tabular_preview.explore import can_explore

from . import settings as DEFAULTS
from urllib.parse import urlsplit


blueprint = Blueprint('tabular', __name__, url_prefix='/tabular',
                      template_folder='templates',
                      static_folder='static')


def can_explore_dataset(ctx):
    dataset = ctx.get('dataset', None)
    return dataset and any(can_explore(resource) for resource in dataset.resources)


@template_hook('header.snippets', when=can_explore_dataset)
def load_explore_metadata(ctx):
    dataset = ctx.get('dataset', None)
    resources = []
    for resource in dataset.resources:
        if can_explore(resource):
            resources.append(resource.id)
    return render_template('metadata.html', resources=resources)


@template_hook('footer.snippets', when=can_explore_dataset)
def load_explore_script(ctx):
    return render_template('script.html')


@template_hook('dataset.display.explore-button', when=can_explore_dataset)
def load_explore_button(ctx):
    dataset = ctx.get('dataset', None)
    explore_url = current_app.config.get('TABULAR_EXPLORE_URL')
    netloc = urlsplit(explore_url).netloc
    url = next(res.preview_url for res in dataset.resources if can_explore(res))
    return render_template('explore-button.html', netloc=netloc, url=url)


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
    return f"{static_root}/{filename}"
