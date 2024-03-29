from django.shortcuts import render
from django.contrib.auth.models import User, Group
from quickstart.models import State, Answer, Question, QuestionImage, StateIcon
from rest_framework import viewsets
from rest_framework import permissions
from quickstart.serializers import UserSerializer, GroupSerializer, StateSerializer, StateIconSerializer, AnswerSerializer, QuestionSerializer, QuestionImageSerializer


# Create your views here.

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.DjangoModelPermissions]


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.DjangoModelPermissions]

    
class StateViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows States to be viewed or edited.
    """
    queryset = State.objects.all().order_by('-added')
    serializer_class = StateSerializer
    permission_classes = [permissions.DjangoModelPermissions]
    
class StateIconViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows State icons to be viewed or edited.
    """
    queryset = StateIcon.objects.all()
    serializer_class = StateIconSerializer
    permission_classes = [permissions.DjangoModelPermissions]

class QuestionViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Questions to be viewed or edited.
    """
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [permissions.DjangoModelPermissions]
    
    
class QuestionImageViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Question Images to be viewed or edited.
    """
    queryset = QuestionImage.objects.all()
    serializer_class = QuestionImageSerializer
    permission_classes = [permissions.DjangoModelPermissions]


class AnswerViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Answers to be viewed or edited.
    """
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer
    permission_classes = [permissions.DjangoModelPermissions]

