from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
from PIL import Image
# from .models import FriendRequest

MIN_LEN_USERNAME = 3
SPECIAL_CHARS = "+/*.,!#%^&\{}[]=:;\'\"`~"

class CustomUser(AbstractUser):
	class Meta:
		verbose_name = 'Custom User'

	email = models.EmailField(unique=True)
	title = models.CharField(max_length=50, null=True)
	avatar = models.ImageField(default='avatar.jpg', upload_to='profile_pictures')
	bio = models.CharField(max_length=500, null=True)
	banner = models.ImageField(null=True)
	winrate = models.DecimalField(max_digits=4, decimal_places=4, validators=[MinValueValidator(0), MaxValueValidator(1)], null=True)
	rank = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(50)], null=True)
	n_games_played = models.IntegerField(null=True)
	friends = models.ManyToManyField("self", blank=True)
	# groups = models.ManyToManyField('auth.Group', related_name='custom_user_set')
	# user_permissions = models.ManyToManyField('auth.Permission', related_name='custom_user_set')
	
	def clean(self):
		super().clean()
		if self.username:
			if len(self.username) < MIN_LEN_USERNAME:
				raise ValidationError({'username': 'Username is too short'})
			if contains_special_char(self.username):
				raise ValidationError({'username': 'Username contains forbidden characters'})
	
	def save(self, *args, **kwargs):
		super().save(*args, **kwargs)
		img = Image.open(self.avatar.path)
		if img.height > 300 or img.width > 300:
			output_size = (300, 300)
			img.thumbnail(output_size)
			img.save(self.avatar.path)


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

def contains_special_char(string):
	for char in SPECIAL_CHARS:
		if char in string:
			return True
	return False