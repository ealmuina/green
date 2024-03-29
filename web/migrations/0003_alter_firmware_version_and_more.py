# Generated by Django 4.0.4 on 2022-09-07 16:36

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('web', '0002_alter_firmware_file_alter_firmware_version'),
    ]

    operations = [
        migrations.AlterField(
            model_name='firmware',
            name='version',
            field=models.PositiveIntegerField(),
        ),
        migrations.AlterUniqueTogether(
            name='firmware',
            unique_together={('node_type', 'version')},
        ),
    ]
