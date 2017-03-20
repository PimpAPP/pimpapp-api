from django.apps import AppConfig

class ApiConfig(AppConfig):
    name = 'api'
    verbose_name = 'API RECO'

    def ready(self):
        import app_site.api.signals.create_auth_token
