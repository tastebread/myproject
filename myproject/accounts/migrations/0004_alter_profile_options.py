# Generated by Django 5.1.5 on 2025-02-11 06:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_alter_profile_profile_image'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='profile',
            options={'ordering': ['user'], 'verbose_name': '프로필', 'verbose_name_plural': '프로필들'},
        ),
    ]
