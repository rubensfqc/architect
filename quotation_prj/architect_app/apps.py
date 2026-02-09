from django.apps import AppConfig

class ArchitectAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'architect_app'

    def ready(self):
        import architect_app.signals