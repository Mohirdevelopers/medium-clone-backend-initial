import pytest
from rest_framework import status


@pytest.mark.order(1)
def test_follow_model_exists():
    """
    The function test follow model exists.
    """
    from users.models import Follow
    assert Follow, "Follow model not created"


@pytest.mark.order(2)
def test_author_follow_view_exists():
    """
    The function test follow view exists.
    """
    from users.views import AuthorFollowView
    assert AuthorFollowView, "AuthorFollowView view not created"


@pytest.fixture()
@pytest.mark.order(3)
def follow_author_data(request, user_factory):
    """
    Fixture to provide data for follow author tests.
    """
    from tests.factories.follow_factory import FollowFactory
    from tests.factories.article_factory import ArticleFactory

    author = user_factory()
    user = user_factory()
    article = ArticleFactory(author=author)

    def valid_data():
        return 201, article, user, author

    def invalid_data():
        return 404, article, user, None

    def already_following():
        FollowFactory.create(follower=user, followee=author)
        return 200, article, user, author

    data = {
        "valid_data": valid_data,
        "invalid_data": invalid_data,
        "already_following": already_following
    }

    return data[request.param]()

@pytest.mark.django_db
@pytest.mark.order(4)
@pytest.mark.parametrize(
    'follow_author_data',
    [
        "valid_data",
        "invalid_data",
        "already_following"
    ],
    indirect=True
)
def test_follow_author(api_client, follow_author_data, tokens):
    """
    The function test user follow to author.
    """
    status_code, article, user, author = follow_author_data

    access, _ = tokens(user)
    client = api_client(token=access)

    if author:
        response = client.post(f"/api/users/{author.id}/follow/")
        assert response.status_code == status_code
        assert response.data['detail'] in ["Mofaqqiyatli follow qilindi.", "Siz allaqachon ushbu foydalanuvchini kuzatyapsiz."]

        client = api_client(token=access)
        followings_response = client.get("/api/users/following/")
        followings_ids = [followee['id'] for followee in followings_response.data['results']]
        assert author.id in followings_ids

        if status_code == status.HTTP_201_CREATED:
            access, _ = tokens(author)
            client = api_client(token=access)

            response = client.get("/api/users/followers/")

            assert response.status_code == status.HTTP_200_OK
            follower_ids = [follower['id'] for follower in response.data['results']]
            assert user.id in follower_ids
    else:
        response = client.post(f"/api/users/{author}/follow/")
        assert response.status_code == status_code


@pytest.fixture()
@pytest.mark.order(5)
def unfollow_author_data(request, user_factory):

    from tests.factories.follow_factory import FollowFactory
    from tests.factories.article_factory import ArticleFactory

    author = user_factory()
    user = user_factory()
    article = ArticleFactory(author=author)

    def valid_unfollow():
        FollowFactory(follower=user, followee=author)
        return 204, article, user, author

    def unfollow_not_following():
        return 404, article, user, author

    def invalid_unfollow():
        return 404, article, user, None

    data = {
        "valid_unfollow": valid_unfollow,
        "unfollow_not_following": unfollow_not_following,
        "invalid_unfollow": invalid_unfollow,
    }

    return data[request.param]()

@pytest.mark.django_db
@pytest.mark.order(6)
@pytest.mark.parametrize(
    "unfollow_author_data",
    [
        "valid_unfollow",
        "unfollow_not_following",
        "invalid_unfollow"
    ],
    indirect=True
)
def test_unfollow_author(api_client, unfollow_author_data, tokens):
    """
    The function test user unfollow to author.
    """
    status_code, article, user, author = unfollow_author_data

    access, _ = tokens(user)
    client = api_client(token=access)

    if author:
        response = client.delete(f"/api/users/{author.id}/follow/")
        assert response.status_code == status_code

        if status_code == status.HTTP_204_NO_CONTENT:
            access, _ = tokens(author)
            client = api_client(token=access)

            response = client.get("/api/users/followers/")

            assert response.status_code == status.HTTP_200_OK
            follower_ids = [follower['id'] for follower in response.data['results']]
            assert user.id not in follower_ids
    else:
        response = client.delete(f"/api/users/{author}/follow/")
        assert response.status_code == status_code
