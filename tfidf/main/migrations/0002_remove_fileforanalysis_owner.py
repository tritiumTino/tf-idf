# Generated by Django 3.2.4 on 2021-09-07 11:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='fileforanalysis',
            name='owner',
        ),
    ]
