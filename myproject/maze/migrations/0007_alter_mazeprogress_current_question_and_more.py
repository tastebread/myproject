# Generated by Django 5.1.5 on 2025-02-11 06:16

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('maze', '0006_mazeprogress'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mazeprogress',
            name='current_question',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='maze.mazequestion'),
        ),
        migrations.AlterField(
            model_name='mazequestion',
            name='level',
            field=models.CharField(choices=[('easy', '쉬움'), ('normal', '보통'), ('hard', '어려움')], default='easy', max_length=6),
        ),
        migrations.AlterField(
            model_name='mazequestion',
            name='order',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='mazequestion',
            name='score_value',
            field=models.PositiveIntegerField(default=10),
        ),
        migrations.AlterField(
            model_name='mazequestion',
            name='time_limit',
            field=models.PositiveIntegerField(default=60),
        ),
        migrations.AddConstraint(
            model_name='mazequestion',
            constraint=models.UniqueConstraint(fields=('order',), name='unique_maze_question_order'),
        ),
    ]
