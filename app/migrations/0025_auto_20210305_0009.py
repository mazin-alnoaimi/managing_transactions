# Generated by Django 3.1.7 on 2021-03-05 00:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0024_auto_20210228_2142'),
    ]

    operations = [
        migrations.RenameField(
            model_name='application',
            old_name='app_status',
            new_name='app_current_status',
        ),
        migrations.AddField(
            model_name='application',
            name='app_next_status',
            field=models.CharField(default='Draft', max_length=50, verbose_name='Status'),
        ),
        migrations.AddField(
            model_name='application',
            name='app_status_index',
            field=models.IntegerField(default=0),
        ),
    ]