# Generated by Django 3.2.3 on 2021-06-07 13:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_auto_20210602_2026'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subject',
            name='subject_code',
            field=models.TextField(max_length=40),
        ),
        migrations.AlterField(
            model_name='teacher',
            name='name',
            field=models.TextField(max_length=40, unique=True),
        ),
    ]
