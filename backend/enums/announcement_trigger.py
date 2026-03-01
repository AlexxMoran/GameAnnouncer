from enum import Enum


class AnnouncementTrigger(str, Enum):
    """
    Lifecycle triggers for the announcement state machine.

    Organizer-facing triggers are exposed via dedicated API endpoints.
    AUTO_FINISH is system-only and is fired internally after the final match completes.
    """

    START_QUALIFICATION = "start_qualification"
    FINALIZE_QUALIFICATION = "finalize_qualification"
    GENERATE_BRACKET = "generate_bracket"
    CANCEL = "cancel"
    AUTO_FINISH = "auto_finish"
