from djoser.serializers import UserCreateSerializer, UserCreateSerializer as BaseUserRegistrationSerializer
from django.contrib.auth import get_user_model
from geo.models import Farmer
from geo.serializers import FarmerSerializer
from rest_framework import serializers


User = get_user_model()


class UserCreateSerializer(serializers.ModelSerializer):
    farmer = FarmerSerializer()

    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = ('username', 'password', 'farmer')

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username']
        )
        user.set_password(validated_data['password'])
        user.save()
        farmer_data = validated_data.pop('farmer')
        farmer = Farmer.objects.create(
            user=user,
            name=farmer_data['name'],
            phone=farmer_data['phone'],
            date_of_birth=farmer_data['date_of_birth']
        )
        return user


