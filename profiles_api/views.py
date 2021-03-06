from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication # assigns a token to the user when they log in and all subsequent requests
from rest_framework import filters
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from rest_framework.permissions import IsAuthenticated # blocks access unless the user is authenticated

from profiles_api import models
from profiles_api import serializers
from profiles_api import permissions

# Create your views here.

class HelloApiView(APIView):
  """Test API View"""

  serializer_class = serializers.HelloSerializer

  def get(self,request, format=None):
    """Returns a list of APIView features"""
    an_api_view = [
      'Uses HTTP methods as function (get, post, patch, put, delete)',
      'Is similar to a traditional Django View',
      'Gives you the most control over your application logic',
      'Is mapped manually to URLs',
    ]

    return Response({'message': 'Hello!', 'an_apiview': an_api_view})

  def post(self, request):
    """Create a hello message with our name"""
    serializer = self.serializer_class(data=request.data)

    if serializer.is_valid():
      name = serializer.validated_data.get('name')
      message = f'Hello {name}'
      return Response({'message': message})
    else:
      return Response(
        serializer.errors,
        status=status.HTTP_400_BAD_REQUEST
      )

  def put(self, request, pk=None): #pk is the object id that you want to update
    """Handles updating an object"""
    return Response({'message': 'Object has been updated', 'method': 'PUT'})

  def patch(self, request, pk=None):
    """Handle a partial update of an Object"""
    return Response({'message': 'Object has been updated', 'method': 'PATCH'})

  def delete(self, request, pk=None):
    """Handles deleting an object"""
    return Response({'message': 'Object has been deleted', 'method': 'DELETE'})


class HelloViewSet(viewsets.ViewSet):
  """Test API ViewSet"""

  serializer_class = serializers.HelloSerializer

  def list(self, request):
    """Return a hello message"""

    a_viewset = [
      'Uses actions (list, create, retrieve, update, partial_update',
      'Automatically maps to URLs using Routers',
      'Provides more functionality with less code'
    ]

    return Response({'message': 'Hello!', 'a_viewset': a_viewset})

  def create(self, request):
    """Create a new hello message"""
    serializer = self.serializer_class(data=request.data)

    if serializer.is_valid():
      name = serializer.validated_data.get('name')
      message = f'Hello {name}!'
      return Response({'message': message})
    else:
      return Response(
        serializer.errors,
        status=status.HTTP_400_BAD_REQUEST
      )

  def retrieve(self, request, pk=None):
    """Handles getting an object by id"""
    return Response({'http_method': 'GET'})


  def update(self, request, pk=None):
    """Handles updating an object"""
    return Response({'http_method': 'PUT'})


  def partial_update(self, request, pk=None):
    """Handles updating part of an object"""
    return Response({'http_method': 'PATCH'})

  def destroy(self, request, pk=None):
    """Handle removing an object"""
    return Response({'http_method': 'DELETE'})

class UserProfileViewSet(viewsets.ModelViewSet):
  """Handle creating and updating profiles. Rest framework knows the standard function that you would want to perform on a viewset"""
  serializer_class = serializers.UserProfileSerializer
  queryset = models.UserProfile.objects.all()
  #how the user will authenticate
  authentication_classes = (TokenAuthentication,) #create it as a tuple
  #permission to do certain things
  permission_classes = (permissions.UpdateOwnProfile,)
  #filter user's based on certain values
  filter_backends = (filters.SearchFilter,)
  search_fields = ('name', 'email',)

class UserLoginApiView(ObtainAuthToken):
  """Handle creating user authtication tokens"""
  # needs to be added so that it's visible in the Django admin view
  renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES

class UserProfileFeedViewSet(viewsets.ModelViewSet):
  """Handles creating, reading and updateing profile feed items"""
  authentication_classes = (TokenAuthentication,)
  serializer_class = serializers.ProfileFeedItemSerializer
  queryset = models.ProfileFeedItem.objects.all()
  permission_classes = (permissions.UpdateOwnStatus, IsAuthenticated)

  def perform_create(self, serializer):
    """Sets the user profile to the logged in user"""
    serializer.save(user_profile=self.request.user)
