# Generated by Django 2.1.3 on 2019-03-12 12:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('printorder', '0006_donesteps'),
    ]

    operations = [
        migrations.AddField(
            model_name='donesteps',
            name='updated',
            field=models.DateTimeField(null=True),
        ),
    ]
