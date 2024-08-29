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


@pytest.mark.django_db
class TestBorrows:
    def test_lent_list(self, client, user_profile_factory, borrow_factory):
        user_profile = user_profile_factory()
        lent = borrow_factory.create_batch(3, object__owner=user_profile)

        client.force_login(user_profile.user)
        url = reverse('borrows-lent')
        response = client.get(url)

        assert response.data == serializers.BorrowSerializer(lent, many=True).data
    
    def test_lent_doesnt_return_other_users_items(self, client, user_profile_factory, borrow_factory):
        user_profile = user_profile_factory()
        another_user_profile = user_profile_factory()
        lent = borrow_factory.create_batch(3, object__owner=another_user_profile)

        client.force_login(user_profile.user)
        url = reverse('borrows-lent')
        response = client.get(url)

        assert response.data == []

    def test_borrowed_list(self, client, user_profile_factory, borrow_factory):
        user_profile = user_profile_factory()
        borrowed = borrow_factory.create_batch(3, borrower=user_profile, status='borrowed')

        client.force_login(user_profile.user)
        url = reverse('borrows-borrowed')
        response = client.get(url)

        assert response.data == serializers.BorrowSerializer(borrowed, many=True).data
    
    def test_borrowed_doesnt_return_other_users_items(self, client, user_profile_factory, borrow_factory):
        user_profile = user_profile_factory()
        another_user_profile = user_profile_factory()
        borrow_factory.create_batch(3, borrower=another_user_profile, status='borrowed')

        client.force_login(user_profile.user)
        url = reverse('borrows-borrowed')
        response = client.get(url)

        assert response.data == []
    
    def test_borrowed_doesnt_return_returned_items(self, client, user_profile_factory, borrow_factory):
        user_profile = user_profile_factory()
        borrow_factory.create_batch(3, borrower=user_profile, status='returned')

        client.force_login(user_profile.user)
        url = reverse('borrows-borrowed')
        response = client.get(url)

        assert response.data == []
