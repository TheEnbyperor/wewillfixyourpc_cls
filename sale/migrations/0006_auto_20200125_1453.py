# Generated by Django 2.2.7 on 2020-01-25 14:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sale', '0005_itemcategory_google_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='mpn',
            field=models.CharField(default='', max_length=255, verbose_name='Manufacturer part number'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='item',
            name='condition',
            field=models.CharField(choices=[('new', 'New'), ('refurbished', 'Refurbished'), ('used', 'Used')], max_length=30),
        ),
    ]
