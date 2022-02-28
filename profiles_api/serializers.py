from rest_framework import serializers
from profiles_api import models

class HelloSerializer(serializers.Serializer):
  """Serializes a name field for testing our APIView"""
  name = serializers.CharField(max_length=10)

class UserProfileSerializer(serializers.ModelSerializer):
  """Serializes a user profile object. We need to define a meta class for that"""

  class Meta:
    model = models.UserProfile
    # list all the fields that we need to use the serializer with
    fields = ('id', 'email', 'name', 'password')

    # we want to make the password read only
    extra_kwargs = {
      'password': {
        'write_only': True, # only use to create new objects, not with GET
        'style': {'input_type': 'password'}
      }
    }

  # override default create object that would save password in plain text
  def create(self, validated_data):
    """Create and return a new user"""
    user = models.UserProfile.objects.create_user(
      email=validated_data['email'],
      name=validated_data['name'],
      password=validated_data['password']
    )

    return user

  def update(self, instance, validated_data):
    """Handle updating  user account"""
    if 'password' in validated_data:
      password = validated_data.pop('password')
      instance.set_password(password)

    return super().update(instance, validated_data)