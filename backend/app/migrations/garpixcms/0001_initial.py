# Generated by Django 3.2.19 on 2023-06-22 08:51

import ckeditor_uploader.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('garpix_page', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Page',
            fields=[
                ('basepage_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='garpix_page.basepage')),
                ('content', ckeditor_uploader.fields.RichTextUploadingField(blank=True, default='', verbose_name='Содержание')),
                ('content_ru', ckeditor_uploader.fields.RichTextUploadingField(blank=True, default='', null=True, verbose_name='Содержание')),
            ],
            options={
                'verbose_name': 'Страница',
                'verbose_name_plural': 'Страницы',
                'ordering': ('-created_at',),
            },
            bases=('garpix_page.basepage',),
        ),
    ]
