from django.urls import path
from django.urls.conf import include
from rest_framework_nested import routers
from . import views

router = routers.DefaultRouter()

router.register('courses', views.CourseViewSet, basename='products')
router.register('categories', views.CategoryViewSet)
router.register('enrollments', views.EnrollmentViewSet, basename='enrollments')

courses_router = routers.NestedDefaultRouter(router, 'courses', lookup='course')
courses_router.register('lessons', views.LessonViewSet, basename='course-lessons')

enrollments_router = routers.NestedDefaultRouter(router, 'enrollments', lookup='enrollment')
enrollments_router.register('progress', views.ProgressViewSet, basename='enrollment-progress')

# URLConf
urlpatterns = router.urls + courses_router.urls + enrollments_router.urls