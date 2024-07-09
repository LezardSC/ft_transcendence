# Generated by Django 4.2.9 on 2024-06-27 14:08

import django.core.validators
from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TournamentMatch',
            fields=[
                ('lobby_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('round', models.IntegerField(default=1)),
                ('player1', models.CharField(default='', max_length=100)),
                ('player2', models.CharField(blank=True, default='', max_length=100, null=True)),
                ('winner', models.CharField(blank=True, max_length=15, null=True)),
                ('score_player_1', models.IntegerField(default=0)),
                ('score_player_2', models.IntegerField(default=0)),
                ('finished', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Tournament',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=15, unique=True)),
                ('max_players', models.IntegerField(validators=[django.core.validators.MinValueValidator(2), django.core.validators.MaxValueValidator(9)])),
                ('started', models.BooleanField(default=False)),
                ('finished', models.BooleanField(default=False)),
                ('max_round', models.IntegerField(default=1)),
                ('current_round', models.IntegerField(default=1)),
                ('matchups', models.ManyToManyField(blank=True, to='tournaments.tournamentmatch')),
            ],
        ),
    ]
