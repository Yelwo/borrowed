import factory
import factory.fuzzy

from objects import models


class UserFactory(factory.django.DjangoModelFactory):
    username = factory.Faker('email')

    class Meta:
        model = models.User

class UserProfileFactory(factory.django.DjangoModelFactory):
    user = factory.SubFactory(UserFactory)

    class Meta:
        model = models.UserProfile

class ObjectFactory(factory.django.DjangoModelFactory):
    owner = factory.SubFactory(UserProfileFactory)
    type = factory.Faker('words')

    class Meta:
        model = models.Object

class BorrowFactory(factory.django.DjangoModelFactory):
    borrower = factory.SubFactory(UserProfileFactory)
    borrowing_date = factory.Faker('date')
    due_date = factory.Faker('date')
    status = factory.fuzzy.FuzzyChoice(['Borrowed', 'Returned'])
    object = factory.SubFactory(ObjectFactory)

    @classmethod
    def _adjust_kwargs(cls, **kwargs):
        if kwargs['status'] == 'Returned':
            kwargs['borrower'] = None
        return kwargs

    class Meta:
        model = models.Borrow