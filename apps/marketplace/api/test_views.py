import pytest
from django.urls import reverse
from django.utils import formats

from rest_framework import status
from rest_framework.test import APIClient

from apps.marketplace.factories import LotFactory
from apps.marketplace.models import Comment, Category
from apps.users.factories.create_users_factory import UsersFactory


@pytest.fixture(autouse=True)
def enable_db_access_for_all_tests(db):
    """Give all tests access to db."""
    return pytest.mark.django_db


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def parent():
    return Category.objects.create(name='parent_category')


@pytest.fixture
def first_child(parent):
    return Category.objects.create(name='first_child', parent=parent)


@pytest.fixture
def second_child(parent):
    return Category.objects.create(name='second_child', parent=parent)


@pytest.fixture
def lot():
    return LotFactory()


@pytest.fixture
def user():
    return UsersFactory()


@pytest.fixture
def auth_user(api_client, user):
    api_client.force_authenticate(user)
    return api_client


class TestCategoryChildrenViewSet:
    """Test class for CategoryChildrenViewSet."""

    def get_url(self, id):
        return reverse('category-children-list', kwargs={'id': id})

    def test_returns_correct_category_children(
            self,
            api_client,
            parent,
            first_child,
            second_child,
    ):
        """Should returns list of children category."""
        response = api_client.get(self.get_url(parent.pk))

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == len(parent.children.all())
        assert response.data[0]['name'] == first_child.name
        assert response.data[1]['name'] == second_child.name
        assert response.data[0]['parent'] == parent.pk
        assert response.data[1]['parent'] == parent.pk

    def test_returns_404_for_not_existing_category(self, api_client, parent):
        """If category not exist should returns 404."""
        non_exist_category_id = parent.id + 1
        response = api_client.get(self.get_url(non_exist_category_id))

        assert response.status_code == status.HTTP_404_NOT_FOUND


class TestCreateCommentViewSet:
    """Test class for CategoryChildrenViewSet."""
    @pytest.fixture
    def url(self):
        return reverse('create-comment-list')

    def test_returns_201_and_info_about_new_comment(
            self,
            lot,
            auth_user,
            url,
            user,
    ):
        """Should returns info about created comment."""
        data = {'lot': lot.pk, 'text': 'test'}
        response = auth_user.post(url, data)
        comment = Comment.objects.last()

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['user']['username'] == user.username
        assert response.data['text'] == data['text']
        assert response.data['created_at_format'] == formats.date_format(
            comment.created_at,
            'd N Y H:i',
        )

    def test_returns_403_for_not_auth_user(self, api_client, url, lot):
        """An unauthorized user cannot comment."""
        data = {'lot': lot.pk, 'text': 'test'}
        response = api_client.post(url, data)

        assert response.status_code == status.HTTP_403_FORBIDDEN