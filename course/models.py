from django.db import models
from django.conf import settings

# Create your models here.
class Category(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField()
    featured_course = models.ForeignKey(
        "Course", on_delete=models.SET_NULL, null=True, related_name="+", blank=True
    )

    class Meta:
        ordering = ["title"]

    def __str__(self) -> str:
        return self.title


class Course(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    instructor = models.ForeignKey(
        settings.USER_PROFILE, on_delete=models.CASCADE, related_name="courses"
    )
    category = models.ForeignKey(
        Category, on_delete=models.PROTECT, related_name="courses"
    )
    thumbnail = models.ImageField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=False)

    class Meta:
        ordering = ["title"]

    def __str__(self) -> str:
        return self.title


class Lesson(models.Model):
    title = models.CharField(max_length=255)
    order = models.PositiveIntegerField()
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    content = models.TextField()
    video_file = models.FileField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["title"]

    def __str__(self) -> str:
        return self.title


class Enrollment(models.Model):
    student = models.ForeignKey(
        settings.USER_PROFILE, on_delete=models.CASCADE, related_name="enrollments"
    )
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, related_name="enrollments"
    )
    enrolled_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["-enrolled_at"]
        constraints = [
            models.UniqueConstraint(
                fields=["student", "course"], name="unique_course_enrollment"
            )
        ]


class Progress(models.Model):
    enrollment = models.ForeignKey(
        Enrollment, on_delete=models.CASCADE, related_name="progress"
    )
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    is_completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True)

    class Meta:
        ordering = ["-completed_at"]
        constraints = [
            models.UniqueConstraint(
                fields=["enrollment", "lesson"], name="unique_lesson_progress"
            )
        ]
