import os
import sys


def get_token() -> str:
    variable = "TELEGRAM_BOT_TOKEN"
    if variable not in os.environ:
        print(
            f"Please specify bot token in variable {variable}.",
            file=sys.stderr,
        )
        sys.exit(1)
    return os.environ[variable].strip()


def get_maps_api_key() -> str:
    variable = "MAPS_API_KEY"
    if variable not in os.environ:
        print(
            f"Please specify Google Maps API key in variable {variable}.",
            file=sys.stderr,
        )
        sys.exit(1)
    return os.environ[variable].strip()
