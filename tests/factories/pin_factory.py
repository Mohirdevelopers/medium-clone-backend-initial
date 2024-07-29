from articles.models import Pin
from faker import Faker
import factory
from .user_factory import UserFactory
from .article_factory import ArticleFactory

fake = Faker()


class PinFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Pin

    user = factory.SubFactory(UserFactory)
    article = factory.SubFactory(ArticleFactory)
