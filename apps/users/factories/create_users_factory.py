import factory

from apps.users.models import User


class UsersFactory(factory.django.DjangoModelFactory):
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    username = factory.Faker('user_name')
    email = factory.Faker('email')
    phone = factory.Faker('phone_number')
    is_active = True
    is_staff = False

    class Meta:
        model = User
