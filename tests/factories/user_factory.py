from django.contrib.auth import get_user_model
from faker import Faker
import factory

fake = Faker()

User = get_user_model()


class UserFactory(factory.django.DjangoModelFactory):
    """This class will create fake data for user"""

    class Meta:
        model = User

    id = factory.Faker('pyint', min_value=1, max_value=100000)
    username = factory.LazyFunction(fake.user_name)
    email = factory.LazyFunction(fake.email)
    first_name = fake.first_name()
    last_name = fake.last_name()
    middle_name = fake.last_name()
    is_staff = False
    is_active = True

    password = factory.PostGenerationMethodCall('set_password', fake.password())

    avatar = fake.image_url()[:30]
