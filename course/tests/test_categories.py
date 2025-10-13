import pytest
from model_bakery import baker
from rest_framework import status
from django.urls import reverse

from course.models import Category

"""
Pytests for Category ViewSet Post and Get
Arrange → Act → Assert rule
Using Fixtures and Model Bakery
"""
@pytest.mark.django_db
class TestCreateCategoryViewSet:
    @pytest.fixture
    def admin_user(self, django_user_model):
        return django_user_model.objects.create_user(
            username="admin", password="pass", is_staff=True
        )

    @pytest.fixture
    def regular_user(self, django_user_model):
        return django_user_model.objects.create_user(
            username="user", password="pass", is_staff=False
        )

    @pytest.fixture
    def api_client(self, client):
        from rest_framework.test import APIClient
        return APIClient()

    @pytest.fixture
    def category_list_url(self):
        return reverse("category-list")

    def test_admin_can_create_category(self, api_client, admin_user, category_list_url):
        api_client.force_authenticate(user=admin_user)
        data = {"title": "New Category", "slug": "new-category"}

        response = api_client.post(category_list_url, data=data, format="json")

        assert response.status_code == status.HTTP_201_CREATED
        assert Category.objects.filter(title="New Category").exists()

    def test_non_admin_cannot_create_category(self, api_client, regular_user, category_list_url):
        api_client.force_authenticate(user=regular_user)
        data = {"title": "User Category", "slug": "user-category"}

        response = api_client.post(category_list_url, data=data, format="json")

        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert not Category.objects.filter(title="User Category").exists()

    def test_unauthenticated_user_cannot_create_category(self, api_client, category_list_url):
        data = {"title": "Anon Category", "slug": "anon-category"}

        response = api_client.post(category_list_url, data=data, format="json")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert not Category.objects.filter(title="Anon Category").exists()


@pytest.mark.django_db
class TestGetCategoryViewSet:
    @pytest.fixture
    def api_client(self):
        from rest_framework.test import APIClient
        return APIClient()

    @pytest.fixture
    def categories(self):
        return baker.make(Category, _quantity=3)

    @pytest.fixture
    def category_list_url(self):
        return reverse("category-list")

    def test_anyone_can_list_categories(self, api_client, categories, category_list_url):
        response = api_client.get(category_list_url)

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data["results"]) == len(categories)
        assert all("title" in item for item in response.data["results"])

    def test_anyone_can_retrieve_category_detail(self, api_client, categories):
        category = categories[0]
        url = reverse("category-detail", args=[category.id])

        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data["id"] == category.id
        assert response.data["title"] == category.title

    def test_category_list_includes_courses_count(self, api_client, categories, category_list_url):
        response = api_client.get(category_list_url)
        first_item = response.data["results"][0]

        assert "courses_count" in first_item
        assert isinstance(first_item["courses_count"], int)
