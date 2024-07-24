from articles.models import (
    Article, Topic, ArticleStatus, Comment, Favorite,
    Clap, ReadingHistory, Follow, Pin, Notification, FAQ)
from faker import Faker
import factory
from .user_factory import UserFactory

fake = Faker()


class TopicFactory(factory.django.DjangoModelFactory):
    """ This class will create fake data for topic """

    class Meta:
        model = Topic

    id = factory.Faker('pyint', min_value=1, max_value=100000)
    name = factory.LazyAttribute(lambda _: fake.word())


class ArticleFactory(factory.django.DjangoModelFactory):
    """ This class will create fake data for article """

    class Meta:
        model = Article

    id = factory.Faker('pyint', min_value=1, max_value=100000)
    title = factory.LazyAttribute(lambda _: fake.sentence())
    summary = factory.LazyAttribute(lambda _: fake.text())
    status = ArticleStatus.PUBLISH
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


class CommentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Comment

    id = factory.Faker('pyint', min_value=1, max_value=100000)
    content = factory.Faker('sentence')
    article = factory.SubFactory(ArticleFactory)
    user = factory.SubFactory(UserFactory)


class FavoriteFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Favorite

    id = factory.Faker('pyint', min_value=1, max_value=100000)
    user = factory.SubFactory(UserFactory)
    article = factory.SubFactory(ArticleFactory)


class ClapFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Clap

    id = factory.Faker('pyint', min_value=1, max_value=100000)
    article = factory.SubFactory(ArticleFactory)
    user = factory.SubFactory(UserFactory)
    count = factory.Faker('pyint', min_value=1, max_value=50)


class ReadingHistoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ReadingHistory

    id = factory.Faker('pyint', min_value=1, max_value=100000)
    article = factory.SubFactory(ArticleFactory)
    user = factory.SubFactory(UserFactory)


class FollowFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Follow

    id = factory.Faker('pyint', min_value=1, max_value=100000)
    follower = factory.SubFactory(UserFactory)
    followee = factory.SubFactory(UserFactory)


class PinFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Pin

    user = factory.SubFactory(UserFactory)
    article = factory.SubFactory(ArticleFactory)


class NotificationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Notification

    id = factory.Faker('pyint', min_value=1, max_value=100000)
    user = factory.SubFactory(UserFactory)
    message = factory.LazyAttribute(lambda _: fake.text())


class FAQFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = FAQ

    id = factory.Faker('pyint', min_value=1, max_value=100000)
    question = factory.LazyAttribute(lambda _: fake.text())
    answer = factory.LazyAttribute(lambda _: fake.text())
