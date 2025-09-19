from django_filters.rest_framework import FilterSet
from . import models

# class CourseFilter(FilterSet):
#   class Meta:
#     model = models.Category
#     fields = {
#       'instructor__id': ['exact'],
#       'category__id': ['exact'],
#       'created_at': ['gt', 'lt'],
#       'updated_at': ['gt', 'lt'],
#       'is_published':[], #todo
#     }
    
# class LessonFilter(FilterSet):
#   class Meta:
#     model = models.Lesson
#     fields = {
#       'course__id': ['exact'],
#       'order': ['gt', 'lt'],
#       'created_at': ['gt', 'lt'],
#     }
    
# class EnrollmentFilter(FilterSet):
#   class Meta:
#     model = models.Enrollment
#     fields = {
#       'course__id': ['exact'],
#       'student__id': ['exact'],
#       'enrolled_at': ['gt', 'lt'],
#       'is_active': [], #todo
#     }
    
# class ProgressFilter(FilterSet):
#   class Meta:
#     model = models.Progress
#     fields = {
#       'enrollment__id': ['exact'],
#       'lesson__id': ['exact'],
#       'completed_at': ['gt', 'lt'],
#       'is_completed': [], #todo
#     }