from articles.models import ReadingHistory
from .article_factory import ArticleFactory
from faker import Faker
import factory
from .user_factory import UserFactory

fake = Faker()


class ReadingHistoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ReadingHistory

    id = factory.Faker('pyint', min_value=1, max_value=100000)
    article = factory.SubFactory(ArticleFactory)
    user = factory.SubFactory(UserFactory)
