# Generated by Django 5.1.5 on 2025-02-24 06:29

import tinymce.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('maze', '0010_remove_mazequestion_unique_maze_question_order_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mazequestion',
            name='question_text',
            field=tinymce.models.HTMLField(),
        ),
    ]
