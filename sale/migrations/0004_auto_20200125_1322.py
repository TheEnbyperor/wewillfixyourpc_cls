# Generated by Django 2.2.7 on 2020-01-25 13:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sale', '0003_auto_20200118_1516'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='available',
            field=models.BooleanField(default=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='item',
            name='brand',
            field=models.CharField(default='', max_length=255),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='item',
            name='condition',
            field=models.CharField(choices=[('new', 'New'), ('refurbished', 'Refurbished'), ('used', 'Used'), ('used_fair', 'Used - Fair'), ('used_good', 'Used - Good'), ('used_like_new', 'Used - Like ew')], max_length=30),
        ),
        migrations.AlterField(
            model_name='item',
            name='description',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
    ]
