from articles.models import Notification
from faker import Faker
import factory
from .user_factory import UserFactory

fake = Faker()


class NotificationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Notification

    id = factory.Faker('pyint', min_value=1, max_value=100000)
    user = factory.SubFactory(UserFactory)
    message = factory.LazyAttribute(lambda _: fake.text())
