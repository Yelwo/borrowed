from pytest_factoryboy import register

from tests import factories

register(factories.UserFactory)
register(factories.UserProfileFactory)
register(factories.ObjectFactory)
register(factories.BorrowFactory)