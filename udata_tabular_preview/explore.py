from udata_tabular_preview.preview import TabularPreview

tabular_preview = TabularPreview()


def can_explore(resource):
    return tabular_preview.can_preview(resource)
