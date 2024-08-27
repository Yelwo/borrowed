import pytest

from django.urls import reverse

from objects import serializers


@pytest.mark.django_db
class TestObjects:
    def test_list(self, client, user_profile_factory, object_factory):
        user_profile = user_profile_factory()
        objects = object_factory.create_batch(5, owner=user_profile)

        client.force_login(user_profile.user)
        url = reverse('objects-list')
        response = client.get(url)

        assert response.data == serializers.ObjectSerializer(objects, many=True).data

    def test_list_has_only_users_objects(self, client, user_profile_factory, object_factory):
        user_profile = user_profile_factory()
        users_object = object_factory(owner=user_profile)
        someone_elses_object = object_factory()

        assert someone_elses_object.owner != user_profile
        client.force_login(user_profile.user)
        url = reverse('objects-list')
        response = client.get(url)

        assert response.data == [serializers.ObjectSerializer(users_object).data]
