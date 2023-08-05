# Generated by Django 2.2.13 on 2020-11-19 10:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import starthinker_ui.recipe.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('project', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Recipe',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('token', models.CharField(max_length=8, unique=True)),
                ('reference', models.CharField(default=starthinker_ui.recipe.models.reference_default, max_length=32, unique=True)),
                ('name', models.CharField(max_length=64)),
                ('active', models.BooleanField(default=True)),
                ('manual', models.BooleanField(default=False)),
                ('week', models.CharField(default='["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]', max_length=64)),
                ('hour', models.CharField(default='[3]', max_length=128)),
                ('timezone', models.CharField(blank=True, default='America/Los_Angeles', max_length=32)),
                ('tasks', models.TextField()),
                ('job_utm', models.BigIntegerField(blank=True, default=0)),
                ('job_status', models.TextField(default='{}')),
                ('worker_uid', models.CharField(default='', max_length=128)),
                ('worker_utm', models.BigIntegerField(blank=True, default=0)),
                ('birthday', models.DateField(auto_now_add=True)),
                ('account', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
                ('project', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='project.Project')),
            ],
        ),
    ]
