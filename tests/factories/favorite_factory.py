from articles.models import Favorite
from .article_factory import ArticleFactory
from faker import Faker
import factory
from .user_factory import UserFactory

fake = Faker()

class FavoriteFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Favorite

    id = factory.Faker('pyint', min_value=1, max_value=100000)
    user = factory.SubFactory(UserFactory)
    article = factory.SubFactory(ArticleFactory)
