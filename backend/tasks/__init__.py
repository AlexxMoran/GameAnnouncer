"""
Taskiq tasks module.
Import all tasks here to make them discoverable by the worker.
"""

from tasks.email_tasks import (
    send_verification_email_task,
    send_password_reset_email_task,
)

__all__ = [
    "send_verification_email_task",
    "send_password_reset_email_task",
]
