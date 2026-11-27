"""Application configuration."""
"""Application configuration."""

import os


SERVICE_NAME = "CloudRescue"
APP_VERSION = os.getenv("APP_VERSION", "1.0")
ENVIRONMENT = os.getenv("ENVIRONMENT", "production")
FORCE_UNHEALTHY = os.getenv("FORCE_UNHEALTHY", "false").lower() == "true"
