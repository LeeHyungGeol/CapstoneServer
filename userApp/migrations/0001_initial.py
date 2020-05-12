# Generated by Django 3.0.3 on 2020-05-12 11:31

from django.db import migrations, models
import django.db.models.manager


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('password', models.CharField(max_length=128)),
                ('last_login', models.DateTimeField(blank=True, null=True)),
                ('idx', models.AutoField(primary_key=True, serialize=False)),
                ('user_id', models.CharField(blank=True, max_length=100, null=True, unique=True)),
                ('user_nm', models.CharField(blank=True, max_length=50, null=True)),
                ('point', models.IntegerField(blank=True, null=True)),
                ('is_admin', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('date_joined', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'db_table': 'user',
            },
            managers=[
                ('object', django.db.models.manager.Manager()),
            ],
        ),
    ]
