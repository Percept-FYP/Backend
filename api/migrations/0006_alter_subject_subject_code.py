# Generated by Django 3.2.3 on 2021-06-02 14:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_auto_20210602_1952'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subject',
            name='subject_code',
            field=models.TextField(max_length=40, unique=True),
        ),
    ]
