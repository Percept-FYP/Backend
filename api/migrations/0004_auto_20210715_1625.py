# Generated by Django 3.2.2 on 2021-07-15 10:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_time_table_time'),
    ]

    operations = [
        migrations.RenameField(
            model_name='time_table',
            old_name='time',
            new_name='end_time',
        ),
        migrations.AddField(
            model_name='time_table',
            name='start_time',
            field=models.CharField(max_length=40, null=True),
        ),
    ]
