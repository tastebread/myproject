# Generated by Django 5.1.5 on 2025-02-08 04:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_profile_bio'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='profile_image',
            field=models.ImageField(blank=True, null=True, upload_to='profile_pics/', verbose_name='자기소개'),
        ),
    ]
