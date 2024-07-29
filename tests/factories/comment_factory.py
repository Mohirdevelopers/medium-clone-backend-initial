from articles.models import Comment
from .article_factory import ArticleFactory
from faker import Faker
import factory
from .user_factory import UserFactory

fake = Faker()


class CommentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Comment

    id = factory.Faker('pyint', min_value=1, max_value=100000)
    content = factory.Faker('sentence')
    article = factory.SubFactory(ArticleFactory)
    user = factory.SubFactory(UserFactory)
