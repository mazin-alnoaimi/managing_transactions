# Generated by Django 3.1.6 on 2021-02-16 22:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0009_auto_20210216_1837'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='organization',
            name='bank_statement_doc',
        ),
        migrations.RemoveField(
            model_name='organization',
            name='cr_doc',
        ),
        migrations.RemoveField(
            model_name='organization',
            name='lmra_agreement',
        ),
    ]
