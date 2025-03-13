from django.apps import AppConfig

class UsersConfig(AppConfig):
    """
    Класс UsersConfig наследуется от AppConfig и используется для настройки приложения Django 'users'.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'
    verbose_name = 'Пользователи'
