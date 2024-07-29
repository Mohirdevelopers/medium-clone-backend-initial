from articles.models import Clap
from faker import Faker
import factory
from .user_factory import UserFactory
from .article_factory import ArticleFactory

fake = Faker()


class ClapFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Clap

    id = factory.Faker('pyint', min_value=1, max_value=100000)
    article = factory.SubFactory(ArticleFactory)
    user = factory.SubFactory(UserFactory)
    count = factory.Faker('pyint', min_value=1, max_value=50)
