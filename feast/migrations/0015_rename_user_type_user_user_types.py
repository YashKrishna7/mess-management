# Generated by Django 5.1.7 on 2025-04-03 07:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('feast', '0014_profile'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='user_type',
            new_name='USER_TYPES',
        ),
    ]
