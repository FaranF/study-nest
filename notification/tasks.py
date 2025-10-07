# tasks.py
from celery import shared_task
from django.contrib.contenttypes.models import ContentType
from django.conf import settings
from django.apps import apps
from .models import Notification

@shared_task
def notify_users(message, content_type_app_label=None, content_type_model=None, object_id=None):
    """
    Create notifications for all recipients with a given message.
    Optionally attach a content object via content type and object_id.
    """
    Profile = apps.get_model(settings.USER_PROFILE)
    recipients = Profile.objects.all()

    content_type = None
    if content_type_app_label and content_type_model:
        try:
            content_type = ContentType.objects.get(
                app_label=content_type_app_label,
                model=content_type_model
            )
        except ContentType.DoesNotExist:
            content_type = None

    notifications = []
    for recipient in recipients:
        notifications.append(Notification(
            recipient=recipient,
            content_type=content_type,
            object_id=object_id or 0,
            message=message,
        ))

    Notification.objects.bulk_create(notifications, ignore_conflicts=True)
    return f"Created {len(notifications)} notifications."


# notify_students.delay("This is a test notification.")
