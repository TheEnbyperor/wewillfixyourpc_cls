# Generated by Django 3.0.4 on 2020-03-07 16:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0004_customercache'),
    ]

    operations = [
        migrations.AlterField(
            model_name='credential',
            name='username',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
