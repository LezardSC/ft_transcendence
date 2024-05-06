# Generated by Django 4.2.9 on 2024-04-29 16:06

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_alter_customuser_n_games_played_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='n_games_played',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='rank',
            field=models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(50)]),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='winrate',
            field=models.DecimalField(decimal_places=4, default=0, max_digits=4, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(1)]),
        ),
    ]
