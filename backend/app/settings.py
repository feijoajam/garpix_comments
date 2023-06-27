from garpixcms.settings import *  # noqa

MIGRATION_MODULES.update({  # noqa:F405
    'fcm_django': 'app.migrations.fcm_django'
})

INSTALLED_APPS += [
    'garpix_comments',
    'testapp'
]
