from users.models import Follow
from faker import Faker
import factory
from .user_factory import UserFactory

fake = Faker()


class FollowFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Follow

    id = factory.Faker('pyint', min_value=1, max_value=100000)
    follower = factory.SubFactory(UserFactory)
    followee = factory.SubFactory(UserFactory)
