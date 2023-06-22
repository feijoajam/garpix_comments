# Generated by Django 3.2.19 on 2023-06-22 08:51

from django.db import migrations, models
import django.db.models.deletion
import garpix_admin_lock.mixins.view_mixin
import garpix_page.fields.grapes_js_html
import garpix_page.mixins.models.clone_mixin
import garpix_page.utils.all_sites
import garpix_page.utils.get_file_path
import garpix_utils.file.file_field
import polymorphic_tree.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('sites', '0002_alter_domain_unique'),
    ]

    operations = [
        migrations.CreateModel(
            name='BaseComponent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='Название')),
                ('title_ru', models.CharField(max_length=255, null=True, verbose_name='Название')),
                ('is_deleted', models.BooleanField(default=False, verbose_name='Запись удалена')),
                ('is_active', models.BooleanField(default=True, verbose_name='Включено')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Дата изменения')),
                ('text_title', models.CharField(blank=True, default='', max_length=128, verbose_name='Заголовок')),
                ('text_title_ru', models.CharField(blank=True, default='', max_length=128, null=True, verbose_name='Заголовок')),
            ],
            options={
                'verbose_name': 'Компонент',
                'verbose_name_plural': 'Компоненты',
                'ordering': ('created_at', 'title'),
            },
            bases=(garpix_page.mixins.models.clone_mixin.CloneMixin, models.Model),
        ),
        migrations.CreateModel(
            name='BasePage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='Название')),
                ('title_ru', models.CharField(max_length=255, null=True, verbose_name='Название')),
                ('is_active', models.BooleanField(default=True, verbose_name='Включено')),
                ('display_on_sitemap', models.BooleanField(default=True, verbose_name='Отображать в карте сайта')),
                ('slug', models.SlugField(blank=True, default='', max_length=150, verbose_name='ЧПУ')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Дата изменения')),
                ('seo_title', models.CharField(blank=True, default='', max_length=250, verbose_name='SEO заголовок страницы (title)')),
                ('seo_title_ru', models.CharField(blank=True, default='', max_length=250, null=True, verbose_name='SEO заголовок страницы (title)')),
                ('seo_keywords', models.CharField(blank=True, default='', max_length=250, verbose_name='SEO ключевые слова (keywords)')),
                ('seo_keywords_ru', models.CharField(blank=True, default='', max_length=250, null=True, verbose_name='SEO ключевые слова (keywords)')),
                ('seo_description', models.TextField(blank=True, default='', verbose_name='SEO описание (description)')),
                ('seo_description_ru', models.TextField(blank=True, default='', null=True, verbose_name='SEO описание (description)')),
                ('seo_author', models.CharField(blank=True, default='', max_length=250, verbose_name='SEO автор (author)')),
                ('seo_author_ru', models.CharField(blank=True, default='', max_length=250, null=True, verbose_name='SEO автор (author)')),
                ('seo_og_type', models.CharField(blank=True, default='website', max_length=250, verbose_name='SEO og:type')),
                ('seo_image', models.FileField(blank=True, null=True, upload_to=garpix_page.utils.get_file_path.get_file_path, verbose_name='SEO изображение')),
                ('url', models.CharField(blank=True, default='', max_length=255, verbose_name='Полный URL страницы')),
                ('lft', models.PositiveIntegerField(editable=False)),
                ('rght', models.PositiveIntegerField(editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('level', models.PositiveIntegerField(editable=False)),
                ('parent', polymorphic_tree.models.PolymorphicTreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='children', to='garpix_page.basepage', verbose_name='Родительская страница')),
                ('polymorphic_ctype', models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='polymorphic_garpix_page.basepage_set+', to='contenttypes.contenttype')),
                ('sites', models.ManyToManyField(default=garpix_page.utils.all_sites.get_all_sites, to='sites.Site', verbose_name='Сайты для отображения')),
            ],
            options={
                'verbose_name': 'Структура страниц',
                'verbose_name_plural': 'Структура страниц',
                'ordering': ('created_at', 'title'),
                'abstract': False,
                'base_manager_name': 'objects',
            },
            bases=(garpix_page.mixins.models.clone_mixin.CloneMixin, models.Model, garpix_admin_lock.mixins.view_mixin.PageLockViewMixin),
        ),
        migrations.CreateModel(
            name='GrapesJsHtmlComponent',
            fields=[
                ('basecomponent_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='garpix_page.basecomponent')),
                ('html', garpix_page.fields.grapes_js_html.GrapesJsHtmlField()),
            ],
            options={
                'verbose_name': 'GrapesJs компонент',
                'verbose_name_plural': 'GrapesJs компоненты',
            },
            bases=('garpix_page.basecomponent',),
        ),
        migrations.CreateModel(
            name='SeoTemplate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=True, verbose_name='Включено')),
                ('rule_field', models.CharField(max_length=255, verbose_name='Поле')),
                ('model_rule_value', models.CharField(blank=True, max_length=255, null=True, verbose_name='Название')),
                ('rule_value', models.CharField(blank=True, max_length=255, null=True, verbose_name='Значение')),
                ('seo_title', models.CharField(blank=True, default='', max_length=250, verbose_name='SEO заголовок страницы (title)')),
                ('seo_title_ru', models.CharField(blank=True, default='', max_length=250, null=True, verbose_name='SEO заголовок страницы (title)')),
                ('seo_keywords', models.CharField(blank=True, default='', max_length=250, verbose_name='SEO ключевые слова (keywords)')),
                ('seo_keywords_ru', models.CharField(blank=True, default='', max_length=250, null=True, verbose_name='SEO ключевые слова (keywords)')),
                ('seo_description', models.TextField(blank=True, default='', verbose_name='SEO описание (description)')),
                ('seo_description_ru', models.TextField(blank=True, default='', null=True, verbose_name='SEO описание (description)')),
                ('seo_author', models.CharField(blank=True, default='', max_length=250, verbose_name='SEO автор (author)')),
                ('seo_author_ru', models.CharField(blank=True, default='', max_length=250, null=True, verbose_name='SEO автор (author)')),
                ('seo_og_type', models.CharField(blank=True, default='website', max_length=250, verbose_name='SEO og:type')),
                ('seo_image', models.FileField(blank=True, null=True, upload_to=garpix_utils.file.file_field.get_file_path, verbose_name='SEO изображение')),
                ('priority_order', models.PositiveIntegerField(default=1, help_text='Чем меньше число, тем выше приоритет', verbose_name='Приоритетность применения')),
                ('sites', models.ManyToManyField(default=garpix_page.utils.all_sites.get_all_sites, to='sites.Site', verbose_name='Сайты для применения')),
            ],
            options={
                'verbose_name': 'Шаблон для seo',
                'verbose_name_plural': 'Шаблоны для seo',
                'ordering': ['priority_order', 'id'],
            },
        ),
        migrations.CreateModel(
            name='PageComponent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('view_order', models.IntegerField(default=1, verbose_name='Порядок отображения')),
                ('component', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='garpix_page.basecomponent', verbose_name='Компонент')),
                ('page', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='garpix_page.basepage', verbose_name='Страница')),
            ],
            options={
                'verbose_name': 'Компонент страницы',
                'verbose_name_plural': 'Компоненты страницы',
                'ordering': ('view_order',),
                'unique_together': {('component', 'page')},
            },
        ),
        migrations.CreateModel(
            name='GarpixPageSiteConfiguration',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('robots_txt', models.TextField(default='User-agent: *\nDisallow: /admin/\nDisallow: /api/', verbose_name='Содержимое файла robots.txt')),
                ('sitemap_frequency', models.CharField(choices=[('always', 'always'), ('hourly', 'hourly'), ('daily', 'daily'), ('weekly', 'weekly'), ('monthly', 'monthly'), ('yearly', 'yearly'), ('never', 'never')], default='always', max_length=7, verbose_name='Sitemap changefreq')),
                ('site', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sites.site')),
            ],
            options={
                'verbose_name': 'Настройки',
                'verbose_name_plural': 'Настройки',
            },
        ),
        migrations.AddField(
            model_name='basecomponent',
            name='pages',
            field=models.ManyToManyField(blank=True, related_name='components', through='garpix_page.PageComponent', to='garpix_page.BasePage', verbose_name='Страницы для отображения'),
        ),
        migrations.AddField(
            model_name='basecomponent',
            name='polymorphic_ctype',
            field=models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='polymorphic_garpix_page.basecomponent_set+', to='contenttypes.contenttype'),
        ),
    ]
