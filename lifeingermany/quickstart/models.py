from django.db import models
from django.core.validators import RegexValidator
from django.utils import timezone


alphanumeric = RegexValidator(r'^[0-9a-zA-Z]*$', 'Only alphanumeric characters are allowed.')

# Create your models here.
class State(models.Model):
    id = models.TextField(max_length=2, primary_key=True, validators=[alphanumeric])
    name = models.TextField(max_length=30, blank=False, null=False)
    icon = models.ImageField(blank=False, null=False, upload_to='state_icons')
    added = models.DateTimeField(default=timezone.now)