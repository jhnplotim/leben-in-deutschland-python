from django.db import models
from django.core.validators import RegexValidator
from django.utils import timezone

alphanumeric = RegexValidator(r'^[0-9a-zA-Z]*$', 'Only alphanumeric characters are allowed.')


# Create your models here.
class State(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.TextField(max_length=30, blank=False, null=False)
    code = models.TextField(max_length=2, null=False, unique=True, validators=[alphanumeric])
    icon = models.ImageField(blank=False, null=False, upload_to='state_icons')
    added = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'{self.name}'


class Question(models.Model):
    id = models.AutoField(primary_key=True)
    text = models.TextField(blank=False, null=False)
    image = models.ImageField(blank=True, null=True, default=None, upload_to='question_images')
    state = models.ForeignKey(State, on_delete=models.CASCADE, blank=True, null=True, default=None)

    def __str__(self):
        return f'{self.text}'

    def set_image(self, image):
        self.image = image

    def set_state(self, state):
        self.state = state


class Answer(models.Model):
    id = models.AutoField(primary_key=True)
    text = models.TextField(blank=False, null=False)
    is_correct = models.BooleanField(default=False, null=False, blank=False)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, null=False, blank=False)

    def __str__(self):
        return f'{self.text}'

    def set_is_correct(self, is_correct):
        self.is_correct = is_correct
