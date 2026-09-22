from django.apps import AppConfig


class UserConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.user"
    label = "user"
    verbose_name = "User"

    def ready(self):
        pass  # import apps.<name>.signals here when needed
