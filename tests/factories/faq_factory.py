from articles.models import FAQ
from faker import Faker
import factory

fake = Faker()


class FAQFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = FAQ

    id = factory.Faker('pyint', min_value=1, max_value=100000)
    question = factory.LazyAttribute(lambda _: fake.text())
    answer = factory.LazyAttribute(lambda _: fake.text())
