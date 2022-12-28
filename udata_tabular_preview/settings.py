'''
Default settings for udata-tabular-preview
'''
# csvapi instance URL
TABULAR_CSVAPI_URL = None

# explore instance URL
TABULAR_EXPLORE_URL = None

# Whether or not to allow remote resources
TABULAR_ALLOW_REMOTE = True

# Max (included) allowed file size in bytes
TABULAR_MAX_SIZE = None

# Default page size
TABULAR_PAGE_SIZE = 5

# Supported mimes
TABULAR_SUPPORTED_MIME_TYPES = (
    'text/csv',
    'application/vnd.ms-excel',
    'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
)
