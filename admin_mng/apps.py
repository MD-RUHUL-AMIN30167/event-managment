from django.apps import AppConfig


class AdminMngConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'admin_mng'
      

    # signal.py setup
    def ready(self):
        import admin_mng.signals