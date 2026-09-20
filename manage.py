import os
import sys


def main():
    django_env = os.environ.get("DJANGO_ENV", "development")
    settings_module = f"config.settings.{django_env}"
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", settings_module)

    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError("Couldn't import Django.") from exc

    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
