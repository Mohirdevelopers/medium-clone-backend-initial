from articles.models import Topic
from faker import Faker
import factory


fake = Faker()


class TopicFactory(factory.django.DjangoModelFactory):
    """ This class will create fake data for topic """

    class Meta:
        model = Topic

    id = factory.Faker('pyint', min_value=1, max_value=100000)
    name = factory.LazyAttribute(lambda _: fake.word())
