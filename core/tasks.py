from celery import shared_task
from django.contrib.contenttypes.models import ContentType
from django.conf import settings
from django.apps import apps
from notification.models import Notification

@shared_task
def notify_users(message, object_id=None):
    """
    Create notifications for all recipients with a given message.
    Automatically attaches the 'course.progress' content type.
    """
    Profile = apps.get_model(settings.USER_PROFILE)
    recipients = Profile.objects.all()

    try:
        content_type = ContentType.objects.get(app_label='course', model='progress')
    except ContentType.DoesNotExist:
        return "Content type 'course.progress' not found. No notifications created."

    notifications = [
        Notification(
            recipient=recipient,
            content_type=content_type,
            object_id=object_id or 0,
            message=message,
        )
        for recipient in recipients
    ]

    Notification.objects.bulk_create(notifications, ignore_conflicts=True)
    return f"Created {len(notifications)} notifications with content_type='course.progress'."
