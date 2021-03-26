from rest_framework import serializers

from .models import CustomUser

"""User should actually be thought of as a researcher
so we name the User serializer as ResearcherSerializer"""
class ResearcherSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'first_name', 'last_name', 'email', 'username', 'organization' ]
        