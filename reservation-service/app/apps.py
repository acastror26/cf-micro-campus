from django.apps import AppConfig

class AppConfig(AppConfig):
    name = 'app'
    verbose_name = 'Reservation Service'

    def ready(self) -> None:
        return super().ready()