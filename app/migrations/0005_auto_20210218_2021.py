# Generated by Django 3.1.6 on 2021-02-18 20:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_auto_20210218_2006'),
    ]

    operations = [
        migrations.AlterField(
            model_name='application',
            name='intial_approval',
            field=models.CharField(blank=True, choices=[('approve', 'Approve'), ('reject', 'Reject')], max_length=50, verbose_name='Manager Decision'),
        ),
        migrations.AlterField(
            model_name='application',
            name='manager_comments',
            field=models.TextField(blank=True, verbose_name='Manager Comments'),
        ),
        migrations.AlterField(
            model_name='application',
            name='staff_comments',
            field=models.TextField(blank=True, verbose_name='Comments'),
        ),
    ]
