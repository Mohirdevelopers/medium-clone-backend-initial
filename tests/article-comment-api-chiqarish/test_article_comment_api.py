import pytest
from django.contrib.auth import get_user_model
from rest_framework import status
from faker import Faker

fake = Faker()
User = get_user_model()


@pytest.fixture
def create_comments_data(request, user_factory):
    """
    The function creates comments data for testing.
    """

    from tests.factories.article_factory import ArticleFactory

    user = user_factory.create()
    article = ArticleFactory.create(author=user)

    article_inactive = ArticleFactory.create(author=user, status="pending")

    def valid_data():
        return (
            201, article.id, user,
            {
                "content": "Assalomu alaykum"
            }
        )

    def invalid_data():
        return (
            400, article.id, user,
            {
                "content": {"foo": "bar"}
            }
        )

    def article_status_inactive():
        return (
            404, article_inactive.id, user,
            {
                "content": "Assalomu alaykum"
            }
        )

    def empty_content():
        return (
            400, article.id, user,
            {
                "content": ""
            }
        )

    def required_content():
        return (
            400, article.id, user,
            {}
        )

    def non_existent_article_id():
        return (
            404, 99999, user,
            {
                "content": "salom"
            }
        )

    data = {
        "valid_data": valid_data,
        "invalid_data": invalid_data,
        "article_status_inactive": article_status_inactive,
        "empty_content": empty_content,
        "required_content": required_content,
        "non_existent_article_id": non_existent_article_id
    }

    return data[request.param]()

@pytest.mark.django_db
@pytest.mark.parametrize(
    "create_comments_data",
    [
        "valid_data",
        "invalid_data",
        "article_status_inactive",
        "empty_content",
        "required_content",
        "non_existent_article_id"
    ],
    indirect=True
)
def test_create_comments_article(api_client, tokens, create_comments_data):
    """
    The function tests the comments functionality on articles.
    """
    status_code, article_id, user, comment_data = create_comments_data

    access, _ = tokens(user)
    client = api_client(token=access)

    response = client.post(f'/articles/{article_id}/comments/', data=comment_data, format='json')

    assert response.status_code == status_code

    if status_code == status.HTTP_201_CREATED:
        assert response.data['content'] == comment_data['content']
    elif status_code == status.HTTP_400_BAD_REQUEST:
        assert 'content' in response.data


@pytest.fixture
def delete_comment_data(request, user_factory):
    """
    Provides test data for deleting comments.
    """

    from tests.factories.article_factory import ArticleFactory
    from tests.factories.comment_factory import CommentFactory

    user = user_factory.create()
    non_author_user = user_factory.create()
    article = ArticleFactory.create(author=user)
    comment = CommentFactory.create(article=article, user=user)

    def valid_deletion():
        return (
            204, comment.id, user
        )

    def non_author_deletion():
        return (
            403, comment.id, non_author_user
        )

    def non_existent_comment():
        return (
            404, 99999, user
        )

    data = {
        "valid_deletion": valid_deletion,
        "non_author_deletion": non_author_deletion,
        "non_existent_comment": non_existent_comment,
    }

    return data[request.param]()


@pytest.mark.django_db
@pytest.mark.parametrize(
    "delete_comment_data",
    [
        "valid_deletion",
        "non_author_deletion",
        "non_existent_comment"
    ],
    indirect=True
)
def test_delete_comment(api_client, tokens, delete_comment_data):
    """
    The function tests the deletion functionality of comments.
    """
    status_code, comment_id, user = delete_comment_data

    access, _ = tokens(user)
    client = api_client(token=access)

    response = client.delete(f'/articles/comments/{comment_id}/')

    assert response.status_code == status_code
    if status_code == 204:
        assert response.data is None
    elif status_code == 403:
        assert response.data['detail'] == 'You do not have permission to perform this action.'
    elif status_code == 404:
        assert response.data['detail'] == 'No Comment matches the given query.'


@pytest.fixture
def update_comment_data(request, user_factory):
    """
    Provides test data for updating comments.
    """

    from tests.factories.article_factory import ArticleFactory
    from tests.factories.comment_factory import CommentFactory

    user = user_factory.create()
    non_author_user = user_factory.create()
    article = ArticleFactory.create(author=user)
    comment = CommentFactory.create(article=article, user=user)

    def valid_update():
        return (
            200, comment.id, user,
            {
                "content": "Updated content"
            }
        )

    def invalid_update():
        return (
            400, comment.id, user,
            {
                "content": {"foo": "bar"}
            }
        )

    def empty_content_update():
        return (
            400, comment.id, user,
            {
                "content": ""
            }
        )

    def non_author_update():
        return (
            403, comment.id, non_author_user,
            {
                "content": "Unauthorized update"
            }
        )

    def non_existent_comment():
        return (
            404, 99999, user,
            {
                "content": "Content for non-existent comment"
            }
        )

    data = {
        "valid_update": valid_update,
        "invalid_update": invalid_update,
        "empty_content_update": empty_content_update,
        "non_author_update": non_author_update,
        "non_existent_comment": non_existent_comment,
    }

    return data[request.param]()

@pytest.mark.django_db
@pytest.mark.parametrize(
    "update_comment_data",
    [
        "valid_update",
        "invalid_update",
        "empty_content_update",
        "non_author_update",
        "non_existent_comment"
    ],
    indirect=True
)
def test_partial_update_comment(api_client, tokens, update_comment_data):
    """
    The function tests the partial update functionality of comments.
    """
    status_code, comment_id, user, update_data = update_comment_data

    access, _ = tokens(user)
    client = api_client(token=access)

    response = client.patch(f'/articles/comments/{comment_id}/', data=update_data, format='json')

    assert response.status_code == status_code
    if status_code == 200:
        assert response.data['content'] == update_data['content']
    elif status_code == 400:
        assert 'content' in response.data
    elif status_code == 403:
        assert response.data['detail'] == 'You do not have permission to perform this action.'
    elif status_code == 404:
        assert response.data['detail'] == 'No Comment matches the given query.'


@pytest.fixture
def create_comment_with_parent_data(request, user_factory):
    """
    Provides test data for creating a comment with a parent.
    """

    from tests.factories.article_factory import ArticleFactory
    from tests.factories.comment_factory import CommentFactory

    user = user_factory.create()
    article = ArticleFactory.create(author=user)
    parent_comment = CommentFactory.create(article=article, user=user)

    def valid_data():
        return (
            201, article.id, user,
            {
                "parent": parent_comment.id,
                "content": "string"
            }
        )

    def invalid_parent():
        return (
            400, article.id, user,
            {
                "parent": 99999,
                "content": "string"
            }
        )

    def missing_content():
        return (
            400, article.id, user,
            {
                "parent": parent_comment.id
            }
        )

    def non_existent_article():
        return (
            404, 99999, user,
            {
                "parent": parent_comment.id,
                "content": "string"
            }
        )

    data = {
        "valid_data": valid_data,
        "invalid_parent": invalid_parent,
        "missing_content": missing_content,
        "non_existent_article": non_existent_article,
    }

    return data[request.param]()


@pytest.mark.django_db
@pytest.mark.parametrize(
    "create_comment_with_parent_data",
    [
        "valid_data",
        "invalid_parent",
        "missing_content",
        "non_existent_article"
    ],
    indirect=True
)
def test_create_comment_with_parent(api_client, tokens, create_comment_with_parent_data):
    """
    Tests the creation of a comment with a parent comment.
    """
    status_code, article_id, user, comment_data = create_comment_with_parent_data

    access, _ = tokens(user)
    client = api_client(token=access)

    response = client.post(f'/articles/{article_id}/comments/', data=comment_data, format='json')

    assert response.status_code == status_code

    if status_code == status.HTTP_201_CREATED:
        assert response.data['parent'] == comment_data['parent']
        assert response.data['content'] == comment_data['content']
        assert response.data['article'] == article_id
    elif status_code == status.HTTP_400_BAD_REQUEST:
        assert 'parent' in response.data or 'content' in response.data
    elif status_code == status.HTTP_404_NOT_FOUND:
        if article_id == 99999:
            assert response.data['detail'] == 'No Article matches the given query.'


@pytest.fixture
def get_comment_from_article(request, user_factory):
    """
    Provides test data for retrieving comments from an article.
    """

    from tests.factories.article_factory import ArticleFactory
    from tests.factories.comment_factory import CommentFactory

    user = user_factory.create()
    article = ArticleFactory.create(author=user)

    comments = [
        CommentFactory.create(article=article, user=user, content="Comment 1"),
        CommentFactory.create(article=article, user=user, content="Comment 2"),
        CommentFactory.create(article=article, user=user, content="Comment 3")
    ]

    def valid_data():
        return (
            200, article.id, user, comments
        )

    data = {
        "valid_data": valid_data
    }

    return data[request.param]()


@pytest.mark.django_db
@pytest.mark.parametrize(
    "get_comment_from_article",
    [
        "valid_data",
    ],
    indirect=True
)
def test_get_comment_from_article(api_client, tokens, get_comment_from_article):
    """
    Tests the retrieval of comments from an article.
    """
    status_code, article_id, user, expected_comments = get_comment_from_article

    access, _ = tokens(user)
    client = api_client(token=access)

    response = client.get(f'/articles/{article_id}/detail/comments/')

    assert response.status_code == status_code

    if status_code == status.HTTP_200_OK:
        results = response.data.get('results', [])
        assert len(results[0]["comments"]) == len(expected_comments)
        for comment in expected_comments:
            assert any(c['content'] == comment.content for c in results[0]["comments"])
