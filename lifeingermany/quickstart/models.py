from django.db import models
from django.core.validators import RegexValidator
from django.utils import timezone
import base64

alphanumeric = RegexValidator(r'^[0-9a-zA-Z]*$', 'Only alphanumeric characters are allowed.')


# Create your models here.

class StateIcon(models.Model):
    id = models.AutoField(primary_key=True)
    path = models.ImageField(blank=False, null=False, upload_to='state_icons')
    data_base64_string = models.TextField(editable=False)
    
    def save(self, *args, **kwargs):
        if self.path:
            image = self.path.open()
            print(image)
            data_base64 = base64.b64encode(image.read())
            self.data_base64_string = data_base64.decode('utf8')
        return super(StateIcon, self).save(*args, **kwargs)
    
    def __str__(self):
        return f'{self.path.name}'
    
class QuestionImage(models.Model):
    id = models.AutoField(primary_key=True)
    path = models.ImageField(blank=False, null=False, upload_to='question_images')
    data_base64_string = models.TextField(editable=False)
    
    def save(self, *args, **kwargs):
        if self.path:
            image = self.path.open()
            print(image)
            data_base64 = base64.b64encode(image.read())
            self.data_base64_string = data_base64.decode('utf8')
        return super(QuestionImage, self).save(*args, **kwargs)
    
    def __str__(self):
        return f'{self.path.name}'
    
class State(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.TextField(max_length=30, blank=False, null=False)
    code = models.TextField(max_length=2, null=False, unique=True, validators=[alphanumeric])
    icon = models.ForeignKey(StateIcon, on_delete=models.CASCADE, blank=False, null=False)
    added = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'{self.name}'


class Question(models.Model):
    id = models.AutoField(primary_key=True)
    text = models.TextField(blank=False, null=False)
    image = models.ForeignKey(QuestionImage, on_delete=models.SET_NULL, blank=True, null=True, default=None)
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
        