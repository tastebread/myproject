# Generated by Django 5.1.5 on 2025-02-08 07:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('board', '0010_post_attached_file'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='tag',
            new_name='tags',
        ),
    ]
