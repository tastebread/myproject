# Generated by Django 5.1.5 on 2025-02-08 03:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('board', '0002_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='post_images/'),
        ),
    ]
