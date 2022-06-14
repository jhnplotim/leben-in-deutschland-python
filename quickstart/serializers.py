from django.contrib.auth.models import User, Group
from quickstart.models import State, StateIcon, Answer, Question, QuestionImage
from rest_framework import serializers


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']

class StateSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = State
        fields = ['id', 'url', 'name', 'code', 'icon', 'added']

class AnswerSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Answer
        fields = ['id', 'text', 'is_correct', 'question']

class QuestionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Question
        fields = ['id', 'text', 'image', 'state']
        
class QuestionImageSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = QuestionImage
        fields = ['id', 'data_base64_string']
        
class StateIconSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = StateIcon
        fields = ['id', 'data_base64_string']


