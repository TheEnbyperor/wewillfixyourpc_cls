# Generated by Django 2.2.7 on 2020-01-18 15:16

import ckeditor_uploader.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sale', '0002_item_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='changes_made',
            field=ckeditor_uploader.fields.RichTextUploadingField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='item',
            name='condition',
            field=models.CharField(default='', max_length=255),
            preserve_default=False,
        ),
    ]
