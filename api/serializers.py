from django.contrib.auth.models import User
from app.models import Leads
from rest_framework import serializers

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']


class LeadsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Leads
        fields = '__all__'