# Generated by Django 3.2.2 on 2021-07-02 20:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0014_academic_info'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='academic_info',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='api.academic_info'),
        ),
        migrations.AddField(
            model_name='subject',
            name='academic_info',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='api.academic_info'),
        ),
        migrations.AlterField(
            model_name='academic_info',
            name='semester',
            field=models.TextField(max_length=30),
        ),
    ]
