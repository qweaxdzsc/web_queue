# Generated by Django 3.1 on 2020-08-20 05:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_queue', '0009_auto_20200816_1231'),
    ]

    operations = [
        migrations.AddField(
            model_name='waitlist',
            name='exec_app',
            field=models.CharField(default='fluent_solver', max_length=128, verbose_name='执行主流程'),
            preserve_default=False,
        ),
    ]
