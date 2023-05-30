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

class StateSerializer(serializers.ModelSerializer):
    class Meta:
        model = State
        fields = ['id', 'url', 'name', 'code', 'icon', 'added']

class AnswerSerializer(serializers.ModelSerializer):
    isCorrect = serializers.BooleanField(source='is_correct')
    
    class Meta:
        model = Answer
        fields = ['id', 'text', 'isCorrect']

class QuestionSerializer(serializers.ModelSerializer):
    title = serializers.CharField(source='text')
    answers = AnswerSerializer(source='answer_set', many=True)  
    class Meta:
        model = Question
        fields = ['id', 'title', 'image', 'state', "answers"]
        
class QuestionImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionImage
        fields = ['id', 'data_base64_string']
        depth = 1
        
class StateIconSerializer(serializers.ModelSerializer):
    class Meta:
        model = StateIcon
        fields = ['id', 'data_base64_string']


