# Generated by Django 3.1.5 on 2021-01-11 12:13

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Rule',
            fields=[
                ('uid', models.AutoField(primary_key=True, serialize=False)),
                ('source', models.CharField(blank=True, max_length=500)),
                ('destination', models.CharField(blank=True, max_length=500)),
                ('path', models.CharField(blank=True, max_length=500)),
                ('status', models.CharField(max_length=50)),
            ],
        ),
    ]
