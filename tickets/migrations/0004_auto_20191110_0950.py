# Generated by Django 2.2.7 on 2019-11-10 09:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tickets', '0003_ticket_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticket',
            name='location',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='tickets.Location'),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='has_case',
            field=models.BooleanField(verbose_name='Case?'),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='has_charger',
            field=models.BooleanField(verbose_name='Charger?'),
        ),
    ]
