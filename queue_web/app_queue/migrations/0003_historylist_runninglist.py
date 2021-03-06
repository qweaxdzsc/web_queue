# Generated by Django 3.0.8 on 2020-07-29 01:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_queue', '0002_auto_20200728_1607'),
    ]

    operations = [
        migrations.CreateModel(
            name='HistoryList',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('account_email', models.EmailField(max_length=254)),
                ('sender_address', models.CharField(max_length=64)),
                ('mission_name', models.CharField(max_length=32)),
                ('mission_data', models.TextField()),
                ('register_time', models.DateTimeField()),
                ('start_time', models.DateTimeField()),
                ('using_time', models.DateTimeField()),
            ],
            options={
                'verbose_name': '历史记录队列',
                'verbose_name_plural': '历史记录队列',
                'ordering': ['start_time'],
            },
        ),
        migrations.CreateModel(
            name='RunningList',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('account_email', models.EmailField(max_length=254)),
                ('sender_address', models.CharField(max_length=64)),
                ('mission_name', models.CharField(max_length=32)),
                ('mission_data', models.TextField()),
                ('register_time', models.DateTimeField()),
                ('start_time', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': '正在计算队列',
                'verbose_name_plural': '正在计算队列',
                'ordering': ['start_time'],
            },
        ),
    ]
