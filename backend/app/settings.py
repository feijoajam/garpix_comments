from garpixcms.settings import *  # noqa

MIGRATION_MODULES.update({  # noqa:F405
    'fcm_django': 'app.migrations.fcm_django',
    'garpix_comments': 'app.migrations.garpix_comments'
})

ACCEPTED_COMMENT_MODELS = ['mypost']
COMMENT_DEPTH_LEVEL = 3

INSTALLED_APPS += [
    'garpix_comments',
    'testapp',
]
