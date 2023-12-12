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
    class Meta:
        model = models.Object
        fields = ["type", "notes"]


class BorrowSerializer(serializers.ModelSerializer):
    owner = serializers.PrimaryKeyRelatedField(queryset=models.UserProfile.objects.all())
    borrower = serializers.PrimaryKeyRelatedField(allow_null=True, queryset=models.UserProfile.objects.all())
    object = ObjectSerializer()

    def create(self, validated_data):
        print(validated_data)
        object = models.Object.objects.create(**validated_data.pop('object'))
        borrow = models.Borrow.objects.create(object=object, **validated_data)
        return borrow

    class Meta:
        model = models.Borrow
        fields = [
            "owner", 
            "borrower", 
            "borrowing_date", 
            "due_date",
            "status",
            "object",
            "notes",
        ]