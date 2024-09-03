import datetime
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
class TestLent:
    def test_list(self, client, user_profile_factory, borrow_factory):
        user_profile = user_profile_factory()
        lent = borrow_factory.create_batch(3, object__owner=user_profile)

        client.force_login(user_profile.user)
        url = reverse('borrows-lent')
        response = client.get(url)

        assert response.data == serializers.BorrowSerializer(lent, many=True).data
    
    def test_doesnt_return_other_users_items(self, client, user_profile_factory, borrow_factory):
        user_profile = user_profile_factory()
        another_user_profile = user_profile_factory()
        lent = borrow_factory.create_batch(3, object__owner=another_user_profile)

        client.force_login(user_profile.user)
        url = reverse('borrows-lent')
        response = client.get(url)

        assert response.data == []


@pytest.mark.django_db
class TestBorrowed:
    def test_list(self, client, user_profile_factory, borrow_factory):
        user_profile = user_profile_factory()
        borrowed = borrow_factory.create_batch(3, borrower=user_profile, status='borrowed')

        client.force_login(user_profile.user)
        url = reverse('borrows-borrowed')
        response = client.get(url)

        assert response.data == serializers.BorrowSerializer(borrowed, many=True).data
    
    def test_doesnt_return_other_users_items(self, client, user_profile_factory, borrow_factory):
        user_profile = user_profile_factory()
        another_user_profile = user_profile_factory()
        borrow_factory.create_batch(3, borrower=another_user_profile, status='borrowed')

        client.force_login(user_profile.user)
        url = reverse('borrows-borrowed')
        response = client.get(url)

        assert response.data == []
    
    def test_doesnt_return_returned_items(self, client, user_profile_factory, borrow_factory):
        user_profile = user_profile_factory()
        borrow_factory.create_batch(3, borrower=user_profile, status='returned')

        client.force_login(user_profile.user)
        url = reverse('borrows-borrowed')
        response = client.get(url)

        assert response.data == []


@pytest.mark.django_db
class TestBorrow:
    def test_positive(self, client, user_profile_factory, object_factory):
        borrower = user_profile_factory()
        object = object_factory()
        data = {
            'borrower': borrower.pk,
            'borrowing_date': str(datetime.date.today()),
            'due_date': str(datetime.date.today() + datetime.timedelta(days=3)),
            'object': object.pk,
        }

        client.force_login(object.owner.user)
        url = reverse('borrows-borrow')
        response = client.post(url, data=data)
        
        data['status'] = 'borrowed'
        data['notes'] = ''
        assert response.data == data

    def test_cant_create_returned_borrow(self, client, user_profile_factory, object_factory):
        borrower = user_profile_factory()
        object = object_factory()
        data = {
            'borrower': borrower.pk,
            'borrowing_date': str(datetime.date.today()),
            'due_date': str(datetime.date.today() + datetime.timedelta(days=3)),
            'object': object.pk,
            'status': 'returned',
        }

        client.force_login(object.owner.user)
        url = reverse('borrows-borrow')
        response = client.post(url, data=data)
        
        assert response.status_code == 400
        assert response.data == {"status": "You can't create returned borrow"}
    
    def test_user_cant_borrow_their_own_items(self, client, user_profile_factory, object_factory):
        borrower = user_profile_factory()
        object = object_factory(owner=borrower)
        data = {
            'borrower': borrower.pk,
            'borrowing_date': str(datetime.date.today()),
            'due_date': str(datetime.date.today() + datetime.timedelta(days=3)),
            'object': object.pk,
        }

        client.force_login(object.owner.user)
        url = reverse('borrows-borrow')
        response = client.post(url, data=data)
        
        assert response.status_code == 400
        assert response.data == {"borrower": "You can't borrow your own items"}

    def test_object_is_already_borrowed(self, client, user_profile_factory, object_factory, borrow_factory):
        borrower = user_profile_factory()
        object = object_factory()
        borrow_factory(status='borrowed', object=object)
        data = {
            'borrower': borrower.pk,
            'borrowing_date': str(datetime.date.today()),
            'due_date': str(datetime.date.today() + datetime.timedelta(days=3)),
            'object': object.pk,
        }

        client.force_login(object.owner.user)
        url = reverse('borrows-borrow')
        response = client.post(url, data=data)
        
        assert response.status_code == 400
        assert response.data == {"object": "Object has been already borrowed"}


@pytest.mark.django_db
class TestReturBorrowedObject:
    def test_positive(self, client, borrow_factory):
        borrow = borrow_factory(status='borrowed')

        client.force_login(borrow.borrower.user)
        url = reverse('borrows-return-borrowed-object', kwargs={'pk': borrow.pk})
        response = client.put(url)

        assert response.status_code == 200
        assert response.data['status'] == 'returned' 

    def test_cant_return_object_you_didnt_borrow(self, client, user_profile_factory, borrow_factory):
        user_profile = user_profile_factory()
        borrow = borrow_factory()

        client.force_login(user_profile.user)
        url = reverse('borrows-return-borrowed-object', kwargs={'pk': borrow.pk})
        response = client.put(url)

        assert response.status_code == 404

    def test_owner_cant_return_object(self, client, user_profile_factory, object_factory, borrow_factory):
        borrow = borrow_factory()

        client.force_login(borrow.object.owner.user)
        url = reverse('borrows-return-borrowed-object', kwargs={'pk': borrow.pk})
        response = client.put(url)

        assert response.status_code == 400
        assert response.data == {"borrower": "Logged in user is not a borrower"}