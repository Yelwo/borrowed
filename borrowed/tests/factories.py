import factory

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

    class Meta:
        model = models.Object
