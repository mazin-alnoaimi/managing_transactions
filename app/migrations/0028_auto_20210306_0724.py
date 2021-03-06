# Generated by Django 3.1.7 on 2021-03-06 07:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0027_auto_20210305_1952'),
    ]

    operations = [
        migrations.AlterField(
            model_name='application',
            name='app_type',
            field=models.CharField(choices=[('initial', 'Initial Approval'), ('final', 'Final Approval'), ('renew', 'Renewal License'), ('cancel', 'Cancel License')], default='Initial Approval', max_length=50, verbose_name='Application Type'),
        ),
    ]