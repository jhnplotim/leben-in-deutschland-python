from django.shortcuts import render
from django.contrib.auth.models import User, Group
from quickstart.models import State
from rest_framework import viewsets
from rest_framework import permissions
from quickstart.serializers import UserSerializer, GroupSerializer, StateSerializer


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
    queryset = State.objects.all()
    serializer_class = StateSerializer
    permission_classes = [permissions.DjangoModelPermissions]
