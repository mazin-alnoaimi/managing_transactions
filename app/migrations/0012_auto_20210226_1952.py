# Generated by Django 3.1.7 on 2021-02-26 19:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0011_auto_20210226_1842'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='application',
            options={},
        ),
        migrations.AlterField(
            model_name='application',
            name='app_no',
            field=models.CharField(blank=True, max_length=50, verbose_name='Application No'),
        ),
        migrations.AlterField(
            model_name='application',
            name='fh_building_no',
            field=models.IntegerField(default=0, verbose_name='Building No'),
        ),
        migrations.AlterField(
            model_name='application',
            name='fh_flat_no',
            field=models.IntegerField(default=0, verbose_name='Flat No'),
        ),
        migrations.AlterField(
            model_name='application',
            name='fh_road_no',
            field=models.IntegerField(default=0, verbose_name='Road No'),
        ),
        migrations.AlterField(
            model_name='application',
            name='full_en_name',
            field=models.CharField(blank=True, max_length=250, verbose_name='Commercial Eng Name'),
        ),
    ]
