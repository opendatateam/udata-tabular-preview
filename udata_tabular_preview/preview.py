from flask import current_app
from udata.core.dataset.preview import PreviewPlugin


class TabularPreview(PreviewPlugin):
    fallback = True

    @property
    def preview_base_url(self):
        return current_app.config.get('TABULAR_EXPLORE_URL')

    def can_preview(self, resource):
        has_config = (
            bool(current_app.config.get('TABULAR_API_URL'))
            and bool(self.preview_base_url)
        )

        is_hydra_table = (
            resource.extras.get('analysis:parsing:finished_at') is not None
            and resource.extras.get('analysis:parsing:error') is None
        )
        is_remote = resource.filetype == 'remote'
        allow_remote = current_app.config.get('TABULAR_ALLOW_REMOTE')
        is_allowed = allow_remote or not is_remote

        return all((has_config, is_hydra_table, is_allowed))

    def preview_url(self, resource):
        return f'{self.preview_base_url}/resources/{resource.id}'
