# Garpix Comments

Комментирование любых моделей. Является частью GarpixCMS.

## Быстрый старт

Установка через pipenv:

```bash
pipenv install garpix_comments
```

Добавьте `garpix_comments` в `INSTALLED_APPS` и укажите адрес для миграций:

```python
# settings.py
from garpixcms.settings import *  # noqa

INSTALLED_APPS += [
    'garpix_comments',
]


MIGRATION_MODULES.update({
    'garpix_comments': 'app.migrations.garpix_comments'
})
```

Создайте директории и файлы:

```bash
backend/app/migrations/garpix_comments/
backend/app/migrations/garpix_comments/__init__.py
```

Сделайте миграции и мигрируйте:

```bash
python3 backend/manage.py makemigrations
python3 backend/manage.py migrate
```

Добавьте в `urls.py`:

```python

# ...
urlpatterns = [
    # ...
    # garpix_favourite
    path('', include(('garpix_comments.urls', 'comments'), namespace='garpix_comments')),

]
```


# Changelog

See [CHANGELOG.md](CHANGELOG.md).

# Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md).

# License

[MIT](LICENSE)

---

Developed by Garpix / [https://garpix.com](https://garpix.com)

