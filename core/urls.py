from django.urls import path
from django.urls.conf import include
from django.views.generic import TemplateView
from rest_framework_nested import routers
from . import views

router = routers.DefaultRouter()

router.register('profiles', views.ProfileViewSet, basename='profiles')
router.register("register", views.RegisterViewSet, basename="register")

# URLConf
urlpatterns = [
    path('', TemplateView.as_view(template_name='core/index.html'))
] + router.urls