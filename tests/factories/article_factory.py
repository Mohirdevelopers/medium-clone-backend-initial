from articles.models import Article
from faker import Faker
import factory
from .user_factory import UserFactory

fake = Faker()


class ArticleFactory(factory.django.DjangoModelFactory):
    """ This class will create fake data for article """

    class Meta:
        model = Article

    id = factory.Faker('pyint', min_value=1, max_value=100000)
    title = factory.LazyAttribute(lambda _: fake.sentence())
    summary = factory.LazyAttribute(lambda _: fake.text())
    status = "publish"
    content = factory.LazyAttribute(lambda _: fake.text())
    thumbnail = fake.image_url()[:30]
    author = factory.SubFactory(UserFactory)

    @factory.post_generation
    def topics(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for topic in extracted:
                self.topics.add(topic)
