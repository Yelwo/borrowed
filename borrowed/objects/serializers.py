from rest_framework import serializers
from . import models


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = ['username', 'email']


class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = models.UserProfile
        fields = ["user"]

    def create(self, validated_data):
        user = models.User.objects.create(**validated_data.pop('user'))
        user_profile = models.UserProfile.objects.create(user=user, **validated_data)
        return user_profile


class ObjectSerializer(serializers.ModelSerializer):
    owner = serializers.PrimaryKeyRelatedField(queryset=models.UserProfile.objects.all())

    class Meta:
        model = models.Object
        fields = ["owner", "type", "notes"]


class BorrowSerializer(serializers.ModelSerializer):
    borrower = serializers.PrimaryKeyRelatedField(allow_null=True, queryset=models.UserProfile.objects.all())
    object = ObjectSerializer()

    class Meta:
        model = models.Borrow
        fields = [
            "borrower", 
            "borrowing_date", 
            "due_date",
            "status",
            "object",
            "notes",
        ]