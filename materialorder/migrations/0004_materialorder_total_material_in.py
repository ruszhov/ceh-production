# Generated by Django 2.0.7 on 2018-08-30 08:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('materialorder', '0003_auto_20180724_1609'),
    ]

    operations = [
        migrations.AddField(
            model_name='materialorder',
            name='total_material_in',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=9, null=True, verbose_name='Всього, м.кв'),
        ),
    ]
