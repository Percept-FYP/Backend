# Generated by Django 3.2.3 on 2021-05-23 16:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='info',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(null=True, upload_to='Images')),
                ('class_name', models.TextField(max_length=30)),
                ('teacher', models.TextField(max_length=30)),
            ],
        ),
    ]
