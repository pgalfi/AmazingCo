# Generated by Django 2.2.4 on 2019-08-05 12:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('branches', '0008_auto_20190805_1408'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='office',
            name='next_pos',
        ),
        migrations.AddField(
            model_name='office',
            name='desc_count',
            field=models.BigIntegerField(default=0),
        ),
    ]
