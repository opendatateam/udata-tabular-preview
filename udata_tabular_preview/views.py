from flask import current_app, render_template, Blueprint

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


@template_hook('header.snippets')
def load_explore_metadata(ctx):
    return render_template('metadata.html')


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
