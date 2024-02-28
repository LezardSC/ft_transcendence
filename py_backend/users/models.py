from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError

MIN_LEN_USERNAME = 3
MIN_LEN_PASSWORD = 6
FORBIDDEN_CHARS = "+/*.,!#%^&"

class CustomUser(AbstractUser):
	class Meta:
		verbose_name = 'Custom User'

	email = models.EmailField(unique=True)
	title = models.CharField(max_length=100, null=True)
	banner = models.ImageField(null=True)
	profil_picture = models.ImageField(null=True)
	winrate = models.DecimalField(max_digits=4, decimal_places=4, validators=[MinValueValidator(0), MaxValueValidator(1)], null=True)
	rank = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(50)], null=True)
	n_games_played = models.IntegerField(null=True)
	# groups = models.ManyToManyField('auth.Group', related_name='custom_user_set')
	# user_permissions = models.ManyToManyField('auth.Permission', related_name='custom_user_set')

	def __str__(self):
		return f'{self.username}'

	def clean(self):
		super().clean()
		if self.username and len(self.username) < MIN_LEN_USERNAME:
			raise ValidationError({'username': 'Username is too short'})
		if self.username:
			for char in FORBIDDEN_CHARS:
				if char in self.username:
					raise ValidationError({'username': 'Username contains forbidden characters'})
		if self.password and len(self.password) < MIN_LEN_PASSWORD:
			raise ValidationError({'password': 'Password is too short'})

class Tournament(models.Model):
	
	name = models.fields.CharField(max_length=100)
	# host = models.ForeignKey(CustomUser, null=True, on_delete=models.SET_NULL)
	winner = models.fields.CharField(max_length=100, unique=True, null=True)

	n_players = models.IntegerField(validators=[MinValueValidator(2), MaxValueValidator(32)])
	date = models.DateTimeField()

	def __str__(self):
		return f'{self.name}'

class Leaderboard(models.Model):

	total_games_played = models.IntegerField()
	total_tournaments_played = models.IntegerField()
	total_current_tournaments = models.IntegerField()

	def __str__(self):
		return f'Leaderboard'