"""
Taskiq tasks module.
Import all tasks here to make them discoverable by the worker.
"""

from tasks.email_tasks import (
    send_verification_email_task,
    send_password_reset_email_task,
)
from tasks.announcement_tasks import update_announcement_statuses
from tasks.registration_request_tasks import expire_registration_requests_task

__all__ = [
    "send_verification_email_task",
    "send_password_reset_email_task",
    "update_announcement_statuses",
    "expire_registration_requests_task",
]
