# Generated by Django 2.2.7 on 2020-01-25 13:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sale', '0004_auto_20200125_1322'),
    ]

    operations = [
        migrations.AddField(
            model_name='itemcategory',
            name='google_category',
            field=models.CharField(default='', max_length=255),
            preserve_default=False,
        ),
    ]