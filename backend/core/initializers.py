from core.logger import logger
from core.permissions import initialize_policies_cache


def initialize_policies():
    """Initialize policies cache at application startup."""
    initialize_policies_cache()
    logger.info("Policies cache initialized")


def initialize_all():
    """
    Run all initialization functions for the application.
    """

    initialize_policies()

    logger.info("✓ Application initialization complete")
