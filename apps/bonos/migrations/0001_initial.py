# Generated by Django 3.0.6 on 2022-04-08 21:36

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Bono',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('folio', models.CharField(editable=False, max_length=25, null=True, unique=True)),
                ('fecha_reg', models.DateTimeField(auto_now_add=True)),
                ('fecha_mod', models.DateTimeField(auto_now=True)),
                ('activo', models.BooleanField(default=True, editable=False)),
                ('tipo', models.CharField(choices=[('comprado', 'Comprado'), ('vitalicio', 'Vitalicio'), ('cortesia', 'Cortesía'), ('palco', 'Palco')], max_length=10)),
                ('abonado', django.contrib.postgres.fields.jsonb.JSONField()),
                ('ubicacion', django.contrib.postgres.fields.jsonb.JSONField()),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
