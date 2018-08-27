# Generated by Django 2.0.7 on 2018-07-23 09:25

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CampaignName',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_of_new_camp', models.CharField(max_length=50)),
                ('description', models.CharField(blank=True, max_length=30)),
            ],
            options={
                'verbose_name': 'Кампанія',
                'verbose_name_plural': 'Кампанії',
                'ordering': ['name_of_new_camp'],
            },
        ),
        migrations.CreateModel(
            name='Material',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_of_material', models.CharField(max_length=50)),
                ('description', models.CharField(blank=True, max_length=50)),
                ('total_m_kv_per_month', models.DecimalField(blank=True, decimal_places=3, max_digits=9, null=True)),
                ('total_m_kv', models.DecimalField(blank=True, decimal_places=3, max_digits=12, null=True)),
            ],
            options={
                'verbose_name': 'Матеріал',
                'verbose_name_plural': 'Матеріали',
                'ordering': ['name_of_material'],
            },
        ),
        migrations.CreateModel(
            name='OfficeManager',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_of_manager', models.CharField(max_length=30)),
                ('description', models.CharField(blank=True, max_length=50)),
            ],
            options={
                'verbose_name': 'Менеджер',
                'verbose_name_plural': 'Менеджери',
                'ordering': ['name_of_manager'],
            },
        ),
        migrations.CreateModel(
            name='PrintOrder',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image_url', models.CharField(max_length=200)),
                ('prioritet', models.CharField(choices=[('NO', 'Ні'), ('YES', 'Так')], default='1', max_length=9)),
                ('print_width', models.FloatField(null=True)),
                ('print_height', models.FloatField(null=True)),
                ('number', models.IntegerField(default=None)),
                ('m_kv', models.DecimalField(decimal_places=3, max_digits=9, null=True)),
                ('description', models.TextField(blank=True, max_length=100)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('created_by', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='created_by', to=settings.AUTH_USER_MODEL)),
                ('manager', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='printorder.OfficeManager')),
                ('material', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='printorder.Material')),
                ('name_of_camp', models.ForeignKey(default=None, on_delete=django.db.models.deletion.DO_NOTHING, to='printorder.CampaignName')),
            ],
            options={
                'verbose_name': 'Замовлення друку',
                'verbose_name_plural': 'Список замовлень друку',
            },
        ),
        migrations.CreateModel(
            name='PrintStatus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(blank=True, max_length=20)),
            ],
            options={
                'verbose_name': 'Статус друку',
                'verbose_name_plural': 'Статуси друку',
                'ordering': ['status'],
            },
        ),
        migrations.AddField(
            model_name='printorder',
            name='status',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='printorder.PrintStatus'),
        ),
        migrations.AddField(
            model_name='printorder',
            name='updated_by',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='updated_by', to=settings.AUTH_USER_MODEL),
        ),
    ]
